from ByteStream import *

class Parameter:
    def __init__(self, decoder):
        self._code = decoder.readField(8)
        self._length = decoder.readField(8)

    @property
    def code(self):
        return self._code

    @property
    def length(self):
        return self._length
