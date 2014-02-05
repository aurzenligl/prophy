import aprot

class MAC_DefaultUserConfigReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('l3Address',TAaSysComSicad),('userInfo',SUserInfoMac)]
	
	