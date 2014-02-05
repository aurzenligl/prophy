import aprot

class MAC_PduMuxBundledDataReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellIdU16),('frameNumber',aprot.u16),('subFrameNumber',aprot.u8),('cfi',TCfiU8),('lastTbInTti',TBooleanU8),('latencyBudgetExceeded',TBooleanU8),('numOfBundledPduMuxMsgs',aprot.u8),('data', aprot.bytes(size = 1))]
	
	