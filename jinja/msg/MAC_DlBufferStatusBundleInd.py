import aprot

class MAC_DlBufferStatusBundleInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellId),('numOfLchHaveData',TNumOfLch),('dlBsr', aprot.bytes(size = 1))]
	
	