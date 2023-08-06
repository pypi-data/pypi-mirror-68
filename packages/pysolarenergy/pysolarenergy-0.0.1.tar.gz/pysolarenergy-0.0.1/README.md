# Python SolarEnergy®
![Continuous Integration](https://github.com/hallenmaia/python-solarenergy/workflows/Continuous%20Integration/badge.svg)
![Upload Python Package](https://github.com/hallenmaia/python-solarenergy/workflows/Upload%20Python%20Package/badge.svg)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/hallenmaia/python-solarenergy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Asynchronous Python client for [SolarEnergy®](http://www.solarenergy.com.br) inverters.

## About

This package allows you to monitor [SolarEnergy®](http://www.solarenergy.com.br) inverters programmatically:

* Equipment serial, model and general info
* Temperature and inverter health
* Real time power, current and voltage
* Grid power information
* Daily/Total energy summaries
* Network summary

## Install

```bash
pip install pysolarenergy
```

## Quick Start

```python
import asyncio
from pysolarenergy import SolarEnergyInverter


async def main():
    """Show example of connecting to your inverter."""
    async with SolarEnergyInverter(host='192.168.1.22') as inverter:
        info = await inverter.get_info()
        print(info)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

## Documentation

### Methods

`get_info()`

`get_real_time_data()`

`get_network()`

## Confirmed Supported Inverters

These inverters have been tested and confirmed to be working.  

* SE-TL2K

If your inverter is not listed above, this library may still work. Please create an issue so we can add your inverter to the list 😊.

## Disclaimer

The code was developed as a way of integrating personally owned [SolarEnergy®](http://www.solarenergy.com.br) inverters, and it cannot be used for other purposes. It is not affiliated with any company and it doesn't have have commercial intent.

The code is provided AS IS and the developers will not be held responsible for failures in the inverter, or any other malfunction.

[SolarEnergy®](http://www.solarenergy.com.br) is a registered mark. Other brands are owned by their respective owners.