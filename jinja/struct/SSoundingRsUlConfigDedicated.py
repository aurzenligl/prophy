import aprot

class SSoundingRsUlConfigDedicated(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('enableSRS',TBoolean),('srsBandwidth',TSrsBandwidth),('srsHoppingBw',TSrsHoppingBw),('freqDomPos',TFrequencyDomainPosition),('srsDuration',TBoolean),('srsConfIndex',TSrsConfIndex),('transComb',TTransmissionComb),('cyclicShift',TCyclicShift)]
	
	