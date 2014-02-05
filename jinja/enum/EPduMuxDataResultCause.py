import aprot

class EPduMuxDataResultCause(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('EPduMuxDataResultCause_ResultOk',0),
	 			    ('EPduMuxDataResultCause_TooLatePhase2',2),
	 			    ('EPduMuxDataResultCause_TooLatePhase1',1),
	 			    ('EPduMuxDataResultCause_Other',3),
	 			    ('EPduMuxDataResultCause_NotRequested',4),
	 			    ('EPduMuxDataResultCause_NotEnoughData',5)]