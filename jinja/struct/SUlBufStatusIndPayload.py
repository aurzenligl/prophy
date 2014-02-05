import aprot

class SUlBufStatusIndPayload(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueIdInfo', aprot.bytes(size = MAX_NUM_OF_USERS_IN_TTI))]
	
	