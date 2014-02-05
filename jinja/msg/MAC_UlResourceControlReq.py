import aprot

class MAC_UlResourceControlReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID),('cqiParams',SCqiParams),('ueSetupParams',SUeSetupParams),('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated),('tpcPdcchConfigParams',STpcPdcchConfigParams),('container',UUlResCtrlParamContainer),('cqiParamsScell', aprot.bytes(size = 1))]
	
	