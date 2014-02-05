import aprot

class MAC_BearerModifyResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TOaMLnCelId),('crnti',TCrnti),('ueId',TUeId)]
	
	