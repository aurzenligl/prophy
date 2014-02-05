import aprot

class SGbrLoadCellUl(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfUsedPrbsForGbrTrafficUl',TMeasurementValue),('averageNbrOfAvailablePrbsForGbrUl',TMeasurementValue),('initTransmEfficiencyUl',TMeasurementValue),('ratioOfPdcchUtilizUesWithGbrBearersUl',TMeasurementValue)]
	
	