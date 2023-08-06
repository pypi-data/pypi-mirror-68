# NuMat Chips
Python drivers for circuit board components. Intended for use with Raspberry Pis.

![](https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSIFf44ELHVCqy6wDeoCrO9F7SweDes8oq7_lbykvrM-KOkpv0P&usqp=CAU)

# Why?

Many of the components supported here come with drivers. However, their code quality is mixed and many important chipset features can be missing or misconfigured. It's your chip and you should be able to use all of it.

These drivers were built ground up from the appropriate datasheets, making sure that all useful features are exposed or set to sensible defaults. The code is concise and linted, and this library works as a dependency.

# Supported Chips

 * ADS1115
 * ADS8344
 * MAX31855
 * MAX31856
 * MAX31865
 * MCP3008
 * MCP3202
 * MCP3208

# Installation

```
pip install numat-chips
```

# Usage

For testing, you can call directly.

```python
import chips
adc = chips.ADS1115(channel=0)
print(adc.read_voltage())
```

For production, consider subclassing to provide space to document the circuit
and improve code reusability.

```python
class PiraniGauge(MCP3202):
    """Reads from an Edwards APG100 vacuum pressure transmitter.

    The gauge is a 0-10V signal, split into a 0-3.3V range by three 10-kiloohm
    resistors.
    """
    def get(self):
        """Returns the pressure reading, in torr."""
        return 10 ** (3 * self.read_voltage() - 6.125)
```
