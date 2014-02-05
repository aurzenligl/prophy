import aprot

class EPagingNB(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('EPagingNB_OneEighthT',5),
	 			    ('EPagingNB_OneThirtySecondT',7),
	 			    ('EPagingNB_QuarterT',4),
	 			    ('EPagingNB_OneT',2),
	 			    ('EPagingNB_OneSixteenthT',6),
	 			    ('EPagingNB_TwoT',1),
	 			    ('EPagingNB_HalfT',3),
	 			    ('EPagingNB_FourT',0)]