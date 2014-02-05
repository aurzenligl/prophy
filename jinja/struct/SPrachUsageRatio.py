import aprot

class SPrachUsageRatio(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfGroupARAPreambleReceived',TMeasurementValue),('nbrOfGroupBRAPreambleReceived',TMeasurementValue),('nbrOfRAPreambleReceivedDedicPreamble',TMeasurementValue),('nbrOfRARespTransmitForGroupAPreamble',TMeasurementValue),('nbrOfRARespTransmitForGroupBPreamble',TMeasurementValue),('nbrOfRARespTransmitForDedicPreamble',TMeasurementValue),('nbrOfAssignNGDedicPreambleSyncReq',TMeasurementValue),('nbrOfOpportDedicPreambleReception',TMeasurementValue),('nbrOfDedicPreambleAllocated',TMeasurementValue),('nbrOfOpportGroupARAPreambleRecept',TMeasurementValue),('nbrOfOpportGroupBRAPreambleRecept',TMeasurementValue)]
	
	