import aprot

class MAC_RlcDataSendResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueRbPacketIdList', aprot.bytes(size = MAX_NUM_SENDRESP_PACKET_IDS))]
	
	