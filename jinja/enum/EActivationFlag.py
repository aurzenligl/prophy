import aprot

class EActivationFlag(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('EActivationFlag_Activate',0),
	 			    ('EActivationFlag_Deactivate',1)]