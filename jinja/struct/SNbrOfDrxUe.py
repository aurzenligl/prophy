import aprot

class SNbrOfDrxUe(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfNonDrxUe',TMeasurementValue),('nbrOfLongDrxUe',TMeasurementValue)]
	
	