# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""utility functions"""

# stdlib imports
import datetime
import platform
# non-stdlib imports

# global defines
_IS_PLATFORM_WINDOWS = platform.system() == 'Windows'


def on_windows():
    # type: () -> bool
    """
    If system environment is Windows
    :return: True if the current platform is windows
    """
    return _IS_PLATFORM_WINDOWS


def distribution():
    # type: () -> str
    """
    Get the OS distribution
    :return: The OS distribution
    """
    dist = platform.system()
    if dist == 'Linux':
        dist = ' '.join(platform.linux_distribution())
    elif dist == 'Darwin':
        dist = ' '.join(platform.mac_ver())
    elif dist == 'Windows':
        dist = ' '.join(platform.win32_ver())
    return dist


def encode_utf8(value):
    # type: (str) -> str
    """
    Encodes a value as utf-8
    :param value: The value to encode
    :return: The encoded value
    """
    return str(value).encode('utf8')


def decode_utf8(value):
    # type: (str) -> str
    """
    Decodes a string encoded as utf-8
    :param value: The value to decode
    :return: The decoded value
    """
    return value.decode('utf8')


def encode_utf16le(value):
    # type: (str) -> str
    """
    Encodes a value as utf-16le (UCS-2)
    :param value: The value to encode
    :return: The encoded value
    """
    return str(value).encode('utf-16le')


def decode_utf16le(value):
    # type: (str) -> str
    """
    Decodes a string encoded as utf-16le (UCS-2)
    :param value: The value to decode
    :return: The decoded value
    """
    return value.decode('utf-16le')


def decode_hex(value):
    # type: (str) -> bytes
    """
    Decodes a string with hex encoding to bytes
    :param value: The value to decode
    :return: The decoded bytes
    """
    return bytes.fromhex(value)


def datetime_utcnow():
    # type: () -> datetime.datetime
    """
    Returns the current datetime with UTC timezone
    :return: The current datetime with UTC timezone
    """
    return datetime.datetime.utcnow()


