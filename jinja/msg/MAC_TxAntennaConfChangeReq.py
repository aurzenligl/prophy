import aprot

class MAC_TxAntennaConfChangeReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('numAvailableTxAntennas',TNumAntennas)]
	
	