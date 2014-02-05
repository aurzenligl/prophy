import aprot

class MAC_UserGroupFreeReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('ueId',TUeId),('ueGroup',TUeGroup)]
	
	