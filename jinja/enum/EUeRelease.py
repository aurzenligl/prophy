import aprot

class EUeRelease(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('EUeRelease_Rel9',1),
	 			    ('EUeRelease_Rel8',0),
	 			    ('EUeRelease_Undefined',0xFFFF),
	 			    ('EUeRelease_Rel10',2)]