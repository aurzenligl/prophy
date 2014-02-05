import aprot

class SAmbrParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ambrUl',TAmbr),('ambrDl',TAmbr)]
	
	