from ByteStream import *

class Parameter:
    def __init__(self, decoder):
        self._code = decoder.readField(8)

    @property
    def code(self):
        return self._code
