import aprot

class MAC_RadioBearerDeleteReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID),('spsCrntiReleaseReq',TBoolean),('spsCrnti',TCrnti),('container',UWmpDcmUserContainer),('ueParams',SUeParams),('sRbList', aprot.bytes(size = MAX_NUM_SRB_PER_USER_WO_SRB1)),('dRbList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]
	
	