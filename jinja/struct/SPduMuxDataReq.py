import aprot

class SPduMuxDataReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueIndex',TUeIndex),('macId',TCrntiU16),('txPower',TTxPower),('spatialMode',TSpatialMode),('numOfLayers',TNumOfLayersU8),('codebookIndex',TCodebookIndexU8),('nIr',TNIr),('resources',SPdschResources),('mimoIndicator',TBooleanU8),('servingCellIndex',TServingCellIndex),('lnCellIdServCell',TOaMLnCelId),('reqType',TEPduMuxReqTypeU8),('hasDlBfTbFormat',TBooleanU8),('dlBfTbFormat',SDlBfTbFormat),('tbFlags',aprot.u32),('cwAttributes', aprot.bytes(size = MAX_NMBR_CODEWORDS))]
	
	