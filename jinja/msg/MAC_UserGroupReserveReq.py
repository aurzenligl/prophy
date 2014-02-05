import aprot

class MAC_UserGroupReserveReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('ueId',TUeId)]
	
	