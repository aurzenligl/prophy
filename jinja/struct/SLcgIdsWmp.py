import aprot

class SLcgIdsWmp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueBufferStatusReport',TBufferSize),('receivedDataSize',TBufferSize)]
	
	