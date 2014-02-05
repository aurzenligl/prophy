import aprot

class SCqiParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cqiAperMode',ECqiAperMode),('cqiPerEnable',ECqiPerEnable),('numOfCqiPmi',aprot.u32),('iCqiPmi', aprot.bytes(size = MAX_NUM_OF_RI_PMI_INFORMATION)),('resourceIndexCqi',TResourceIndexCqi),('cqiPerMode',ECqiPerMode),('riEnable',TBoolean),('numOfRi',aprot.u32),('iRi', aprot.bytes(size = MAX_NUM_OF_RI_PMI_INFORMATION)),('cqiPerSimulAck',ECqiPerSimulAck),('cqiPerSbCycK',TCqiPerSbCycK),('cqiPerSbPeriodFactor',EOaMCqiPerSbPeriodFactor)]
	
	