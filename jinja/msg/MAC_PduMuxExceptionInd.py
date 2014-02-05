import aprot

class MAC_PduMuxExceptionInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('frameNumber',aprot.u16),('subFrameNumber',aprot.u16),('resLength',aprot.u32),('resArray', aprot.bytes(size = 1))]
	
	