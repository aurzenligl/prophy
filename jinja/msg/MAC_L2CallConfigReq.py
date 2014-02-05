import aprot

class MAC_L2CallConfigReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('ueGroup',TUeGroup),('transactionId',TTransactionID),('lnCelIdSCell', aprot.bytes(size = 1)),('spsCrntiAllocationReq',TBoolean),('handoverType',EHandoverType),('ueSetupParams',SUeSetupParams),('container',UWmpDcmUserContainer),('cqiParams',SCqiParams),('controlOffsets',SPuschControlOffsets),('ueParams',SUeParams),('ttiBundlingEnable',TBoolean),('tpcPdcchConfigParams',STpcPdcchConfigParams),('ulPCUeParams',SUlPCUeParams),('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated),('sRbInfoList', aprot.bytes(size = MAX_NUM_SRB_PER_USER)),('rbInfoList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]
	
	