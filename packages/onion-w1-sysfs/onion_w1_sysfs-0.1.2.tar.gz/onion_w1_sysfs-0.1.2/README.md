# w1-sysfs
One Wire protocol library using the sysfs interface

## Compatibility

Now comptatible with all Python 3 versions.

## Install

pip install onion-w1-sysfs

## Usage

        OneWire# python
        Python 3.6.9 (default, Dec 06 2019, 16:28:06)
        [GCC 7.3.0] on linux
        Type "help", "copyright", "credits" or "license" for more information.
        >>> from OneWire import OneWire
        >>> w1 = OneWire(0)
        >>> w1.read_device()
        ['85 01 4b 46 7f ff 0c 10 31 : crc=31 YES\n', '85 01 4b 46 7f ff 0c 10 31 t=24312\n']
        >>> w1.read_device()[1].split('=')[1].rstrip()
        '24312'
        >>>

## Author

PyPi package by https://github.com/grizmin