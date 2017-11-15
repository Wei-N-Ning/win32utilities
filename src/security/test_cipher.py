
import cipher

import unittest


def sut():
    import json
    return json.dumps([2, {'a': 0}, {'b': 1}])


class TestCipherFunction(unittest.TestCase):

    def test_roundTrip(self):
        buf = cipher.cipher(sut, key_=0x19)
        f = cipher.decipher(buf, key_=0x19)
        result = f()
        self.assertTrue(result)

