import aprot

class EAaMemPoolCid(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('EAaMemPoolCid_ApplicationCidStart',2),
	 			    ('EAaMemPoolCid_Dynamic',1),
	 			    ('EAaMemPoolCid_System',0)]