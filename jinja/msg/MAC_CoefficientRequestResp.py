import aprot

class MAC_CoefficientRequestResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('macCoefficientValues', aprot.bytes(size = MAX_NUM_COEFF_BW))]
	
	