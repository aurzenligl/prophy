import aprot

class EFaultSeverity(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('EFaultSeverity_Working',0),
	 			    ('EFaultSeverity_OutOfOrder',1),
	 			    ('EFaultSeverity_Degraded',2),
	 			    ('EFaultSeverity_Info',3)]