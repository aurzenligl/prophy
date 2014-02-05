import aprot

class MAC_RlcDataReceiveInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('sRingBufferUlItem',SRingBufferUlItem)]
	
	