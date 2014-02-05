import aprot

class MAC_HarqReleaseReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellId),('frameNumber',TFrameNumber),('subFrameNumber',TSubFrameNumber),('harqReleaseInfo', aprot.bytes(size = 1))]
	
	