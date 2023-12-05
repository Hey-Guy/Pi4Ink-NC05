import sys
from adafruit_bus_device.i2c_device import I2CDevice

# pylint: disable=wrong-import-position
try:
    lib_index = sys.path.index("/lib")  # pylint: disable=invalid-name
    if lib_index < sys.path.index(".frozen"):
        # Prefer frozen modules over those in /lib.
        sys.path.insert(lib_index, ".frozen")
except ValueError:
    # Don't change sys.path if it doesn't contain "lib" or ".frozen".
    pass

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/schlafsack/CircuitPython_NCD_PR33_15.git"

DEVICE_ADDRESS = 0x68  # default address of PR33-15 board

GAIN_1X = 0x00
GAIN_2X = 0x01
GAIN_4X = 0x02
GAIN_8X = 0x03

SAMPLE_RATE_12_BIT = 0x00
SAMPLE_RATE_14_BIT = 0x01
SAMPLE_RATE_16_BIT = 0x02

CHANNEL_1 = 0x00
CHANNEL_2 = 0x02
CHANNEL_3 = 0x04
CHANNEL_4 = 0x06

SAMPLE_BITS = {
    SAMPLE_RATE_12_BIT: 12,
    SAMPLE_RATE_14_BIT: 14,
    SAMPLE_RATE_16_BIT: 16,
}

RESOLUTION = {
    SAMPLE_RATE_12_BIT: 0.001,
    SAMPLE_RATE_14_BIT: 0.00025,
    SAMPLE_RATE_16_BIT: 0.0000625,
}

GAIN_DIVIDER = {
    GAIN_1X: 1,
    GAIN_2X: 2,
    GAIN_4X: 4,
    GAIN_8X: 8,
}


class ConfigBits:

    def __init__(self, num_bits, lowest_bit):
        self.bit_mask = ((1 << num_bits) - 1) << lowest_bit
        if self.bit_mask >= 1 << 8:
            raise ValueError("Cannot have more than 8 bits")
        self.lowest_bit = lowest_bit
        self.buffer = bytearray(3)

    def __get__(self, obj, objtype=None):
        with obj.i2c_device as i2c:
            i2c.readinto(self.buffer)
        return (self.buffer[2] & self.bit_mask) >> self.lowest_bit

    def __set__(self, obj, value):
        value <<= self.lowest_bit  # shift the value over to the right spot
        with obj.i2c_device as i2c:
            i2c.readinto(self.buffer)
            reg = self.buffer[2]
            reg &= ~self.bit_mask  # mask off the bits we're about to change
            reg |= value  # then or in our new value
            self.buffer[2] = reg & 0xFF
            i2c.write(self.buffer[2:3])


class Receiver:

    def __init__(self, i2c, device_address=DEVICE_ADDRESS):
        self.i2c_device = I2CDevice(i2c, device_address)
        self.buffer = bytearray(2)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def raw_value(self):
        sample_rate = self.sample_rate
        sample_bits = SAMPLE_BITS[sample_rate]
        self.ready = 1
        while self.ready:
            continue
        with self.i2c_device as i2c:
            i2c.readinto(self.buffer)
        raw_data = ((self.buffer[0] << 8) + self.buffer[1]) & (65535 >> (16 - sample_bits))
        raw_data -= int((raw_data << 1) & 2 ** sample_bits)
        return raw_data

    # configuration properties
    gain = ConfigBits(2, 0)  # 2 bits: bits 0 & 1
    sample_rate = ConfigBits(2, 2)  # 2 bits: bits 2 & 3
    continuous = ConfigBits(1, 4)  # 1 bit: bit 4
    channel = ConfigBits(2, 5)  # 2 bits: bit 5 & 6
    ready = ConfigBits(1, 7)  # 1 bit: bit 7