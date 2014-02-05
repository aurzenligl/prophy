import aprot

class SSoundingRsUlConfigCommon(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('enableSRS',TBoolean),('srsBwConf',TSrsBandwidthConfiguration),('srsSubfrConf',TSrsSubframeConfiguration),('anSrsSimulTx',TBoolean),('srsMaxUpPts',TOaMSrsMaxUpPts)]
	
	