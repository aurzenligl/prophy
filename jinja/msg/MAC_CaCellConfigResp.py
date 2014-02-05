import aprot

class MAC_CaCellConfigResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TOaMLnCelId),('poolId',TPoolId),('transactionId',TTransactionID)]
	
	