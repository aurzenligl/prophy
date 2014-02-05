import aprot

class MAC_RadioBearerSetupReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID),('spsCrntiAllocationReq',TBoolean),('ueSetupParams',SUeSetupParams),('container',UWmpDcmUserContainer),('cqiParams',SCqiParams),('ueParams',SUeParams),('tpcPdcchConfigParams',STpcPdcchConfigParams),('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated),('sRbInfoList', aprot.bytes(size = MAX_NUM_SRB_PER_USER_WO_SRB1)),('drbInfoList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]
	
	