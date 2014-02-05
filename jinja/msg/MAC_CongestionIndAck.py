import aprot

class MAC_CongestionIndAck(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('cellResourceGroupId',TCellResourceGroupId),('congestionResolutionResult',SMessageResult)]
	
	