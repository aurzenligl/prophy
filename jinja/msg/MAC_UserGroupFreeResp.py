import aprot

class MAC_UserGroupFreeResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TOaMLnCelId),('ueId',TUeId)]
	
	