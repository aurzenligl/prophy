import aprot

class ERlsCause(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('ERlsCause_RLF',3),
	 			    ('ERlsCause_TatExpiry',2),
	 			    ('ERlsCause_PuschRlf_OFF',12),
	 			    ('ERlsCause_InSync',1),
	 			    ('ERlsCause_SrsDowngrade',19),
	 			    ('ERlsCause_CqiRlf_OFF',10),
	 			    ('ERlsCause_Bundling_OFF',14),
	 			    ('ERlsCause_RA_SR',4),
	 			    ('ERlsCause_PuschRlf_ON',11),
	 			    ('ERlsCause_AckNackRlf_OFF',6),
	 			    ('ERlsCause_OutSync',0),
	 			    ('ERlsCause_SrsRlf_OFF',16),
	 			    ('ERlsCause_SrsRlf_ON',15),
	 			    ('ERlsCause_Tat2withLcg0Bsr',17),
	 			    ('ERlsCause_RA_Completed',7),
	 			    ('ERlsCause_SrsUpgrade',18),
	 			    ('ERlsCause_AckNackRlf_ON',5),
	 			    ('ERlsCause_TmSwitchToTm8',22),
	 			    ('ERlsCause_Bundling_ON',13),
	 			    ('ERlsCause_OutSyncFinal',8),
	 			    ('ERlsCause_TmSwitchToTm3',20),
	 			    ('ERlsCause_CqiRlf_ON',9),
	 			    ('ERlsCause_TmSwitchToTm7',21)]