import aprot

class MAC_UlBufferStatusInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('header',SMacMessageHeader),('payload',SUlBufStatusIndPayload)]
	
	