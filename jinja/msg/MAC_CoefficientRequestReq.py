import aprot

class MAC_CoefficientRequestReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('caBw', aprot.bytes(size = MAX_NUM_COEFF_BW))]
	
	