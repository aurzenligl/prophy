import aprot

class SUeBufferStatusWmp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('crnti',TCrnti),('ueIndex',TUeIndex),('usefulDataReceived',TBooleanU8),('lcgIdList', aprot.bytes(size = MAX_NUM_LCG_IDS))]
	
	