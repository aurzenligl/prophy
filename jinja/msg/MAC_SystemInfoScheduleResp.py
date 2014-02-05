import aprot

class MAC_SystemInfoScheduleResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('transactionId',TTransactionID)]
	
	