import aprot

class MAC_StartUlTestModelReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('referenceChannelNumber',EReferenceChannelNumber),('resourceBlockOffset',TResourceBlock),('reportingTimeInterval',TReportingTimeInterval),('harqUsed',TBoolean),('digitalOutputEnabled',TBoolean),('ulTestModelDigitalOutputParams',SUlTestModelsDigitalOutputParams),('additionalMeasurementParameters',UAdditionalMeasurementParameters)]
	
	