import aprot

class SRingBufferUlCtrl(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('item', aprot.bytes(size = MAX_RINGBUF_CTRL_UL)),('totalPayloadLen',aprot.u32),('nextMarkerPtr',aprot.u32),('marker',aprot.u32)]
	
	