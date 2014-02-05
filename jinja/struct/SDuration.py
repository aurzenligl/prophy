import aprot

class SDuration(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('bcchModPeriodLength',TBcchModPeriodLength),('bcchModPeriodNumber',TBcchModPeriodNumber)]
	
	