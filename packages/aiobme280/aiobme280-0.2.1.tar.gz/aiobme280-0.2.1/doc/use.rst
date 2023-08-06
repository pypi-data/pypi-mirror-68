Using the Library
=================
Sensor instance is created with :py:class:`aiobme280.Sensor` class. The
object provides :py:func:`aiobme280.Sensor.read` asynchronous coroutine
to read data from the sensor.

The data is returned as a tuple of three values: pressure, temperature and
humidity.

Example usage::

    import asyncio
    import aiobme280

    async def read_data():
        sensor = aiobme280.Sensor('/dev/i2c-1', 0x77)
        while True:
            pressure, temperature, humidity = await sensor.read()
            print(pressure, temperature, humidity)

            await asyncio.sleep(1)

    asyncio.run(read_data())

.. vim: sw=4:et:ai
