import aprot

class MAC_SystemInfoScheduleReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('transactionId',TTransactionID),('activationTimePresent',TBoolean),('activationTime',TFrameNumber),('mibSfnPosition',TMibSfnPosition),('mibSfnLength',TMibSfnLength),('siWindowLen',EOaMSiWindowLen),('siSchedule', aprot.bytes(size = MAX_NUM_SIS)),('siList', aprot.bytes(size = MAX_NUM_SIS)),('container',USystemInfoContainer),('siTypeSegmented',ESysInfoTypeId),('siSegmentSize', aprot.bytes(size = MAX_NUM_SI_SEGMENT)),('siSegmentData', aprot.bytes(size = MAX_SI_SEGMENT_DATA))]
	
	