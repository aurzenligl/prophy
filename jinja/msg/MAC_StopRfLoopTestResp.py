import aprot

class MAC_StopRfLoopTestResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId)]
	
	