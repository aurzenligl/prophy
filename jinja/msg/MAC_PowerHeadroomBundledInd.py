import aprot

class MAC_PowerHeadroomBundledInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('frameNumber',TFrameNumber),('subFrameNumber',TSubFrameNumber),('uePhrList', aprot.bytes(size = MAX_NUM_OF_USERS_IN_TTI))]
	
	