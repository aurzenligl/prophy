import aprot

class MAC_RrcConnectionReconfCompletedReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('ueId',TUeId),('relatedProcedure',ERelatedProcedure),('sCellServCellIndex',TSCellServCellIndex),('cqiParams',SCqiParams),('cqiParamsScell',SCqiParamsScell),('actNewTransmMode',ETransmMode),('actNewTransmModeScell',ETransmMode)]
	
	