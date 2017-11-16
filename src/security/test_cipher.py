
import os
import unittest
import zipimport

import cipher


def sut():
    import json
    return json.dumps([2, {'a': 0}, {'b': 1}])


def file_path(file_name):
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), file_name)
    )


class TestCipherFunction(unittest.TestCase):

    def test_roundTrip(self):
        buf = cipher.cipher(sut, key_=0x19)
        f = cipher.decipher(buf, key_=0x19)
        result = f()
        self.assertTrue(result)


class TestPackageToBuffer(unittest.TestCase):

    def test_roundTrip(self):
        cbuf = cipher.package_to_buf(file_path('testdata'))
        p = '/tmp/testdata.zip'
        cipher.buf_to_package(cbuf, p)
        imp = zipimport.zipimporter(p)
        self.assertTrue(imp.load_module('dd'))
        self.assertTrue(imp.load_module('dd/components'))
        self.assertTrue(imp.load_module('dd/components/xlib'))

