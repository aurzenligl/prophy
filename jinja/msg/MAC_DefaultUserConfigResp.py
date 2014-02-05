import aprot

class MAC_DefaultUserConfigResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('nodeAddress', aprot.bytes(size = MAX_NUM_OF_L2DEPLOYABLE_NODE))]
	
	