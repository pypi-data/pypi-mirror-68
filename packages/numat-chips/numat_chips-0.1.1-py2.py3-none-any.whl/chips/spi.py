"""
Chips that communicate over Serial Peripheral Interface.

Distributed under the GNU General Public License v3
Copyright (C) 2015 NuMat Technologies
"""
import logging
import spidev
import time

logger = logging.getLogger('chips')


class MCP3008(object):
    """Base class for devices connected to the MCP3008, a 10-bit ADC.

    This is a low-accuracy high-speed chip, which means that the data can be
    noisy. Only use with low-accuracy sensors!
    """

    def __init__(self, adc_channel, bus=0, device=0):
        """Open a channel for SPI communication.

        Args:
            adc_channel: The ADC channel on the MCP3008 to read, [0, 7].

        """
        if adc_channel < 0 or adc_channel > 7:
            raise ValueError("ADC channel must be in the range [0, 7].")
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.max = 1024.0
        self.adc_channel = adc_channel

    def _read_adc(self):
        """Read the analog-to-digital converter pin, outputs [0, 1024)."""
        adc = self.spi.xfer2([1, (8 + self.adc_channel) << 4, 0])
        return ((adc[1] & 3) << 8) + adc[2]

    def read_voltage(self):
        """Read the ADC and converts to voltage, 0-3.3V."""
        return self._read_adc() * (10.0 / 3.0) / self.max

    def close(self):
        """Close the SPI connection."""
        self.spi.close()


class MCP3208(object):
    """Base class for devices connected to the MCP3208, a 12-bit ADC.

    This should always be preferred over the 10-bit MCP3008. For better
    resolution, use the 16-bit ADS1115.
    """

    def __init__(self, adc_channel, bus=0, device=0):
        """Open a channel for SPI communication.

        Args:
            adc_channel: The ADC channel on the MCP3008 to read, [0, 7].
            weight: The number of past datapoints to average into voltage
                readings. Higher weights improve smoothing but increase
                lag time.

        """
        if adc_channel < 0 or adc_channel > 7:
            raise ValueError("ADC channel must be in the range [0, 7].")
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.max = 4096.0
        self.adc_channel = adc_channel

    def _read_adc(self):
        """Read the analog-to-digital converter pin, outputs [0, 4096)."""
        adc = self.spi.xfer2([6 + ((self.adc_channel >> 2) & 1),
                              (self.adc_channel & 3) << 6, 0])
        return ((adc[1] & 15) << 8) + adc[2]

    def read_voltage(self):
        """Read the ADC and converts to voltage, 0-3.3V."""
        return self._read_adc() * (10.0 / 3.0) / self.max

    def close(self):
        """Close the SPI connection."""
        self.spi.close()


class MCP3202(object):
    """Base class for devices connected to the MCP3202, a 12-bit ADC.

    This is a 2-port version of the MCP3208.
    """

    def __init__(self, adc_channel=0, bus=0, device=0):
        """Open a channel for SPI communication.

        Args:
            adc_channel: The ADC channel on the MCP3202 to read, 0 or 1.

        """
        if adc_channel not in [0, 1]:
            raise ValueError("ADC channel must be 0 or 1.")
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.max = 4096.0
        self.adc_channel = adc_channel
        # Slowing down the speed significantly helps read stability
        # https://www.raspberrypi.org/forums/viewtopic.php?t=115971
        self.spi.max_speed_hz = 1350000

    def _read_adc(self):
        """Read the analog-to-digital converter pin, outputs [0, max)."""
        adc = self.spi.xfer2([1, 160 + (self.adc_channel << 6), 0])
        return ((adc[1] & 15) << 8) + adc[2]

    def read_voltage(self):
        """Read the ADC and converts to voltage, 0-3.3V."""
        return self._read_adc() * (10.0 / 3.0) / self.max

    def close(self):
        """Close the SPI connection."""
        self.spi.close()


class ADS8344(object):
    """Base class for devices connected to the ADS8344, a 16-bit ADC.

    Datasheet [here](http://www.ti.com/lit/ds/symlink/ads8344.pdf).
    """

    # ADC channels to binary, from the datasheet. It's a little weird.
    bitmap = [0, 4, 1, 5, 2, 6, 3, 7]

    def __init__(self, adc_channel, bus=0, device=0, samples=20):
        """Open a channel for SPI communication.

        Args:
            adc_channel: The ADC channel on the ADS8344 to read, [0, 7].

        """
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        if adc_channel < 0 or adc_channel > 7:
            raise ValueError("ADC channel must be in the range [0, 7].")
        self.adc_channel = adc_channel
        self.samples = samples

    def _read_adc(self):
        """Read the analog-to-digital converter pin, outputs [0, max)."""
        # Bits are S, A2, A1, A0, -, SGL, PD1, PD0. A2-0 come from bitmap,
        # all other bits are high. See datasheet for more.
        control = ((8 + self.bitmap[self.adc_channel]) << 4) + 7
        adc = self.spi.xfer2([control, 0, 0, 0])
        # The return value is offset by a bit. See datasheet for more.
        return (adc[1] << 9) + (adc[2] << 1) + (adc[3] >> 7)

    def read_voltage(self):
        """Read the ADC and converts to voltage, 0-3.3V."""
        return sum(self._read_adc() * (10.0 / 3.0) / (65536.0 * self.samples)
                   for _ in range(self.samples))

    def close(self):
        """Close the SPI connection."""
        self.spi.close()


class MAX31855(object):
    """Python driver for MAX38155 Thermocouple-to-Digital Converters.

    [Datasheet](http://datasheets.maximintegrated.com/en/ds/MAX31855
    .pdf).
    """

    def __init__(self, bus=0, device=0):
        """Initialize MAX31855 with SPI library."""
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)

    def get(self):
        """Return the thermocouple temperature, in Celsius."""
        return self.get_both()['thermocouple']

    def get_reference_junction(self):
        """Return the reference junction temperature, in Celsius."""
        return self.get_both()['reference junction']

    def get_both(self):
        """Return thermocouple and reference temperature, in Celsius."""
        return self._parse(self._read())

    def _read(self):
        """Read 32 bits from the SPI bus.

        Returns a list of 32 ints, corresponding to the 32 bits. This
        method flips the bits so index access corresponds to the manual
        (ie. index 0 is the least significant bit).
        """
        data = self.spi.readbytes(4)
        if data[3] is None or len(data) != 4:
            raise RuntimeError("Did not read expected number of bytes.")
        return [b >> j & 1 for b in data for j in range(7, -1, -1)][::-1]

    def _parse(self, bits):
        """Convert the binary array into relevant data.

        Return thermocouple temperature and reference junction temperature,
        and raise an error if error bits are flagged.

        The data format is specified in [the manual](http://datasheets.
        maximintegrated.com/en/ds/MAX31855.pdf), and can be summarized as:
            31: sign
            30-18: temperature, from 2^10 to 2^-2
            15: sign, reference junction
            14-4: temperature, reference junction, from 2^6 to 2^-4
            2-0: error indicators (short to vcc, short to gnd, open circuit)
        These bits are accessible by array indices.

        """
        if bits[0]:
            logger.debug("Open circuit detected.")
        if bits[1]:
            logger.debug("Short to ground detected.")
        if bits[2]:
            logger.debug("Short to high voltage detected.")
        rj = sum(b * 2 ** (i - 4) for i, b in enumerate(bits[4:15]))
        rj *= -1 if bits[15] else 1
        tc = sum(b * 2 ** (i - 2) for i, b in enumerate(bits[18:31]))
        tc *= -1 if bits[31] else 1
        tc = tc if -100 < tc < 1000 else None
        return {'thermocouple': tc, 'reference junction': rj}

    def close(self):
        """Close the SPI connection."""
        self.spi.close()


class MAX31856(object):
    """Python driver for MAX38156 Precision Thermocouple Converter.

    [Datasheet](https://datasheets.maximintegrated.com/en/ds/MAX31856.pdf).

    This driver returns the average of 16 reads, each with 19-bit accuracy.
    It sets the chip into auto-conversion mode to do so. Read the datasheet
    for more.
    """

    faults = ['Thermocouple Open-Circuit Fault',
              'Overvoltage or Undervoltage Input Fault',
              'Thermocouple Temperature Low Fault',
              'Thermocouple Temperature High Fault',
              'Cold-Junction Low Fault',
              'Cold-Junction High Fault',
              'Thermocouple Out-of-Range',
              'Cold Junction Out-of-Range']

    def __init__(self, bus=0, device=0):
        """Initialize MAX31856 with SPI library."""
        self.device = device
        self.active_faults = set()
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 7629
        self.spi.mode = 0b01
        self._config()

    def get(self):
        """Return the thermocouple temperature, in Celsius."""
        # Read three temperature bytes and one fault byte.
        # See pages 24-25 of datasheet for more.
        r = self.spi.xfer2([0x0c, 0x00, 0x00, 0x00, 0x00])
        self._faults(r[-1])
        bits = (((r[1] & 0x7f) << 16) + (r[2] << 8) + r[3]) >> 5
        tc = bits * 2.0 ** -7
        tc *= -1 if r[0] & 0x80 else 1
        tc = tc if -100 < tc < 1000 else None
        return tc

    def close(self):
        """Close the SPI connection."""
        self.spi.close()

    def _config(self):
        """Write config registers."""
        # Average 16 readings, K type. See page 20 of datasheet for more.
        self.spi.xfer2([0x81, 0b01110011])
        # Auto conversion. See page 19 of datasheet for more.
        self.spi.xfer2([0x80, 0b10000000])

    def _faults(self, fault_byte):
        """Log changes to faults.

        Compare current fault codes to previously recorded fault codes and
        log if new fault occured or if previously recorded fault got fixed.

        Args:
            fault_byte: Byte containing all fault bit status codes.

        """
        current_faults = {fault for i, fault in enumerate(self.faults)
                          if (fault_byte >> (7 - i)) & 1}
        if current_faults != self.active_faults:
            new = current_faults - self.active_faults
            cleared = self.active_faults - current_faults
            if new:
                logger.warning('New faults, thermocouple {}:\n{}'
                               .format(self.device, '\n'.join(new)))
                self.active_faults = self.active_faults | new
            if cleared:
                logger.warning('Cleared faults, thermocouple {}:\n{}'
                               .format(self.device, '\n'.join(cleared)))
            self.active_faults = current_faults


class MAX31865(object):
    """Python driver for MAX31865 Adafruit Breakout Board.

    [Product Page](https://www.adafruit.com/product/3328).

    This device reads RTDs with a ~0.03 degree resolution.
    """

    r_rtd = 100  # ohm, pt100
    r_ref = 430  # ohm, from Adafruit breakout
    faults = ['RTD High Threshold',
              'RTD Low Threshold',
              'REFIN- > 0.85 x V_BIAS',
              'REFIN- < 0.85 x V_BIAS (FORCE- Open)',
              'RTDIN- < 0.85 x V_BIAS (FORCE- Open)',
              'Overvoltage / undervoltage fault']

    def __init__(self, bus=0, device=0):
        """Initialize MAX31865 with SPI library."""
        self.device = device
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 7629
        self.spi.mode = 0b01

    def get(self):
        """Return the RTD temperature, in degrees Celsius."""
        # Step 1: Send config byte to trigger ADC. See manual for more.
        self.spi.xfer2([0x80, 0b10110010])
        time.sleep(0.075)
        # Step 2: Read data bytes (15-bit resistance, 1-bit fault indicator)
        _, msb, lsb = self.spi.xfer2([0x01, 0x00, 0x02])
        # Step 3: Check fault bit. Request more data if high.
        if lsb & 1:
            logger.debug('RTD fault on device {}.'.format(self.device))
            self._get_faults()
        # Step 4: Bits -> Resistance -> Temperature conversion
        adc = ((msb << 8) + lsb) >> 1
        r = float(adc * self.r_ref) / 32768
        return self._resistance_to_temperature(r)

    def _resistance_to_temperature(self, r):
        """Convert RTD resistance to temperature, in degrees C.

        This uses a quadratic relationship, which should provide a conversion
        accuracy tighter than the read error. If greater accuracy is desired,
        each RTD should be calibrated and this equation replaced with a lookup.
        """
        a, b = 3.90830e-3, -5.775e-7
        try:
            t = (-a + (a**2 - 4 * b * (1 - r / self.r_rtd))**0.5) / (2 * b)
        except ValueError:
            t = None
        return t

    def _get_faults(self):
        """Check fault status codes, logging any found."""
        status = self.spi.xfer2([0x07, 0x00])[1]
        for i, fault in enumerate(self.faults):
            if (status >> (7 - i)) & 1:
                logger.warning('{}, device {}.'.format(fault, self.device))

    def close(self):
        """Close the SPI connection."""
        self.spi.close()
