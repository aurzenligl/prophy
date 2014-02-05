import aprot

class SPduTimeStamp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('frameNumber',TFrameNumber),('subFrameNumber',TSubFrameNumber)]
	
	