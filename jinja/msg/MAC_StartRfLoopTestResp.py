import aprot

class MAC_StartRfLoopTestResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId)]
	
	