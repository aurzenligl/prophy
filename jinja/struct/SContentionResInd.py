import aprot

class SContentionResInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',aprot.u16),('crnti',aprot.u16),('ueIndex',TUeIndex),('raEvent',aprot.u8),('ueContentionResolutionId',aprot.u64)]
	
	