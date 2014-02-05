import aprot

class STransmittedAndReceivedPower(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('phichTransmitPower',TMeasurementValue),('transmitPowerOfControlPart',TMeasurementValue),('totalTransmitPowerBranch1',TMeasurementValue),('totalTransmitPowerBranch2',TMeasurementValue),('receivedTotalPowerBranch1',TMeasurementValue),('receivedTotalPowerBranch2',TMeasurementValue)]
	
	