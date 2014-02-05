import aprot

class MAC_BcchModIndReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('transactionId',TTransactionID),('activationTimePresent',TBoolean),('activationTime',TFrameNumber),('duration',SDuration),('pagingNb',EPagingNB),('pagingBitmapData', aprot.bytes(size = MAX_PAGING_BITMAP_DATA)),('data', aprot.bytes(size = MAX_PCCH_DATA))]
	
	