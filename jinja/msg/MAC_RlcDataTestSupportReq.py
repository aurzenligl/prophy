import aprot

class MAC_RlcDataTestSupportReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('c',SRingBufferSendReq),('data', aprot.bytes(size = MAX_RLC_DATA))]
	
	