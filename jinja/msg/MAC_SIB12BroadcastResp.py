import aprot

class MAC_SIB12BroadcastResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('transactionId',TTransactionID),('messageIdentifier',aprot.u16),('serialNumber',aprot.u16),('messageResult',SMessageResult)]
	
	