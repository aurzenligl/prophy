import aprot

class SUeBufferStatus(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueIndex',TUeIndex),('crnti',TCrntiU16),('usefulDataReceived',TBooleanU8),('numBearerIdList',aprot.u8),('dtchMacSduReceived',TBooleanU8),('harqProcessNumber',THarqProcessNumberU8),('lcgIdList', aprot.bytes(size = MAX_NUM_LCG_IDS)),('bearerIdList', aprot.bytes(size = MAX_NUM_GBR_BEARER_PER_UE))]
	
	