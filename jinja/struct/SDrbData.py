import aprot

class SDrbData(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('drbId',TMeasurementValue),('nbrOfAllocatedPrbs',TMeasurementValue)]
	
	