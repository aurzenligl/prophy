import aprot

class MAC_UeMeasResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TOaMLnCelId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID),('roundTripDelayEstimate',aprot.u32)]
	
	