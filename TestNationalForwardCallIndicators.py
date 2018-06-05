import unittest
from NationalForwardCallIndicators import *
from StreamDecoder import *

class TestNationalForwardCallIndicators(unittest.TestCase):

    def testCode(self):
        self.assertEqual(NationalForwardCallIndicators(StreamDecoder.fromBits("0xfe020300")).code, 0xFE)

    def testLength(self):
        self.assertEqual(NationalForwardCallIndicators(StreamDecoder.fromBits("0xfe020300")).length, 0x2)

    def testCliBlocking(self):
        self.assertFalse(NationalForwardCallIndicators(StreamDecoder.fromBits("0xfe02, 0b0000, 0b0000, 0x00")).isCliBlocking)
        self.assertTrue(NationalForwardCallIndicators(StreamDecoder.fromBits("0xfe02, 0b0000, 0b0001, 0x00")).isCliBlocking)

    def testNetworkTranslatedAddress(self):
        self.assertFalse(NationalForwardCallIndicators(StreamDecoder.fromBits("0xfe02, 0b0000, 0b0000, 0x00")).isNetworkTranslatedAddress)
        self.assertTrue(NationalForwardCallIndicators(StreamDecoder.fromBits("0xfe02, 0b0000, 0b0010, 0x00")).isNetworkTranslatedAddress)

    def testPriorityAccess(self):
        self.assertFalse(NationalForwardCallIndicators(StreamDecoder.fromBits("0xfe02, 0b0000, 0b0000, 0x00")).isPriorityAccess)
        self.assertTrue(NationalForwardCallIndicators(StreamDecoder.fromBits("0xfe02, 0b0000, 0b0100, 0x00")).isPriorityAccess)

    def testProtection(self):
        self.assertFalse(NationalForwardCallIndicators(StreamDecoder.fromBits("0xfe02, 0b0000, 0b0000, 0x00")).isProtection)
        self.assertTrue(NationalForwardCallIndicators(StreamDecoder.fromBits("0xfe02, 0b0000, 0b1000, 0x00")).isProtection)

if __name__ == '__main__':
    unittest.main()
