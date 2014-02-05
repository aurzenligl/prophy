import aprot

class MAC_UlDataReceivedResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('data', aprot.bytes(size = 1))]
	
	