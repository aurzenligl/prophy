import aprot

class SCommonCellParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lCelId',TLocalCellResId),('dlChBw',ECarrierBandwidth),('ulChBw',ECarrierBandwidth),('pMax',TMaxTxPower),('dlPhyDataAddress',TAaSysComSicad),('ulPhyDataAddress',TAaSysComSicad),('maxNrSymPdcch',TOaMMaxNrSymPdcch),('taTimer',ETimeAlignTimer),('taMaxOffset',TTaMaxOffset),('dlMimoMode',EDlMimoMode),('cycPrefixDl',TCycPrefix),('cycPreFixUl',TCycPrefix),('frameConfTdd',SFrameConfTdd)]
	
	