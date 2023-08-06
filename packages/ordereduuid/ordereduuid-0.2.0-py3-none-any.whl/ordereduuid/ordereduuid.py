"""Generate secure UUIDs ordered by time created."""
# Author: Jaron S. C. Powser

# Standard Library Imports
import os
import secrets
import time
import uuid
from datetime import datetime, timezone


# Time offset used by Python uuid module
# See https://github.com/python/cpython/blob/3.8/Lib/uuid.py
#     function uuid1()
_TIME_OFFSET = 0x1b21dd213814000

_MAC_BITS = 48
_MAX_MAC_VALUE = 0xffffffffffff
_MULTICAST_MAC_MASK = 0x10000000000

_CLOCK_SEQ_AND_VARIANT_BITS = 16


class OrderedUUID(uuid.UUID):
    _last_timestamp = 0

    def __init__(self, clock_seq=None, private_mac=True):
        time_and_version = _get_timestamp()

        # OR clock sequence bits to indicate RESERVED_FUTURE variant
        # See https://github.com/python/cpython/blob/3.8/Lib/uuid.py
        #     RESERVED_FUTURE string definition
        if clock_seq is None:
            clock_seq_and_variant = (
                secrets.randbits(_CLOCK_SEQ_AND_VARIANT_BITS) | 0xE000
            )
        else:
            clock_seq_and_variant = clock_seq | 0xE000

        if private_mac:
            node = secrets.randbits(_MAC_BITS) | _MULTICAST_MAC_MASK
        else:
            node = uuid.getnode()

        uuid_int = (
            (time_and_version << 64)
            + (clock_seq_and_variant << 48)
            + node
        )
        super(OrderedUUID, self).__init__(int=uuid_int)

    @property
    def time_low(self):
        return NotImplemented

    @property
    def time_mid(self):
        return NotImplemented

    @property
    def time_hi_version(self):
        return NotImplemented

    @property
    def version(self):
        return (self.int >> 64) & 0xf

    @property 
    def asctime_local(self):
        return time.asctime(time.localtime(self.time_seconds))

    @property 
    def asctime_utc(self):
        return time.asctime(time.gmtime(self.time_seconds))

    @property
    def ctime(self):
        return time.ctime(self.time_seconds)

    @property
    def datetime(self, tz=None):
        """Return either a naive datetime or one in tz."""
        return datetime.fromtimestamp(self.time_seconds, tz)

    @property
    def datetime_utc(self):
        """Return a timezone-aware datetime object in UTC."""
        return datetime.fromtimestamp(self.time_seconds, timezone.utc)

    @property
    def time_micros(self):
        return ((self.int >> 68) - _TIME_OFFSET) // 10

    @property
    def time_millis(self):
        return ((self.int >> 68) - _TIME_OFFSET) // 10000

    @property
    def time_nanos(self):
        return ((self.int >> 68) - _TIME_OFFSET) * 100

    @property
    def time_precise(self):
        return (self.int >> 68) - _TIME_OFFSET

    @property
    def time_seconds(self):
        return ((self.int >> 68) - _TIME_OFFSET) // 10000000


def _get_timestamp():
    """Generate a timestamp for use with an OrderedUUID."""
    timestamp = (time.time_ns() // 100) + _TIME_OFFSET
    if timestamp <= OrderedUUID._last_timestamp:
        timestamp = timestamp + 1

    OrderedUUID._last_timestamp = timestamp

    # Use max value as version number to indicate nonstandard
    time_and_version_int = (timestamp << 4) + 0xf
    return time_and_version_int

