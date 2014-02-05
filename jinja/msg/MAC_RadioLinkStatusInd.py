import aprot

class MAC_RadioLinkStatusInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('sCellServCellIndex',TSCellServCellIndex),('srbId',TSrbId),('drbId',TDrbId),('rlsCause',ERlsCause)]
	
	