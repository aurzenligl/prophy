import aprot

class SBearerIds(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('drbId',TRadioBearerIdU8),('lcgId',TLogicalChannelGrIdU8),('rcvdData',aprot.u16)]
	
	