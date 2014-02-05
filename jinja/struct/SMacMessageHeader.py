import aprot

class SMacMessageHeader(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellId),('frameNumber',TFrameNumber),('subFrameNumber',TSubFrameNumber),('srioDioBufferAddr',aprot.u32),('srioDioBufferSize',aprot.u32)]
	
	