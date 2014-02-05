import aprot

class MAC_RlcDataRegisterReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',TUeId),('tupUserAddress',STupUserAddress)]
	
	