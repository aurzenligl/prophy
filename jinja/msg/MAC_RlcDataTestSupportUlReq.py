import aprot

class MAC_RlcDataTestSupportUlReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('c',SRingBufferUlItem),('data', aprot.bytes(size = MAX_RLC_DATA))]
	
	