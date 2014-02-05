import aprot

class SGbrLoadCellDl(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfUsedPrbsForGbrTrafficDl',TMeasurementValue),('averageNbrOfAvailablePrbsForGbrDl',TMeasurementValue),('initTransmEfficiencyDl',TMeasurementValue),('ratioOfPdcchUtilizUesWithGbrBearersDl',TMeasurementValue)]
	
	