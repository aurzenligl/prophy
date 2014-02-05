import aprot

class MAC_UserGroupReserveResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TOaMLnCelId),('ueId',TUeId),('ueGroup',TUeGroup)]
	
	