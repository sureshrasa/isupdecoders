from Parameter import *
from ByteStream import *

class PresentationNumber(Parameter):
    def __init__(self, decoder):
        super(PresentationNumber, self).__init__(decoder)
        
        self._natureOfAddress = decoder.readField(7)
        self._isOddAddressSignals = decoder.readField(1)

        self._screeningIndicator = decoder.readField(2)
        self._addressPresentationRestricted = decoder.readField(2)

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

