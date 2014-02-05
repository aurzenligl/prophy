import aprot

class MAC_RemoveUesInCellReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('pCelId',TOaMLnCelId),('ueToRemove', aprot.bytes(size = MAX_NUM_CA_UES))]
	
	