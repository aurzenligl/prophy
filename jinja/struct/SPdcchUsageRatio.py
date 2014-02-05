import aprot

class SPdcchUsageRatio(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfMultiplexedPdcchDl',TMeasurementValue),('nbrOfMultiplexedPdcchUl',TMeasurementValue),('nbrOfMultiplexedPdcchVoiceDl',TMeasurementValue),('nbrOfMultiplexedPdcchVoiceUl',TMeasurementValue),('totalNbrOfCces',TMeasurementValue),('nbrOfCcesAssignedToPdcch',TMeasurementValue),('nbrOfCcesAssignedToPdcchVoice',TMeasurementValue)]
	
	