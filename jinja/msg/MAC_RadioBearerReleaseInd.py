import aprot

class MAC_RadioBearerReleaseInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLCelId),('ueList', aprot.bytes(size = MAX_NUM_OF_RELEASED_UES))]
	
	