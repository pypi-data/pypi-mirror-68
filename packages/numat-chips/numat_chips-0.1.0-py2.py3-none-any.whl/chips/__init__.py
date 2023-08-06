"""
Drivers for various chips used at NuMat with Raspberry Pis.

Distributed under the GNU General Public License v3
Copyright (C) 2020 NuMat Technologies
"""
from chips.smbus import *
from chips.spi import *


def command_line():
    """Command-line tool for Productivity PLC communication."""
    import argparse
    import inspect
    import sys

    argparse.ArgumentParser(description="Get supported chips.")
    classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    print('\n'.join([c[0] for c in classes]))


if __name__ == '__main__':
    command_line()
