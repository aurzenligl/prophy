import aprot

class MAC_TCrntiDeleteInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellId),('crnti',TCrnti),('ueIndex',TUeIndex),('frameNumber',TFrameNumber),('subFrameNumber',TSubFrameNumber),('sendDeleteReqToMacData',TBoolean)]
	
	