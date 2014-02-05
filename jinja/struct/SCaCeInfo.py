import aprot

class SCaCeInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('caCeAvail',TBooleanU8),('caCeValue',TCaCeValue),('unused',aprot.u16)]
	
	