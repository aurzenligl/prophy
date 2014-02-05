import aprot

class SUeSetupParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('srEnable',TBoolean),('pucchResourceIndex',TPucchResourceIndex),('srPeriod',ESrPeriod),('srOffset',TSrOffset)]
	
	