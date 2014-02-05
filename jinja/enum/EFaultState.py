import aprot

class EFaultState(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('EFaultState_Cancel',0),
	 			    ('EFaultState_Event',2),
	 			    ('EFaultState_Start',1)]