import aprot

class SRingBufferDlBlock(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('data',SRingBufferDlPayload),('ctrl',SRingBufferDlCtrl)]
	
	