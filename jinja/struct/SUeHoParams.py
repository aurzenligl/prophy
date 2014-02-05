import aprot

class SUeHoParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueCategory',TUeCategory),('ueCategoryR10',TUeCategory),('ambrParams',SAmbrParams),('bitRateParams',SBitRateParams),('drxParameters',SDrxParameters)]
	
	