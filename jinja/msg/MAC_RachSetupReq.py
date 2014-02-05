import aprot

class MAC_RachSetupReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('lCelId',TLocalCellResId),('rachParams',SRachParams)]
	
	