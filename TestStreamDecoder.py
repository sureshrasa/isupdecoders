import unittest
from StreamDecoder import *

from bitstring import BitArray
from io import BytesIO

class TestDecoder:
    def test1Bit(self):
        stream = self.fromBits("0b1101, 0b0101");
        self.assertTrue(stream.hasMore())
        self.assertEqual(stream.readField(1), 1)
        self.assertTrue(stream.hasMore())
        self.assertEqual(stream.readField(1), 0)
        self.assertTrue(stream.hasMore())
        self.assertEqual(stream.readField(1), 1)
        self.assertTrue(stream.hasMore())
        self.assertEqual(stream.readField(1), 0)
        self.assertTrue(stream.hasMore())
        self.assertEqual(stream.readField(1), 1)
        self.assertTrue(stream.hasMore())
        self.assertEqual(stream.readField(1), 0)
        self.assertTrue(stream.hasMore())
        self.assertEqual(stream.readField(1), 1)
        self.assertTrue(stream.hasMore())
        self.assertEqual(stream.readField(1), 1)
        self.assertFalse(stream.hasMore())

    def test4Bits(self):
        stream = self.fromBits("0xA, 0x3, 0x2, 0xE, 0x5, 0xC,");
        self.assertTrue(stream.hasMore())
        self.assertEqual(stream.readField(4), 0x3)
        self.assertTrue(stream.hasMore())
        self.assertEqual(stream.readField(4), 0xA)
        self.assertTrue(stream.hasMore())
        self.assertEqual(stream.readField(4), 0xE)
        self.assertTrue(stream.hasMore())
        self.assertEqual(stream.readField(4), 0x2)
        self.assertTrue(stream.hasMore())
        self.assertEqual(stream.readField(4), 0xC)
        self.assertTrue(stream.hasMore())
        self.assertEqual(stream.readField(4), 0x5)
        self.assertFalse(stream.hasMore())

    def test431Bits(self):
        stream = self.fromBits("0b1101, 0b0101");
        self.assertEqual(stream.readField(4), 0b0101)
        self.assertEqual(stream.readField(3), 0b101)
        self.assertEqual(stream.readField(1), 0b1)
        self.assertFalse(stream.hasMore())

    def testByte(self):
        stream = self.fromBits("0xAB, 0xCD, 0x01, 0x52");
        self.assertEqual(stream.readField(8), 0xAB)
        self.assertEqual(stream.readField(8), 0xCD)
        self.assertEqual(stream.readField(8), 0x01)
        self.assertEqual(stream.readField(8), 0x52)
        self.assertFalse(stream.hasMore())

    def testWordOnByteBoundary(self):
        stream = self.fromBits("0xAB, 0xCD, 0x01, 0x52");
        self.assertEqual(stream.readField(16), 0xCDAB)
        self.assertEqual(stream.readField(16), 0x5201)
        self.assertFalse(stream.hasMore())
  
    def testLongWordOnByteBoundary(self):
        stream = self.fromBits("0xABCD0152, 0x89ABCDEF");
        self.assertEqual(stream.readField(32), 0x5201CDAB)
        self.assertEqual(stream.readField(32), 0xEFCDAB89)
        self.assertFalse(stream.hasMore())
      
    def testWordAcrossByteBoundary(self):
        stream = self.fromBits("0b110001, 0b10, 0b00010100, 0b00101010, 0b11, 0b100101");
        self.assertEqual(stream.readField(2),  0b10)
        self.assertEqual(stream.readField(14), 0b00010100110001)
        self.assertEqual(stream.readField(14), 0b10010100101010)
        self.assertEqual(stream.readField(2),  0b11)
        self.assertFalse(stream.hasMore())

    def testSkipBytesOnByteBoundary(self):
        stream = self.fromBits("0x0123456789ABCDEF")
        self.assertTrue(stream.hasMore())
        stream.skipBytes(0)
        stream.skipBytes(3)
        self.assertTrue(stream.hasMore())
        self.assertEqual(stream.readField(8), 0x67)
        stream.skipBytes(2)
        self.assertEqual(stream.readField(8), 0xCD)
        stream.skipBytes(1)
        self.assertFalse(stream.hasMore())
        stream.skipBytes(0)

    def testSkipBytesAcrossByteBoundaryThrows(self):
        stream = self.fromBits("0x0123456789ABCDEF")
        self.assertTrue(stream.hasMore())
        stream.skipBytes(3)
        stream.skipBytes(0)
        self.assertTrue(stream.hasMore())
        self.assertEqual(stream.readField(4), 0x7)
        self.assertRaises(Exception, stream.skipBytes, 2)

    def testReadBytesOnByteBoundaryOnSingleBuffer(self):
        stream = self.fromBits("0x0123456789ABCDEF")
        self.assertTrue(stream.hasMore())
        stream.skipBytes(3)
        self.assertTrue(stream.hasMore())
        self.assertEqual(stream.readBytes(4), bytes.fromhex("6789ABCD"))
        self.assertEqual(stream.readBytes(1), bytes.fromhex("EF"))
        self.assertFalse(stream.hasMore())

    def testReadBytesOnByteBoundaryOnMultipleBuffers(self):
        stream = self.fromBits("0x0123456789ABCDEF", bufferSize=2)
        self.assertTrue(stream.hasMore())
        stream.skipBytes(3)
        self.assertTrue(stream.hasMore())
        self.assertEqual(stream.readBytes(4), bytes.fromhex("6789ABCD"))
        self.assertEqual(stream.readBytes(1), bytes.fromhex("EF"))
        self.assertFalse(stream.hasMore())

class TestStreamDecoder(TestDecoder, unittest.TestCase):
    def fromBits(self, bitString, bufferSize=StreamDecoder.BUFFER_SIZE):
        return StreamDecoder(BytesIO(bytes.fromhex(BitArray(bitString).hex)), bufferSize=bufferSize)

class TestStreamDecoderSlice(TestDecoder, unittest.TestCase):
    def fromBits(self, bitString, bufferSize=StreamDecoder.BUFFER_SIZE):
        data = bytes.fromhex(BitArray(bitString + ", 0x1234").hex)
        return StreamDecoderSlice(StreamDecoder(BytesIO(data), bufferSize=bufferSize), len(data) - 2)

if __name__ == '__main__':
    unittest.main()
