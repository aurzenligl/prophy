import aprot

class MAC_CellSetupResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('macUser',TAaSysComSicad),('macSgnl',TAaSysComSicad),('macCellMeas',TAaSysComSicad),('macTest',TAaSysComSicad),('macUserPsService',TAaSysComSicad)]
	
	