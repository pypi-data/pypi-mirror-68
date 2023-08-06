Introduction
============
`aiobme280` is a Python 3 module to read data asynchronously from BME280
environmental sensor.

Features

- asynchronous sensor data read using Python asyncio coroutines, which
  allows to read multiple sensors in parallel without using threads
- sensor is put into sleep mode to minimize power consumption after data is
  read

Requirements

- Python 3.8
- cython 0.29
- optionally, uvloop

.. vim: sw=4:et:ai
