import aprot

class MAC_OverloadInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellId),('numberOfOverloadTtis',TNumberOfItems),('maxNumberOfUesPerOverloadTti',TNumberOfItems)]
	
	