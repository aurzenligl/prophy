import aprot

class SBearerList(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('drbId',TDrbId),('packetId',TPacketId)]
	
	