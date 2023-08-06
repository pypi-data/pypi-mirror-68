#!/usr/bin/python
"""
This file is part of PyMMB - The crossplatform MMB library and toolset
If you don't use MMC Flash cards in a BBC Microcomputer, this is unlikely
to be a lot of use to you!
"""

from ._version import get_versions
__version__ = get_versions()['version']

def fromBCD(bcd):
    """
    Convert a BCD byte to a decimal integer
    """
    return ((bcd >> 4) * 10) + (bcd & 15)

def toBCD(decimal):
    """
    Convert a decimal integer to a BCD byte
    """
    return (int(decimal / 10) << 4) + (decimal % 10)
