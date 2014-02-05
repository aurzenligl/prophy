import aprot

class ECAProcedureResults(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('ECAProcedureResults_sCellConfigurationCancel',1),
	 			    ('ECAProcedureResults_sCellConfigurationComplete',0)]