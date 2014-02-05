import aprot

class SSCellsConfiguration(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCellIdScell',TOaMLnCelId),('sCellServCellIndex',TSCellServCellIndex),('transmModeScell',ETransmMode),('maxNumOfLayersScell',EMaxNumOfLayers),('cqiParamsScell',SCqiParamsScell),('container',UCaWmpDcmSCellContainer)]
	
	