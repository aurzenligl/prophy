import aprot

class SRingBufferDlCtrl(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('sendReq', aprot.bytes(size = MAX_RINGBUF_CTRL_DL)),('padding',aprot.u32),('nextMarkerPtr',aprot.u32),('marker',aprot.u32)]
	
	