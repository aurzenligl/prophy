import aprot

class MAC_BundledContentionResInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('numberOfContResMsg',TNumberOfItems),('pduMuxContentionResInd', aprot.bytes(size = MAX_NUM_CONT_RES_PER_MSG))]
	
	