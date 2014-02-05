import aprot

class ERandomAccessEvent(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('ERandomAccessEvent_InitialAccess',0),
	 			    ('ERandomAccessEvent_Other',1)]