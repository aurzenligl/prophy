import aprot

class MAC_UeInfoResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TOaMLnCelId),('ueId',TUeId),('ueInfo',UUeInfo)]
	
	