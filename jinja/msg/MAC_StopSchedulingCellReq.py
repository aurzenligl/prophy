import aprot

class MAC_StopSchedulingCellReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId)]
	
	