import aprot

class MAC_CellDeleteReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId)]
	
	