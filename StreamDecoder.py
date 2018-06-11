#
#  Author(s): Suresh Rasakulasuriar
#
#  Copyright: © Resilientplc.com Ltd. 2018 - All Rights Reserved
#
class StreamDecoder:
    BUFFER_SIZE = 128

    def __init__(self, stream, bufferSize = BUFFER_SIZE):
        self._stream = stream
        self._bufferSize = bufferSize
        self._fillPayload()

    def _fillPayload(self):
        self._payload = self._stream.read(self._bufferSize)
        self._currByteIndex = -1
        self._currBitIndex = 8 

    def _checkHasMore(self):
        if not self.hasMore():
            raise Exception("Stream reached end")

    def _fillBitBuffer(self):
        self._checkHasMore()
        if (self._currBitIndex == 8):
            self._currBitIndex = 0
            self._currByteIndex +=1
            self._currBits = self._payload[self._currByteIndex]

    def _readBitField(self, length):
        self._fillBitBuffer()

        assert (self._currBitIndex+length <= 8)
        assert(length > 0)

        result = self._currBits & ((1 << length) - 1)

        self._currBitIndex += length
        self._currBits >>= length
 
        return result;

    def hasMore(self):
        if self._currBitIndex < 8:
            return True

        if self._currByteIndex+1 < len(self._payload):
            return True

        self._fillPayload()

        return len(self._payload) > 0

    def readField(self, length):
        self._fillBitBuffer()

        bitsLeft = 8 - self._currBitIndex
        if length <= bitsLeft:
            return self._readBitField(length)

        result = 0
        lsbLen = 0
        
        if (bitsLeft > 0):
            result = self._readBitField(bitsLeft)
            length -= bitsLeft
            lsbLen = bitsLeft

        while length > 8:
            result += self._readBitField(8)<<lsbLen
            length -= 8
            lsbLen += 8

        if length > 0:
            result += self._readBitField(length)<<lsbLen

        return result

    def _checkByteBoundary(self):
        if self._currBitIndex%8 != 0:
            raise Exception("Cannot skip bytes on non byte boundary")

    def skipBytes(self, length):
        if length > 0:
            self.readBytes(length)  

    def readBytes(self, length):
        self._fillBitBuffer()
        self._checkByteBoundary()

        assert(self._currBitIndex == 0)

        result = bytearray()
        totalLeftToRead = length

        bytesLeft = len(self._payload) - self._currByteIndex
        assert(bytesLeft > 0)
        xfrLen = min(totalLeftToRead, bytesLeft)
        result += self._payload[self._currByteIndex:self._currByteIndex+xfrLen]
        totalLeftToRead -= xfrLen
        self._currByteIndex += xfrLen-1
        self._currBitIndex = 8

        if totalLeftToRead > 0:
            result += self._stream.read(totalLeftToRead)

        if len(result) != length:
            raise Exception("Reached end of stream whilst reading bytes length={0}, result len={1}".format(length, len(result)))

        return result
        

class StreamDecoderSlice:
    def __init__(self, stream, size):
        self._stream = stream
        self._bitLen = size * 8

    def skipBytes(self, length):
        self._stream.skipBytes(length)
        self._bitLen -= length * 8

    def readField(self, length):
        if (self._bitLen < length):
            raise Exception("Stream slice reached end", self._bitLen, length)

        result = self._stream.readField(length)
        self._bitLen -= length

        return result

    def readBytes(self, length):
        result = self._stream.readBytes(length)
        self._bitLen -= length * 8
        return result

    def hasMore(self):
        return self._bitLen > 0

