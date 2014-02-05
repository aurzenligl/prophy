import aprot

class MAC_CongestionInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('gbrCongestionCause',ESpecificCauseLte),('numOfExceedingRb',aprot.u32),('cellResourceGroupId',TCellResourceGroupId)]
	
	