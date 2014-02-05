import aprot

class MAC_InternalAddressReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('transactionId',TTransactionID),('nodeAddress',SNodeAddress)]
	
	