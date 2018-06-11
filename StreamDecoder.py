#
#  Author(s): Suresh Rasakulasuriar
#
#  Copyright: © Resilientplc.com Ltd. 2018 - All Rights Reserved
#
class StreamDecoder:
    PAYLOAD_SIZE = 128

    def __init__(self, stream):
        self._stream = stream
        self._fillPayload()
        self._prevLen = 0 

    def _fillPayload(self):
        self._payload = self._stream.read(StreamDecoder.PAYLOAD_SIZE)
        self._currByteIndex = 0
        self._currBitIndex = 0 
        if len(self._payload) > 0:
            self._currBits = self._payload[0] 

    def _readField(self, length):
        if not self.hasMore():
            raise Exception("Stream reached end")

        if (self._currBitIndex == 8):
            self._currBitIndex = 0
            self._currByteIndex +=1
            self._currBits = self._payload[self._currByteIndex]
        else:
           self._currBits = self._currBits >> self._prevLen

        assert (self._currBitIndex+length <= 8)
        assert(length > 0)

        result = self._currBits & ((1 << length) - 1)
        #print("Read field: payload=", self._payload[self._currByteIndex], " nextBit=", self._currBitIndex, " nextByte=", self._currByteIndex, " result=", result)

        self._currBitIndex += length
        self._prevLen = length
 
        return result;

    def hasMore(self):
        if self._currBitIndex < 8 or self._currByteIndex < (len(self._payload)-1):
            return True

        self._fillPayload()

        return len(self._payload) > 0

    def readField(self, length):
        if length <= self._currBitIndex:
            return self._readField(length)

        result = 0
        lsbLen = 0
        
        bitsLeft = 8 - self._currBitIndex
        if (bitsLeft > 0) and (length > bitsLeft):
            #print("Reading bits; len=", bitsLeft)
            result = self._readField(bitsLeft)
            length -= bitsLeft
            lsbLen = bitsLeft

        while length > 8:
            #print("Reading bytes; len=", length)
            result += self._readField(8)<<lsbLen
            length -= 8
            lsbLen += 8

        if length > 0:
            #print("Reading last bits; len=", length)
            result += self._readField(length)<<lsbLen

        return result

class StreamDecoderSlice:
    def __init__(self, stream, size):
        self._stream = stream
        self._bitLen = size * 8

    def skipBytes(self, len):
        self._stream.skipBytes(len)
        self._bitLen -= len * 8

    def readField(self, length):
        if (self._bitLen < length):
            raise Exception("Stream reached eof", self._bitLen, length)

        result = self._stream.readField(length)
        self._bitLen -= length

        return result

    def hasMore(self):
        return self._bitLen > 0

