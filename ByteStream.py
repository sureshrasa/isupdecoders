from io import BytesIO
from bitstring import BitArray

class ByteStream:
    def __init__(self, payLoad):
        self._stream = BytesIO(bytes.fromhex(payLoad))

    def readByte(self):
        return self._stream.read(1)[0]

    def fromBits(bitString):
        return ByteStream(BitArray(bitString).hex)
