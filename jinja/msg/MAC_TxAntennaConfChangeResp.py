import aprot

class MAC_TxAntennaConfChangeResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId)]
	
	