import aprot

class MAC_CcchDataReceiveInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('msg3Info', aprot.bytes(size = MAX_MSG3_PER_TTI))]
	
	