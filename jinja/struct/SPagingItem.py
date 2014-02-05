import aprot

class SPagingItem(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('frameNumber',TFrameNumber),('subFrameNumber',TSubFrameNumber),('data', aprot.bytes(size = MAX_PCCH_DATA))]
	
	