import aprot

class SRingBufferDlParam(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('destinationSrioId',TAaSysComNid),('addressLastReadMarkerPtr',aprot.u32),('startAddressBlocks',aprot.u32),('lengthBlocks',aprot.u32)]
	
	