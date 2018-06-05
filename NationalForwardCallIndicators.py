from Parameter import *
from ByteStream import *

class NationalForwardCallIndicators(Parameter):
    def __init__(self, decoder):
        super(NationalForwardCallIndicators, self).__init__(decoder)
        
        self._isCliBlocking = decoder.readField(1)
        self._isNetworkTranslatedAddress = decoder.readField(1)
        self._isPriorityAccess = decoder.readField(1)
        self._isProtection = decoder.readField(1)

    @property
    def code(self):
        return self._code

    @property
    def length(self):
        return self._length

    @property
    def isCliBlocking(self):
        return self._isCliBlocking

    @property
    def isNetworkTranslatedAddress(self):
        return self._isNetworkTranslatedAddress

    @property
    def isPriorityAccess(self):
        return self._isPriorityAccess

    @property
    def isProtection(self):
        return self._isProtection

