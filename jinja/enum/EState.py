import aprot

class EState(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('EState_Disabled',1),
	 			    ('EState_Enabled',0)]