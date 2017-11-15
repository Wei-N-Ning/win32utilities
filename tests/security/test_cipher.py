
import os
import marshal
import re
import unittest
import types


def file_path(file_name):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), file_name))


def cipher(c):
    return chr((ord(c) + 0x13) % 256)


def decipher(c):
    return chr((ord(c) - 0x13) % 256)


class TestExtendedCaesarCipher(unittest.TestCase):

    def test_decipherSpecialToken(self):
        self.assertEqual('L  \xf4LL...', re.sub('[\xf0\xf1\xf2]', 'L', '\xf0  \xf4\xf1\xf2...'))

    def test_cipherFunctionsRoundTrip_singleCharacter(self):
        char = 's'
        self.assertEqual(char, decipher(cipher(char)))

    def test_cipherFunctionsRoundTrip_binaryFile(self):
        p = file_path('testfile.byte')
        with open(p, 'rb') as fp:
            orig = fp.read()
        new_ = ''.join(cipher(_) for _ in orig)
        restored_ = ''.join(decipher(_) for _ in new_)
        self.assertEqual(orig, restored_)

    def test_serializeCipherFunctions(self):
        _ = lambda(__): chr((ord(__) + 0x13) % 256)
        _buf = marshal.dumps(_.func_code)

    def test_deserializeCipherFunctions(self):
        _buf = '\x63\x01\x00\x00\x00\x01\x00\x00\x00\x03\x00\x00\x00\x43\x00\x00\x00\x73\x18\x00\x00\x00\x74\x00\x00' \
               '\x74\x01\x00\x7c\x00\x00\x83\x01\x00\x64\x01\x00\x17\x64\x02\x00\x16\x83\x01\x00\x53\x28\x03\x00\x00' \
               '\x00\x4e\x69\x13\x00\x00\x00\x69\x00\x01\x00\x00\x28\x02\x00\x00\x00\x74\x03\x00\x00\x00\x63\x68\x72' \
               '\x74\x03\x00\x00\x00\x6f\x72\x64\x28\x01\x00\x00\x00\x74\x02\x00\x00\x00\x5f\x5f\x28\x00\x00\x00\x00' \
               '\x28\x00\x00\x00\x00\x73\x07\x00\x00\x00\x3c\x73\x74\x64\x69\x6e\x3e\x74\x08\x00\x00\x00\x3c\x6c\x61' \
               '\x6d\x62\x64\x61\x3e\x01\x00\x00\x00\x73\x00\x00\x00\x00'
        f = types.FunctionType(marshal.loads(_buf), globals(), '___')
        print f('a')


if __name__ == '__main__':
    unittest.main()
