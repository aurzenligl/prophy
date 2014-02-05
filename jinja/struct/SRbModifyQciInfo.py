import aprot

class SRbModifyQciInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('schedulWeight',TSchedulingWeight),('qci',aprot.u32)]
	
	