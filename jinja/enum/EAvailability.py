import aprot

class EAvailability(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('EAvailability_NotAvailable',0),
	 			    ('EAvailability_BasebandDisabled',2),
	 			    ('EAvailability_Available',1)]