import aprot

class MAC_SIB12BroadcastReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('transactionId',TTransactionID),('messageIdentifier',aprot.u16),('serialNumber',aprot.u16),('numberOfBroadcastsRequested',aprot.u16),('padding',aprot.u16),('repetitionPeriod',aprot.u32),('killFlag',TBoolean),('siSegmentSize', aprot.bytes(size = MAX_NUM_SI_SEGMENT)),('siSegmentData', aprot.bytes(size = MAX_SI_SEGMENT_DATA))]
	
	