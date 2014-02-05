import aprot

class ECATypeOfOperation(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('ECATypeOfOperation_CaCellDelete',1),
	 			    ('ECATypeOfOperation_CaCellSetup',0)]