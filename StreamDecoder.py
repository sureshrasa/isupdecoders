#
#  Author(s): Suresh Rasakulasuriar
#
#  Copyright: © Resilientplc.com Ltd. 2018 - All Rights Reserved
#

from bitstring import BitArray

class StreamDecoder:

    def __init__(self, payload):
        self._payload = payload
        self._currByteIndex = 0
        self._currBitIndex = 0 
        self._currBits = payload[0] 
        self._prevLen = 0     

    def readField(self, length):
        if (self._currBitIndex == 8):
            if (self._currByteIndex >= len(self._payload)):
                raise Exception("Stream reached eof", self._currByteIndexIndex)

            self._currBitIndex = 0
            self._currByteIndex +=1
            self._currBits = self._payload[self._currByteIndex]
        else:
           self._currBits = self._currBits >> self._prevLen

        if (self._currBitIndex+length > 8):
            raise Exception("Field crosses byte boundary", self._currByteIndex, self._currBitIndex, length)

        assert(length > 0)

        result = self._currBits & ((1 << length) - 1)
        #print("Read field: payload=", self._payload[self._currByteIndex], " nextBit=", self._currBitIndex, " nextByte=", self._currByteIndex, " result=", result)

        self._currBitIndex += length
        self._prevLen = length
 
        return result;

    def fromBits(bitString):
        return StreamDecoder(bytes.fromhex(BitArray(bitString).hex))
