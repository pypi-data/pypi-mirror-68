Configuration
=============
If using Raspberry Pi, then enable I2C Linux kernel subsystem by adding
the following line in `/boot/config.txt` file::

    dtparam=i2c=on

Add user reading data from a sensor to `uucp` group and create the
following udev rule in the `/etc/udev/rules.d` file::

    KERNEL=="i2c-[0-9]*", GROUP="uucp", MODE="0660"

.. vim: sw=4:et:ai
