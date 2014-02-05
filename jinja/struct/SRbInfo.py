import aprot

class SRbInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('drbId',TDrbId),('drbType',EDrbType),('logicalChannelId',TLogicalChannelId),('logicalChannelGrId',TLogicalChannelGrId),('logicalChannelIndex',TLcp),('rlcMode',ERlcMode),('rlcUmParameters',SRlcUmParameters),('rlcAmParameters',SRlcAmParameters),('container',UWmpDcmRbContainer)]
	
	