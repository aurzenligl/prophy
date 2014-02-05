import aprot

class MAC_EnableSystemInfoReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('ibType',EIbType),('activationFlag',EActivationFlag)]
	
	