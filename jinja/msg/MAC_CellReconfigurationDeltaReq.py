import aprot

class MAC_CellReconfigurationDeltaReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('dcmContainer',UWmpDcmCellReconfigurationContainer)]
	
	