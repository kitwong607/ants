"""
Copyright (C) 2018 Interactive Brokers LLC. All rights reserved. This code is subject to the terms
and conditions of the IB API Non-Commercial License or the IB API Commercial License, as applicable.
"""

"""
This module has tools for implementing the IB low level messaging.
"""

import struct
import logging
import json


# I use this just to visually emphasize it's a wrapper overriden method
def iswrapper(fn):
    return fn

def make_msg(text) -> bytes:
    """ adds the length prefix """
    msg = struct.pack("!I%ds" % len(text), len(text), str.encode(text))
    return msg


def read_msg(buf: bytes) -> tuple:
    """ first the size prefix and then the corresponding msg payload """
    if len(buf) < 4:
        return (0, "", buf)
    size = struct.unpack("!I", buf[0:4])[0]
    logging.debug("read_msg: size: %d", size)
    if len(buf) - 4 >= size:
        text = struct.unpack("!%ds" % size, buf[4:4 + size])[0]
        return (size, text, buf[4 + size:])
    else:
        return (size, "", buf)


def read_fields(buf: bytes) -> tuple:
    """ msg payload is made of fields terminated/separated by NULL chars """
    fields = buf.split(b"\0")

    return tuple(fields[0:-1])  # last one is empty; this may slow dow things though, TODO


def send_msg(conn, d):
    try:
        serialized = json.dumps(d)

    except (TypeError, ValueError) as e:
        raise Exception('You can only send JSON-serializable data')
    msg = make_msg(serialized)
    conn.send(msg)
