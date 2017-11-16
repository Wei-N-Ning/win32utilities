
import itertools
import os
import marshal
import re
import StringIO
import types
import zipfile
import zlib
import pwd


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


def package_to_buf(dir_path, key_=0x13):
    """
    If dir_path is /x/y/z
    the top-level directory in the zip archive will be z
    so that /x/y/z/onefile.ext becomes z/onefile.ext

    Args:
        dir_path:
        key_:

    Returns:
        str
    """
    dir_path = re.sub('/+$', '', dir_path)
    si = StringIO.StringIO()
    ziph = zipfile.ZipFile(si, 'w', zipfile.ZIP_DEFLATED, False)
    for root, dirs, files in os.walk(dir_path):
        for f in itertools.chain(dirs, files):
            full_path = os.path.join(root, f)
            rel_path = full_path.replace(dir_path, '')
            ziph.write(full_path, arcname=rel_path)
    ziph.close()
    cbuf = _caesar(si.getvalue(), key_, encode=True)
    return cbuf


def buf_to_package(cbuf, file_path, key_=0x13):
    buf = _caesar(cbuf, key_, encode=False)
    with open(file_path, 'wb') as fp:
        fp.write(buf)

