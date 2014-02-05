import aprot

class SRbModifyInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('drbId',TDrbId),('congestionWeight',aprot.u32),('qciInfo',SRbModifyQciInfo)]
	
	