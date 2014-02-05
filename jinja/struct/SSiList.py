import aprot

class SSiList(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('siType',ESysInfoTypeId),('data', aprot.bytes(size = MAX_SI_DATA))]
	
	