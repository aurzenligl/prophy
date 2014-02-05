import aprot

class MAC_BufferStatusTriggerReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellId),('lnCellIdServCell',TOaMLnCelId),('frameNumber',TFrameNumber),('subFrameNumber',TSubFrameNumber)]
	
	