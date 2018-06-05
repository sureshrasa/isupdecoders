import unittest
from PresentationNumber import *
from StreamDecoder import *
from bitstring import BitArray

class TestPresentationNumber(unittest.TestCase):

    def testCode(self):
        self.assertEqual(PresentationNumber(StreamDecoder.fromBits("0xfd0d123456789a")).code, 0xFD)

    def testLength(self):
        self.assertEqual(PresentationNumber(StreamDecoder.fromBits("0xfd0d123456789a")).length, 0xd)

    def testNatureOfAddress(self):
        self.assertEqual(PresentationNumber(StreamDecoder.fromBits("0xfd0d, 0b1, 0b1010001, 0x12345678")).natureOfAddress, 0b1010001)

    def testOddAddressSignals(self):
        self.assertFalse(PresentationNumber(StreamDecoder.fromBits("0xfd0d, 0b0, 0b1010001, 0x12345678")).isOddAddressSignals)
        self.assertTrue(PresentationNumber(StreamDecoder.fromBits("0xfd0d, 0b1, 0b1010001, 0x12345678")).isOddAddressSignals)

    def testScreeningIndicator(self):
        self.assertEqual(PresentationNumber(StreamDecoder.fromBits("0xfd0da3, 0b00, 0b11, 0x1234567")).screeningIndicator, 0b11)
        self.assertEqual(PresentationNumber(StreamDecoder.fromBits("0xfd0da3, 0b00, 0b10, 0x1234567")).screeningIndicator, 0b10)
        self.assertEqual(PresentationNumber(StreamDecoder.fromBits("0xfd0da3, 0b00, 0b00, 0x1234567")).screeningIndicator, 0b0)

    def testAddressPresentationRestricted(self):
        self.assertEqual(PresentationNumber(StreamDecoder.fromBits("0xfd0da3, 0b11, 0b10, 0x1234567")).addressPresentationRestricted, 0b11)
        self.assertEqual(PresentationNumber(StreamDecoder.fromBits("0xfd0da3, 0b10, 0b11, 0x1234567")).addressPresentationRestricted, 0b10)
        self.assertEqual(PresentationNumber(StreamDecoder.fromBits("0xfd0da3, 0b00, 0b11, 0x1234567")).addressPresentationRestricted, 0b00)

if __name__ == '__main__':
    unittest.main()
