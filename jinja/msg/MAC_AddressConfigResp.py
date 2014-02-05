import aprot

class MAC_AddressConfigResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('transactionId',TTransactionID),('serviceInfo', aprot.bytes(size = MAX_NUM_OF_TESTABILITY_SERVICES))]
	
	