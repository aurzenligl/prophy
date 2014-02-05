import aprot

class MAC_CrntiReserveReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crntiList', aprot.bytes(size = MAX_NUM_USER_PER_CELL))]
	
	