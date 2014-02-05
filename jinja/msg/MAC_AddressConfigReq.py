import aprot

class MAC_AddressConfigReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('transactionId',TTransactionID),('poolId',TPoolId),('enbId',TOaMLnBtsId),('poolInfo', aprot.bytes(size = MAX_NUM_OF_POOLS_IN_SUPER_POOL))]
	
	