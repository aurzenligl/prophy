import aprot

class MAC_ConfigChangeInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('ueIndex',TUeIndex),('hasDrxConfigId',TBooleanU8),('drxConfigId',TConfigurationId)]
	
	