import aprot

class MAC_StopSchedulingResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('ueId',TUeId),('bearerList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]
	
	