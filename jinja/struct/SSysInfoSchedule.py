import aprot

class SSysInfoSchedule(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('siType',ESysInfoTypeId),('siPeriodicity',TSiPeriodicity),('siRepetition',TSiRepetition)]
	
	