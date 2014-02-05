import aprot

class MAC_CcchDataSendReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('data', aprot.bytes(size = MAX_CCCH_DATA))]
	
	