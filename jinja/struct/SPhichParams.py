import aprot

class SPhichParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('phichRes',EOaMPhichRes),('phichDur',EOaMPhichDur)]
	
	