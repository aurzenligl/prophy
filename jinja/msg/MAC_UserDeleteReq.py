import aprot

class MAC_UserDeleteReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('validUeId',TBoolean),('ueId',TUeId),('transactionId',TTransactionID),('spsCrntiReleaseReq',TBoolean),('ueReleaseCause',ECauseLte),('specificUeReleaseCause',ESpecificCauseLte)]
	
	