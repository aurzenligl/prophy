import aprot

class MAC_InternalAddressResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('transactionId',TTransactionID)]
	
	