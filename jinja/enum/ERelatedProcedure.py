import aprot

class ERelatedProcedure(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('ERelatedProcedure_SCellRelease',3),
	 			    ('ERelatedProcedure_InSync',2),
	 			    ('ERelatedProcedure_sCellConfiguration',0),
	 			    ('ERelatedProcedure_TmSwitch',4),
	 			    ('ERelatedProcedure_RA_SR',1),
	 			    ('ERelatedProcedure_sCellConfigurationByHO',5)]