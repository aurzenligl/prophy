import aprot

class MAC_CellReconfigurationReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('activationTimeSFN',TSfn),('commonCellParams',SCommonCellParams),('phichParams',SPhichParams),('pucchParams',SPucchConfiguration),('soundingRsUlConfigCommon',SSoundingRsUlConfigCommon),('hsTrainScenario',EHsTrainScenario),('harqMaxMsg3',TOaMHarqMaxMsg3),('container',UWmpDcmCellContainer)]
	
	