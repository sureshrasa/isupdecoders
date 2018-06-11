from ByteStream import *

class IsupMessage:
    SIZE = 3

    def __init__(self, decoder):
        cic_lsb = decoder.readField(8)
        cic_msb = decoder.readField(4)
        decoder.readField(4)
        self._cic = cic_msb<<8 | cic_lsb
        self._code = decoder.readField(8)

    def __str__(self):
        return "IsupMessage[cic:{0}, code:{1}]".format(self.cic, self.code)                

    @property
    def cic(self):
        return self._cic

    @property
    def code(self):
        return self._code
