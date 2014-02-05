import aprot

class MAC_CaCellConfigReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('poolId',TPoolId),('transactionId',TTransactionID),('typeOfOperation',ECATypeOfOperation),('l2DlPhyAddressess',SL2DlPhyAddressess),('l2MacPsAddresses',SL2MacPsAddresses)]
	
	