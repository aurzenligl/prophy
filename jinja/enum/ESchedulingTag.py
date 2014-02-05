import aprot

class ESchedulingTag(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('ESchedulingTag_NewAllocation',13),
	 			    ('ESchedulingTag_Msg4USS',4),
	 			    ('ESchedulingTag_DrxPrioritised',9),
	 			    ('ESchedulingTag_BroadcastPagingRachResponse',0),
	 			    ('ESchedulingTag_DelaySensitiveAllocation',12),
	 			    ('ESchedulingTag_UlSr',7),
	 			    ('ESchedulingTag_Msg4CSS',1),
	 			    ('ESchedulingTag_GbrAllocation',11),
	 			    ('ESchedulingTag_ProactiveAssignment',14),
	 			    ('ESchedulingTag_PreambleAssignmentCSS',2),
	 			    ('ESchedulingTag_UlReTx',3),
	 			    ('ESchedulingTag_Qci234',15),
	 			    ('ESchedulingTag_DlReTx',6),
	 			    ('ESchedulingTag_SemiPersistent',8),
	 			    ('ESchedulingTag_INVALID_SCHEDULING_TAG',16),
	 			    ('ESchedulingTag_PreambleAssignmentUSS',5),
	 			    ('ESchedulingTag_SrbAllocation',10)]