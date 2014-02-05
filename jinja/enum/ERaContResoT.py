import aprot

class ERaContResoT(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('ERaContResoT_sf32',32),
	 			    ('ERaContResoT_sf48',48),
	 			    ('ERaContResoT_sf16',16),
	 			    ('ERaContResoT_DCM',2000),
	 			    ('ERaContResoT_sf56',56),
	 			    ('ERaContResoT_sf24',24),
	 			    ('ERaContResoT_sf40',40),
	 			    ('ERaContResoT_sf64',64),
	 			    ('ERaContResoT_sf8',8),
	 			    ('ERaContResoT_NotDefined',0),
	 			    ('ERaContResoT_DCM_SCT',3200)]