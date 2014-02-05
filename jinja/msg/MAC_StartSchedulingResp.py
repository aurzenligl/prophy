import aprot

class MAC_StartSchedulingResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('ueId',TUeId)]
	
	