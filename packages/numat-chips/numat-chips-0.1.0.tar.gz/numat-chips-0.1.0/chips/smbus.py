"""
Chips that communicate over System Management Bus.

Distributed under the GNU General Public License v3
Copyright (C) 2015 NuMat Technologies
"""
import smbus
import time


class ADS1115(object):
    """Base class for devices connected to the ADS1115, a 16-bit ADC."""

    sample_rate_options = [8, 16, 32, 64, 128, 250, 475, 860]
    gain_options = [6144, 4096, 2048, 1024, 512, 256]

    def __init__(self, adc_channel, i2c_address=0x48, gain=4096, rate=250):
        """Open a channel for I2C communication.

        Args:
            adc_channel: The ADC channel on the ADS1115 to read, [0, 3].
            i2c_address: (Optional) The I2C address of the device, configurable
                in the circuit. Default is address to ground, or 0x48.
            gain: (Optional) Maximum voltage, in millivolts.
            rate: (Optional) Sampling speed. Provides a handle on speed
                versus reliability.

        """
        self.i2c = smbus.SMBus(1)
        self.i2c_address = i2c_address
        self.adc_channel = adc_channel
        self.gain, self.rate = gain, rate
        self._write_config()

    def _write_config(self):
        """Write out configuration data to the ADC.

        This driver makes some assumptions on use case, only functionalizing
        some of the config options. For more information, read the
        [datasheet](http://www.ti.com/lit/ds/symlink/ads1115.pdf).

        """
        if self.gain not in self.gain_options:
            raise ValueError("Gain must be in {}.".format(self.gain_options))
        if self.rate not in self.sample_rate_options:
            raise ValueError("Sample rate must be in {}.".format(
                             self.sample_rate_options))

        a = self.adc_channel
        g = self.gain_options.index(self.gain)
        r = self.sample_rate_options.index(self.rate)

        bits = [1,                                  # 15: operational status
                1, (a >> 1) & 1, a & 1,             # 14:12: channels
                (g >> 2) & 1, (g >> 1) & 1, g & 1,  # 11:9: gain
                1,                                  # 8: operating mode
                (r >> 2) & 1, (r >> 1) & 1, r & 1,  # 7:5: sample rate
                0, 0, 0, 1, 1]                      # 5:0 comparator
        data = [sum(b << (7 - i) for i, b in enumerate(byte))
                for byte in (bits[:8], bits[8:])]
        self.i2c.write_i2c_block_data(self.i2c_address, 0x01, data)
        time.sleep(1.0 / self.rate + 0.0001)

    def _read_adc(self):
        """Read the analog-to-digital converter pin."""
        self._write_config()
        adc = self.i2c.read_i2c_block_data(self.i2c_address, 0x00, 2)
        return (adc[0] << 8) + adc[1]

    def read_voltage(self):
        """Read the ADC and converts to voltage."""
        return self._read_adc() * self.gain / 32768.0 / 1000.0
