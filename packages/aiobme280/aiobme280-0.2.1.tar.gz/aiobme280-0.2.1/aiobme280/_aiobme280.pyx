#
# aiobme280 - BME280 sensor asyncio library
#
# Copyright (C) 2016-2020 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# distutils: language = c
# cython: c_string_type=unicode, c_string_encoding=utf8, language_level=3str

import logging
import os

from libc.errno cimport errno
from libc.stdint cimport int8_t, int16_t, int32_t, int64_t, \
    uint8_t, uint16_t, uint32_t, uint64_t
from posix.unistd cimport read, write, close, usleep
from posix.fcntl cimport open, O_RDWR
from posix.time cimport itimerspec, timespec, clock_gettime
from posix.ioctl cimport ioctl

from .error import *

logger = logging.getLogger(__name__)

#
# Delay [us] needed for measurement based on datasheet (t_{measure,max},
# page 27)
#
#     (1.25 + 2.3 * 16 + 2.3 * 16 + 0.575 + 2.3 * 16 + 0.575) * 1000
#
DELAY = 112800

I2C_SLAVE = 0x0703

cdef uint8_t *CMD_SENSOR_REGISTER = [0xd0]
cdef uint8_t *CMD_SENSOR_REGISTER_H4_H5 = [0xe4, 0xe5, 0xe6]
cdef uint8_t *CMD_SENSOR_READ_START = [0xf7]

cdef extern from "<sys/timerfd.h>":
    enum: CLOCK_MONOTONIC

    int timerfd_create(int, int)
    int timerfd_settime(int, int, itimerspec*, itimerspec*)

#cdef extern from "<sys/ioctl.h>":
#    enum: I2C_SLAVE

cdef class SensorData:
    cdef public float temperature
    cdef public float pressure
    cdef public float humidity

    cdef public int i2c_fd
    cdef public int timer_fd

    cdef public int32_t fine

    cdef public uint16_t dig_t1
    cdef public int16_t dig_t2
    cdef public int16_t dig_t3

    cdef public uint16_t dig_p1
    cdef public int16_t dig_p2
    cdef public int16_t dig_p3
    cdef public int16_t dig_p4
    cdef public int16_t dig_p5
    cdef public int16_t dig_p6
    cdef public int16_t dig_p7
    cdef public int16_t dig_p8
    cdef public int16_t dig_p9

    cdef public uint8_t dig_h1
    cdef public int16_t dig_h2
    cdef public uint8_t dig_h3
    cdef public int16_t dig_h4
    cdef public int16_t dig_h5
    cdef public int8_t dig_h6

    def __init__(self, int i2c_fd, int timer_fd):
        self.i2c_fd = i2c_fd
        self.timer_fd = timer_fd

#
# Functions to calculate temperature, pressure and humidity using raw data and
# compensation parameters.

cdef int32_t calc_temperature(SensorData data, int32_t raw):
    cdef int32_t var1, var2, temperature

    var1 = ((((raw >> 3) - (data.dig_t1 << 1))) * data.dig_t2) >> 11
    var2 = (((((raw >> 4) - data.dig_t1) * ((raw >> 4) - data.dig_t1)) >> 12) * data.dig_t3) >> 14

    data.fine = var1 + var2
    temperature = (data.fine * 5 + 128) >> 8
    return temperature

cdef uint32_t calc_pressure(SensorData data, int32_t raw):
    cdef int64_t var1, var2, pressure

    var1 = data.fine - 128000
    var2 = var1 * var1 * data.dig_p6
    var2 = var2 + (var1*data.dig_p5 << 17)
    var2 = var2 + (<int64_t> data.dig_p4 << 35)
    var1 = ((var1 * var1 * data.dig_p3) >> 8) + ((var1 * data.dig_p2) << 12)
    var1 = ((<int64_t> 1 << 47) + var1) * data.dig_p1 >> 33

    if var1 == 0:
        return 0

    pressure = 1048576 - raw
    pressure = (((pressure << 31) - var2) * 3125) // var1
    var1 = (data.dig_p9 * (pressure >> 13) * (pressure >> 13)) >> 25
    var2 = (data.dig_p8 * pressure) >> 19
    pressure = ((pressure + var1 + var2) >> 8) + (data.dig_p7 << 4)
    return pressure

cdef uint32_t calc_humidity(SensorData data, int32_t raw):
    cdef int32_t var
    var = data.fine - 76800
    var = (((((raw << 14) - (<int32_t> data.dig_h4 << 20) - (data.dig_h5 * var)) + 16384) >> 15)
        * (((((((var * data.dig_h6) >> 10) * (((var * data.dig_h3) >> 11) + 32768)) >> 10) + 2097152)
        * data.dig_h2 + 8192) >> 14))
    var = (var - (((((var >> 15) * (var >> 15)) >> 7) * data.dig_h1) >> 4))
    var = 0 if var < 0 else var
    var = 419430400 if var > 419430400 else var
    return var >> 12

#
# Data reading and writing helper functions.
#

cdef int read_reg_word(int i2c_fd, uint8_t reg, uint16_t *value):
    cdef uint8_t *reg_data = [reg, reg + 1]
    cdef uint8_t data[2]
    cdef int r

    r = write(i2c_fd, reg_data, 2)
    if r != 2:
        return -1

    r = read(i2c_fd, data, 2)
    if r != 2:
        return -1

    logger.debug('BME280: register value: %02x %02x'.format(data[0], data[1]))
    value[0] = ((data[1]) << 8) | data[0]
    return 0

cdef int read_reg_byte(int i2c_fd, uint8_t reg, uint8_t *value):
    cdef int r
    cdef uint8_t *reg_data = [reg]

    r = write(i2c_fd, reg_data, 1)
    if r != 1:
        return -1

    r = read(i2c_fd, value, 1)
    if r != 1:
        return -1
    return 0

cdef int write_config(int i2c_fd, uint8_t reg, uint8_t value):
    cdef uint8_t *data = [reg, value]
    cdef int r

    r = write(i2c_fd, data, 2)
    if r != 2:
        return -1
    return 0

cdef int read_reg_h4_h5(int i2c_fd, int16_t *dig_h4, int16_t *dig_h5):
    cdef uint8_t buff[6]
    cdef int r

    r = write(i2c_fd, CMD_SENSOR_REGISTER_H4_H5, 2)
    if r != 2:  # FIXME
        return -1
    r = read(i2c_fd, buff, 3)
    if r != 3:
        return -1

    dig_h4[0] = (buff[0] << 4) | (buff[1] & 0x0f)
    dig_h5[0] = (buff[1] << 4) | (buff[2] >> 4)
    return 0

#
# High level helper functions to enable sensor, reset sensor and read data
# from sensor.
#

cdef int reset_sensor(int i2c_fd):
    cdef uint8_t reg_id
    cdef int r

    # reset sensor
    r = write_config(i2c_fd, 0xe0, 0xb6)
    if r != 0:
        return -1

    # read sensor register id until its value is 0x60
    for i in range(1, 6):
        r = write(i2c_fd, CMD_SENSOR_REGISTER, 1)
        if r != 1:
            return -1

        r = read(i2c_fd, &reg_id, 1)
        if r != 1:
            return -1

        logger.debug('register id value 0x%02x, attempt %d/5'.format(reg_id, i))
        if reg_id == 0x60:
            break
        usleep(5000)

    logger.debug('sensor reset performed')
    return 0

cdef int enable_sensor(SensorData data):
    cdef int r

    # enable humidity measurement
    r = write_config(data.i2c_fd, 0xf2, 0x05)
    if r != 0:
        return -1

    # enable temperature and pressure measurement
    # set forced mode
    r = write_config(data.i2c_fd, 0xf4, 0xb6)
    if r != 0:
        return -1

    # ir filter coefficient = 16
    r = write_config(data.i2c_fd, 0xf5, 0x08)
    if r != 0:
        return -1

    return 0

cdef int read_data_start(SensorData data):
    cdef int r

    r = enable_sensor(data)
    if r != 0:
        return -1

    r = write(data.i2c_fd, CMD_SENSOR_READ_START, 1)
    if r != 1:
        return -1
    return 0

cdef int read_data_end(SensorData data):
    cdef int r
    cdef int32_t raw
    cdef uint8_t buff[8]

    r = read(data.i2c_fd, buff, 8)
    if r != 8:
        return -1

    logger.debug(
        'raw data %02x %02x %02x %02x %02x %02x %02x %02x'.format(
            buff[0], buff[1], buff[2], buff[3], buff[4], buff[5], buff[6],
            buff[7]
    ))

    raw = (buff[0] << 12) | (buff[1] << 4) | (buff[2] >> 4)
    data.pressure = calc_pressure(data, raw) / 256.0
    raw = (buff[3] << 12) | (buff[4] << 4) | (buff[5] >> 4)
    data.temperature = calc_temperature(data, raw) / 100.0
    raw = (buff[6] << 8) | buff[7]
    data.humidity = calc_humidity(data, raw) / 1024.0

    r = write_config(data.i2c_fd, 0xf4, 0x00)   # force sleep
    if r != 0:
        return -1

    return 0

#
# Sensor functions API implementation.
#

def bme280_init(bytes f_dev, uint8_t address) -> SensorData:
    cdef int r
    cdef int i2c_fd
    cdef int timer_fd
    cdef uint16_t result
    cdef uint8_t result8

    i2c_fd = open(f_dev, O_RDWR)
    if i2c_fd < 0:
        raise SensorInitError(
            'cannot open device {}: {}'
            .format(f_dev.decode(), os.strerror(errno))
        )

    r = ioctl(i2c_fd, I2C_SLAVE, address)
    if r < 0:
        raise SensorInitError(
            'cannot initalize i2c device at address 0x{:02x}: {}'
            .format(address, os.strerror(errno))
        )

    timer_fd = timerfd_create(CLOCK_MONOTONIC, 0)
    if timer_fd < 0:
        raise SensorInitError(
            'cannot create timer: {}'
            .format(os.strerror(errno))
        )
    r = reset_sensor(i2c_fd)
    if r != 0:
        raise SensorInitError(
            'sensor reset failed: {}'
            .format(os.strerror(errno))
        )

    data = SensorData(i2c_fd, timer_fd)

    r = enable_sensor(data)
    if r != 0:
        raise SensorInitError(
            'enabling sensor failed: {}'
            .format(os.strerror(errno))
        )

    read_reg_word(i2c_fd, 0x88, &data.dig_t1)
    read_reg_word(i2c_fd, 0x8a, &result)
    data.dig_t2 = result
    read_reg_word(i2c_fd, 0x8c, &result)
    data.dig_t3 = result

    read_reg_word(i2c_fd, 0x8e, &data.dig_p1)
    read_reg_word(i2c_fd, 0x90, &result)
    data.dig_p2 = result
    read_reg_word(i2c_fd, 0x92, &result)
    data.dig_p3 = result
    read_reg_word(i2c_fd, 0x94, &result)
    data.dig_p4 = result
    read_reg_word(i2c_fd, 0x96, &result)
    data.dig_p5 = result
    read_reg_word(i2c_fd, 0x98, &result)
    data.dig_p6 = result
    read_reg_word(i2c_fd, 0x9a, &result)
    data.dig_p7 = result
    read_reg_word(i2c_fd, 0x9c, &result)
    data.dig_p8 = result
    read_reg_word(i2c_fd, 0x9e, &result)
    data.dig_p9 = result

    read_reg_byte(i2c_fd, 0xa1, &data.dig_h1)
    read_reg_word(i2c_fd, 0xe1, &result)
    data.dig_h2 = result
    read_reg_byte(i2c_fd, 0xe3, &data.dig_h3)
    read_reg_h4_h5(i2c_fd, &data.dig_h4, &data.dig_h5)
    read_reg_byte(i2c_fd, 0xe7, &result8)
    data.dig_h6 = result8

    return data

def bme280_read_start(SensorData data):
    cdef itimerspec ts
    cdef int r

    r = read_data_start(data)
    if r != 0:
        raise SensorReadError(
            'cannot start sensor read: {}'
            .format(os.strerror(errno))
        )

    ts.it_interval.tv_sec = 0
    ts.it_interval.tv_nsec = 0
    ts.it_value.tv_sec = 0
    ts.it_value.tv_nsec = DELAY * 1000   # usleep(DELAY)
    r = timerfd_settime(data.timer_fd, 0, &ts, NULL)
    if r != 0:
        raise SensorReadError(
            'cannot start sensor read timer: {}'
            .format(os.strerror(errno))
        )

def bme280_read_end(SensorData data):
    cdef int r
    cdef uint64_t value

    # disable timer
    r = read(data.timer_fd, &value, 8)
    if r != 8:
        raise SensorReadError(
            'cannot stop sensor read timer (result={}): {}'
            .format(r, os.strerror(errno))
        )

    # read sensor data
    r = read_data_end(data)
    if r != 0:
        raise SensorReadError(
            'sensor data read failed: {}'
            .format(os.strerror(errno))
        )

def bme280_close(SensorData data):
    cdef int r
    r = close(data.timer_fd)
    if r != 0:
        raise SensorCloseError(
            'cannot stop sensor timer: {}'
            .format(os.strerror(errno))
        )

    r = close(data.i2c_fd)
    if r != 0:
        raise SensorCloseError(
            'cannot close i2c device: {}'
            .format(os.strerror(errno))
        )

# vim: sw=4:et:ai
