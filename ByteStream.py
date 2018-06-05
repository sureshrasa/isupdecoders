from io import BytesIO

class ByteStream:
    def __init__(self, payLoad):
        self._stream = BytesIO(bytes.fromhex(payLoad))

    def readByte(self):
        return self._stream.read(1)[0]
