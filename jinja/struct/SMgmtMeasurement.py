import aprot

class SMgmtMeasurement(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('val',aprot.u32),('offsetInGroup',aprot.u16),('groupId',aprot.u8),('status',aprot.u8)]
	
	