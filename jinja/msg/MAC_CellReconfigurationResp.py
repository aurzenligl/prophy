import aprot

class MAC_CellReconfigurationResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TOaMLnCelId)]
	
	