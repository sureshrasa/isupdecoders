from Parameter import *
from ByteStream import *

class NationalForwardCallIndicators(Parameter):
    def __init__(self, stream):
        super(NationalForwardCallIndicators, self).__init__(stream)
        
        flags = stream.readByte()
        self._isCliBlocking = flags & 0xA0
        self._isNetworkTranslatedAddress = flags & 0x80
        self._isPriorityAccess = flags & 0x40
        self._isProtection = flags & 0x20

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

