import aprot

class MAC_SIB12BroadcastInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('messageIdentifier',aprot.u16),('serialNumber',aprot.u16),('numberOfBroadcasts',aprot.u16)]
	
	