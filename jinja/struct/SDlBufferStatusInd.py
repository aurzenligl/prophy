import aprot

class SDlBufferStatusInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('amountDataOctets',aprot.u32),('amountOfRlcSduData',aprot.u32),('amountCtrlOctets',aprot.u16),('ueIndex',TUeIndex),('rbId',TRadioBearerIdU8),('lcId',TLogicalChannelIdU8),('xsfnTimeStamp',aprot.u16)]
	
	