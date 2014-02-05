import aprot

class SPathloss(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfUes', aprot.bytes(size = 124))]
	
	