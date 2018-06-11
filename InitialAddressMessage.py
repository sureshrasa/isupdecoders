from ByteStream import *
from ForwardCallIndicatorsDecoder import *
from CallingPartyCategoryDecoder import *
from TransmissionMediumRequirementDecoder import *
from CalledPartyNumberDecoder import *
from IsupParameterDecoder import *

class InitialAddressMessage:
    def __init__(self, stream):
        self._natureOfConnectionIndictors = stream.readField(8)
        self._forwardCallIndicatorsDecoder = ForwardCallIndicatorsDecoder.decode(stream)
        self._callingPartyCategory = CallingPartyCategoryDecoder.decode(stream)
        self._transmissionMediumRequirement = TransmissionMediumRequirementDecoder.decode(stream)
        cpnOffset = stream.readField(8)
        optionalOffset = stream.readField(8)
        self._calledPartyNumber = CalledPartyNumberDecoder.decode(StreamDecoderSlice(stream, stream.readField(8)))

        self._optionalParams = {}
        if (optionalOffset > 0):
            while (stream.hasMore()):
                tag = stream.readField(8)
                if (tag == 0):
                    break;

                size = stream.readField(8)
                if (size == 0):
                    break;
                self._optionalParams[tag] = IsupParameterDecoder.decode(tag, size, StreamDecoderSlice(stream, size))

    @property
    def natureOfConnectionIndictors(self):
        return self._natureOfConnectionIndictors

    @property
    def forwardCallIndicatorsDecoder(self):
        return self._forwardCallIndicatorsDecoder

    @property
    def callingPartyCategory(self):
        return self._callingPartyCategory

    @property
    def transmissionMediumRequirement(self):
        return self._transmissionMediumRequirement

    @property
    def calledPartyNumber(self):
        return self._calledPartyNumber

    def getOptionalParam(self, tag):
        return self._optionalParams.get(tag)

    def __str__(self):
        return ("IAM["
        + str(self.natureOfConnectionIndictors) + ","
        + str(self.forwardCallIndicatorsDecoder) + ","
        + str(self.callingPartyCategory) + ","
        + str(self.transmissionMediumRequirement) + ","
        + str(self.calledPartyNumber) + ","
        + ",".join(map(str, self._optionalParams.values())) + "]")
