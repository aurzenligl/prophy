import aprot

class SAmountOctets(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('rbId',TRadioBearerId),('isDataOctetsLeft',aprot.u8),('isCtrlOctetsLeft',aprot.u8)]
	
	