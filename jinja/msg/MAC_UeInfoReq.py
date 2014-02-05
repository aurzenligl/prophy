import aprot

class MAC_UeInfoReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('ueId',TUeId),('ueInfo',EUeInfo)]
	
	