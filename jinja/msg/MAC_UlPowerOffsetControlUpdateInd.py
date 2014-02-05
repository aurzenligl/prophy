import aprot

class MAC_UlPowerOffsetControlUpdateInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('container',UUlPowerControlUpdateIndContainer)]
	
	