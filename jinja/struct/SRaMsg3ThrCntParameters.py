import aprot

class SRaMsg3ThrCntParameters(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('discardingCellGroupId',TCntId),('raMsg3ThrCnt',TRaMsg3ThrCnt)]
	
	