import aprot

class EIbType(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('EIbType_SIB',1),
	 			    ('EIbType_MIB_SIB',2),
	 			    ('EIbType_MIB',0)]