import aprot

class ELinkState(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('ELinkState_OutOfService',1),
	 			    ('ELinkState_LinkDeleted',3),
	 			    ('ELinkState_DeactivationOngoing',2),
	 			    ('ELinkState_InService',0)]