class Header:
    def __init__(self, decoder):
        self._magic = decoder.readField(32)
        if self._magic != 0xa1b2c3d4:
            raise Exception("Unknown PCAP version", self._version)

        self._version = decoder.readField(32)
        self._tzOffset = decoder.readField(32)
        self._tmAccuracy = decoder.readField(32)
        self._snapshotMaxLen = decoder.readField(32)
        self._linkLayerType = decoder.readField(32)

    def __str__(self):
        return "PcapHeader[magic:{0}, ver:{1}, tzOffset:{2}, tmAccuracy:{3}, snapShotMaxLen:{4}, linkLayerType:{5}]".format(
                hex(self.magic), self.version, self.tzOffset, self.tmAccuracy, self.snapshotMaxLen, self.linkLayerType)                

    @property
    def magic(self):
        return self._magic

    @property
    def version(self):
        return self._version

    @property
    def tzOffset(self):
        return self._tzOffset

    @property
    def tmAccuracy(self):
        return self._tmAccuracy

    @property
    def snapshotMaxLen(self):
        return self._snapshotMaxLen

    @property
    def linkLayerType(self):
        return self._linkLayerType

class Packet:
    def __init__(self, decoder):
        self._tmStampSecs = decoder.readField(32)
        self._tmStampMillisecs = decoder.readField(32)
        self._captureLen = decoder.readField(32)
        self._length = decoder.readField(32)
        self._payload = decoder.readBytes(self._length)

    def __str__(self):
        return "PcapPacket[timestampSecs:{0}, timestampMillsecs:{1}, captureLen:{2}, len:{3}\npayload:{4}]".format(
                self.tmStampSecs, self.tmStampMillisecs, self.captureLen, self.length, ",".join(map(str,self.payload)))                
    @property
    def tmStampSecs(self):
        return self._tmStampSecs

    @property
    def tmStampMillisecs(self):
        return self._tmStampMillisecs

    @property
    def captureLen(self):
        return self._captureLen

    @property
    def length(self):
        return self._length

    @property
    def payload(self):
        return self._payload
