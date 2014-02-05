import aprot

class SRingBufferUlPayload(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('d', aprot.bytes(size = SIZE_RINGBUF_PAYLOAD_UL))]
	
	