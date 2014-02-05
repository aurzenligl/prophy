import aprot

class MAC_RadioBearerSetupResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID),('spsCrnti',TCrnti),('container',UUlTfrParamContainer),('sRbList', aprot.bytes(size = MAX_NUM_SRB_PER_USER_WO_SRB1)),('dRbList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]
	
	