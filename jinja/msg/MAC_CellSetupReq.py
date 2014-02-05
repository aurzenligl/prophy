import aprot

class MAC_CellSetupReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('phyCellId',TPhyCellId),('commonCellParams',SCommonCellParams),('phichParams',SPhichParams),('pucchParams',SPucchConfiguration),('soundingRsUlConfigCommon',SSoundingRsUlConfigCommon),('hsTrainScenario',EHsTrainScenario),('harqMaxMsg3',TOaMHarqMaxMsg3),('bufferDiscardParams',SBufferDiscardParams),('voLteThresholdParams',SVoLteThresholdParams),('rlcDlLcpInfo', aprot.bytes(size = MAX_NUM_OF_LCP_DCM)),('container',UWmpDcmCellContainer)]
	
	