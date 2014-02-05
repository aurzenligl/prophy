import aprot

class EPollPDU(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('EPollPDU_p256',6),
	 			    ('EPollPDU_p16',2),
	 			    ('EPollPDU_p64',4),
	 			    ('EPollPDU_pInfinity',7),
	 			    ('EPollPDU_p4',0),
	 			    ('EPollPDU_p8',1),
	 			    ('EPollPDU_p128',5),
	 			    ('EPollPDU_p32',3)]