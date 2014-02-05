import aprot

class SDlSchPduMuxAmountOctets(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('logicalChannelId',aprot.u16),('ctrl',aprot.u16),('data',aprot.u16)]
	
	