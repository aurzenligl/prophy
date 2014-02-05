import aprot

class MAC_UlVoLteReceptionInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellId),('frameNumber',TFrameNumber),('subFrameNumber',TSubFrameNumber),('ueInfoList', aprot.bytes(size = MAX_NUM_OF_USERS_IN_TTI))]
	
	