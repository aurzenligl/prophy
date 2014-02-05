import aprot

class SChannelUsageStatus(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfPdcchOfdmSymbol1',TMeasurementValue),('nbrOfPdcchOfdmSymbol2',TMeasurementValue),('nbrOfPdcchOfdmSymbol3',TMeasurementValue),('nbrOfProcessingResourceShortageSituation',TMeasurementValue),('nbrOfUnTransmitUesDueLackOfPdcchResource',TMeasurementValue),('pdfOfWidebankCQI', aprot.bytes(size = 256)),('pdfOfDlAverageDataRate',TMeasurementValue),('pdfOfUlAverageDataRate',TMeasurementValue),('pdfOfUeInactiveTimer', aprot.bytes(size = 11))]
	
	