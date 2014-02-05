import aprot

class SGbrLoadUe(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',TMeasurementValue),('transmEfficiency',TMeasurementValue),('nbrOfBearers',TMeasurementValue),('drbData', aprot.bytes(size = 4))]
	
	