import aprot

class SAaTime(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('year',aprot.u32),('month',aprot.u32),('day',aprot.u32),('hour',aprot.u32),('minute',aprot.u32),('second',aprot.u32),('millisec',aprot.u32)]
	
	