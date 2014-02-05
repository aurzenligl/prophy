import aprot

class EPollByte(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('EPollByte_kb250',5),
	 			    ('EPollByte_kb750',8),
	 			    ('EPollByte_kb50',1),
	 			    ('EPollByte_kb3000',13),
	 			    ('EPollByte_kb25',0),
	 			    ('EPollByte_kb1500',11),
	 			    ('EPollByte_kb375',6),
	 			    ('EPollByte_kb1250',10),
	 			    ('EPollByte_kb2000',12),
	 			    ('EPollByte_kbInfinity',14),
	 			    ('EPollByte_kb100',3),
	 			    ('EPollByte_kb1000',9),
	 			    ('EPollByte_kb75',2),
	 			    ('EPollByte_kb500',7),
	 			    ('EPollByte_kb125',4)]