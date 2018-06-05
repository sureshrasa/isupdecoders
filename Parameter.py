from ByteStream import *

class Parameter:
    def __init__(self, stream):
        self._code = stream.readByte()
        self._length = stream.readByte()

    @property
    def code(self):
        return self._code

    @property
    def length(self):
        return self._length
