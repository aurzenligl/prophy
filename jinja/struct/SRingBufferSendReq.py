import aprot

class SRingBufferSendReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',aprot.u16),('radioBearerId',aprot.u8),('validDrxConfigId',aprot.u8),('drxConfigId',TConfigurationId),('packetId',aprot.u16),('frameNumber',aprot.u16),('harqRespFlag',aprot.u8),('subFrameNumber',aprot.u8),('size',aprot.u16),('dataPtr',aprot.u32)]
	
	