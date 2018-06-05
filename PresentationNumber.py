from Parameter import *
from ByteStream import *

class PresentationNumber(Parameter):
    def __init__(self, stream):
        super(PresentationNumber, self).__init__(stream)
        
        byte = stream.readByte()
        self._natureOfAddress = byte >> 1
        self._isOddAddressSignals = byte & 0x1

        byte = stream.readByte()
        self._screeningIndicator = byte >> 6
        self._addressPresentationRestricted = (byte >> 4) & 0x3

    @property
    def code(self):
        return self._code

    @property
    def length(self):
        return self._length

    @property
    def natureOfAddress(self):
        return self._natureOfAddress

    @property
    def isOddAddressSignals(self):
        return self._isOddAddressSignals

    @property
    def screeningIndicator(self):
        return self._screeningIndicator

    @property
    def addressPresentationRestricted(self):
        return self._addressPresentationRestricted

