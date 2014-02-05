import aprot

class ERlcDataSendRespCause(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('ERlcDataSendRespCause_MaxRlcRetransExceeded',3),
	 			    ('ERlcDataSendRespCause_DiscardDcmUeBasedThresh',5),
	 			    ('ERlcDataSendRespCause_DiscardDcmCellBasedThresh',6),
	 			    ('ERlcDataSendRespCause_OutOfMemory',2),
	 			    ('ERlcDataSendRespCause_DiscardTimerExpired',4),
	 			    ('ERlcDataSendRespCause_RlcTransStatusOk',0),
	 			    ('ERlcDataSendRespCause_InvalidParameter',1)]