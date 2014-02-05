import aprot

class SLcgIds(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueBufferStatusReport',TBufferSize),('receivedDataSize',TBufferSize)]
	
	