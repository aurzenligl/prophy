import aprot

class EDrbType(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('EDrbType_NonGbr_Voice',4),
	 			    ('EDrbType_Gbr',0),
	 			    ('EDrbType_Gbr_Voice',3),
	 			    ('EDrbType_Signalling',2),
	 			    ('EDrbType_NonGBR',1)]