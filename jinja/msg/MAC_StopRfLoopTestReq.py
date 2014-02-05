import aprot

class MAC_StopRfLoopTestReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId)]
	
	