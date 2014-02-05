import aprot

class MAC_MeasGapStopReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID)]
	
	