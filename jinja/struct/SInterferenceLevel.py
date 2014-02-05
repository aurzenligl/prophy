import aprot

class SInterferenceLevel(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('interferenceLevelPucch',TMeasurementValue),('interferenceLevelPusch',TMeasurementValue),('interferenceLevelPrach',TMeasurementValue)]
	
	