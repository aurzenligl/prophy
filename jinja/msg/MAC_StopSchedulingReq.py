import aprot

class MAC_StopSchedulingReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',TUeId),('handoverType',EHandoverType),('enableRlcBufferStateReport',TBoolean),('rbStopSchedulingInfo', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]
	
	