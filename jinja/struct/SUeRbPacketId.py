import aprot

class SUeRbPacketId(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',TUeId),('radioBearerId',TRadioBearerId),('packetId',TPacketId)]
	
	