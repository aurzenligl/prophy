import aprot

class MAC_MacCrntiCeInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellId),('crnti',TCrnti),('tempCrnti',TCrnti),('ueIndex',TUeIndex),('tempUeIndex',TUeIndex),('frameNumber',TFrameNumber),('subFrameNumber',TSubFrameNumber)]
	
	