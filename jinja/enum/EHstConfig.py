import aprot

class EHstConfig(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('EHstConfig_NotApplied',0),
	 			    ('EHstConfig_Hst',1),
	 			    ('EHstConfig_HstPucch',2)]