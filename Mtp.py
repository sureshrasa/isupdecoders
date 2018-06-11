from ByteStream import *

#+-------+-------+---------------+---------------+-------+-~~~~~~~~~~~~~~~~~ +
#+ 4bits | 4bits | 14 bits       | 14 bits       | 4bits |  MTP3 User Data   |
#+-------+-------+---------------+---------------+-------+-~~~~~~~~~~~~~~~~~ +
#  SI       SSF        DPC             OPC          SLS       MTP3 User Part 
class Mtp3:
    SIZE = 5

    def __init__(self, decoder):
        self._ssf = decoder.readField(4)
        self._si = decoder.readField(4)
        #dpc_lsb = decoder.readField(8)
        #dpc_msb = decoder.readField(6)
        #opc_lsb = decoder.readField(2)
        #opc_isb = decoder.readField(8)
        #opc_msb = decoder.readField(4)
        self._dpc = decoder.readField(14) #dpc_msb<<8 | dpc_lsb
        self._opc = decoder.readField(14) #opc_msb<<10 | opc_isb<<2 | opc_lsb
        self._sls = decoder.readField(4)

    def __str__(self):
        return "Mtp3[ssf:{0}, si:{1}, dpc:{2}, opc:{3}, sls:{4}]".format(
                self.ssf, self.si, self.dpc, self.opc, self.sls)   
             
    @property
    def ssf(self):
        return self._ssf

    @property
    def si(self):
        return self._si

    @property
    def dpc(self):
        return self._dpc

    @property
    def opc(self):
        return self._opc

    @property
    def sls(self):
        return self._sls

class Mtp2:
    SIZE = 3

    def __init__(self, decoder):
        self._bsn = decoder.readField(7)
        self._bib = decoder.readField(1)
        self._fsn = decoder.readField(7)
        self._fib = decoder.readField(1)
        self._len = decoder.readField(6)
        decoder.readField(2)

    def __str__(self):
        return "Mtp2[bsn:{0}, bib:{1}, fsn:{2}, fib:{3}, length:{4}]".format(
                self.bsn, self.bib, self.fsn, self.fib, self.length)                

    @property
    def bsn(self):
        return self._bsn

    @property
    def bib(self):
        return self._bib

    @property
    def fsn(self):
        return self._fsn

    @property
    def fib(self):
        return self._fib

    @property
    def length(self):
        return self._len
