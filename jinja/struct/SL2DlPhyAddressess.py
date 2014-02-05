import aprot

class SL2DlPhyAddressess(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('pdschCw0SendReqAddress',TAaSysComSicad),('pdschCw1SendReqAddress',TAaSysComSicad),('srioType9Cos',aprot.u32),('srioType9StreamId',aprot.u32),('pdschEventQueueId',aprot.u32)]
	
	