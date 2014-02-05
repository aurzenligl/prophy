import aprot

class MAC_RlcDataDiscardInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueRbPacketId', aprot.bytes(size = MAX_NUM_PACKET_IDS))]
	
	