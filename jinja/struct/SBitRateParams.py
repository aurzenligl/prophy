import aprot

class SBitRateParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('minBitrateUl',TOaMMinBitrateUl),('minBitrateDl',TOaMMinBitrateDl),('maxBitrateUl',TOaMMaxBitrateUl),('maxBitrateDl',TOaMMaxBitrateDl)]
	
	