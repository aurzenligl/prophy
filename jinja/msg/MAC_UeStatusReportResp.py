import aprot

class MAC_UeStatusReportResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID),('container',UUeStatusReportRespContainerDcm)]
	
	