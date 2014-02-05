import aprot

class SResourceBlockUsageRatio(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('dlRbUsageRatio',TMeasurementValue),('ulRbUsageRatio',TMeasurementValue),('dlRbUsageRatioDbch',TMeasurementValue),('dlRbUsageRatioPch',TMeasurementValue),('dlRbUsageRatioRar',TMeasurementValue),('dlRbUsageRatioVoice',TMeasurementValue),('ulRbUsageRatioVoice',TMeasurementValue)]
	
	