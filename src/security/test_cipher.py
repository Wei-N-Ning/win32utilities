
import os
import unittest

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
