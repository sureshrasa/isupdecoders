from ByteStream import *

class IsupMessage:
    def __init__(self, decoder):
        cic_lsb = decoder.readField(8)
        cic_msb = decoder.readField(4)
        decoder.readField(4)
        self._cic = cic_msb<<8 | cic_lsb
        self._code = decoder.readField(8)

    @property
    def cic(self):
        return self._cic

    @property
    def code(self):
        return self._code
