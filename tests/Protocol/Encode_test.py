import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from wrapper.Protocol.Encode import *
class TestEncode(unittest.TestCase):
    def test_UINT8(self):
        self.assertEqual(encodeUINT8(255), bytearray(b"\xFF"))
        self.assertEqual(encodeUINT8(256), False)
        self.assertEqual(encodeUINT8(135), bytearray(b"\x87"))
    def test_UINT16(self):
        self.assertEqual(encodeUINT16(65537), False)
        self.assertEqual(encodeUINT16(65535), bytearray(b"\xFF\xFF"))
        self.assertEqual(encodeUINT16(48002), bytearray(b"\x82\xBB"))
    def test_CRC(self):
        self.assertEqual(packetCRC(200, b'\xdc\x05\xdc\x05\xdc\x05\xdc\x05\xdc\x05\xdc\x05\xdc\x05\xdc\x05'), b'\xd8')
        self.assertEqual(packetCRC(200, b'\xdc\x05\xdc\x05\xdc\x05\xdc\x05\xdc\x05\x7c\x05\xdc\x05\xdc\x05'), b'\x78')
        

if __name__=='__main__':
	unittest.main()