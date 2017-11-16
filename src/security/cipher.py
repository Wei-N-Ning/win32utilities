
import itertools
import os
import marshal
import re
import StringIO
import shutil
import types
import zipfile
import subprocess
import shlex
import zlib


def _caesar(s, key_, encode=True):
    """

    Args:
        s (str):
        key_ (int):
        encode (bool): True if encoding; False if decoding

    Returns:
        str
    """

    def _c(_):
        return chr((ord(_) + key_) % 256)

    def c_(_):
        return chr((ord(_) - key_) % 256)

    if encode:
        return ''.join(map(_c, s))
    else:
        return ''.join(map(c_, s))


def cipher(func, key_=0x13):
    """
    Given a function object, serialize it (marshal) to string then:
     - compress them using zlib string compression
     - run caesar cipher on the resulting string with the given key

    Args:
        func: a python function
        key_ (int): to be passed to caesar cipher function

    Returns:
        str:
    """

    return _caesar(zlib.compress(marshal.dumps(func.func_code)), key_, encode=True)


def decipher(s, key_=0x13):
    """
    The inverse of cipher()

    Args:
        s (str):
        key_ (int):

    Returns:
        a function object
    """

    return types.FunctionType(marshal.loads(zlib.decompress(_caesar(s, key_, encode=False))), globals(), '_f')
