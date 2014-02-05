import aprot

class SRlcPdcpTraffic(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('transmittedDataRateIni',TMeasurementValue),('transmittedDataRateReTrans',TMeasurementValue),('receivedDataRate',TMeasurementValue),('nbrOfReset',TMeasurementValue),('amountOfDataBufferedRlcPdcp',TMeasurementValue)]
	
	