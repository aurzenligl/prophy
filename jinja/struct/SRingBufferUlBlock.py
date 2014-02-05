import aprot

class SRingBufferUlBlock(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('data',SRingBufferUlPayload),('ctrl',SRingBufferUlCtrl)]
	
	