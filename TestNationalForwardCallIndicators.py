import unittest
from NationalForwardCallIndicators import *
from ByteStream import *

class TestNationalForwardCallIndicators(unittest.TestCase):

    def testCode(self):
        self.assertEqual(NationalForwardCallIndicators(ByteStream("fe020300")).code, 0xFE)

    def testLength(self):
        self.assertEqual(NationalForwardCallIndicators(ByteStream("fe020300")).length, 0x2)

    def testCliBlocking(self):
        self.assertFalse(NationalForwardCallIndicators(ByteStream("fe020000")).isCliBlocking)
        self.assertTrue(NationalForwardCallIndicators(ByteStream("fe02A000")).isCliBlocking)

    def testNetworkTranslatedAddress(self):
        self.assertFalse(NationalForwardCallIndicators(ByteStream("fe020000")).isNetworkTranslatedAddress)
        self.assertTrue(NationalForwardCallIndicators(ByteStream("fe028000")).isNetworkTranslatedAddress)

    def testPriorityAccess(self):
        self.assertFalse(NationalForwardCallIndicators(ByteStream("fe020000")).isPriorityAccess)
        self.assertTrue(NationalForwardCallIndicators(ByteStream("fe024000")).isPriorityAccess)

    def testProtection(self):
        self.assertFalse(NationalForwardCallIndicators(ByteStream("fe020000")).isProtection)
        self.assertTrue(NationalForwardCallIndicators(ByteStream("fe022000")).isProtection)

if __name__ == '__main__':
    unittest.main()
