import aprot

class SRingBufferUlItem(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',aprot.u16),('radioBearerId',aprot.u8),('subFrameNumber',aprot.u8),('frameNumber',aprot.u16),('lastUlSdu',aprot.u8),('unused1',aprot.u8),('unused2',aprot.u16),('size',aprot.u16),('dataPtr',aprot.u32)]
	
	