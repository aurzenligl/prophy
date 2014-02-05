import aprot

class SSrbInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('srbId',TSrbId),('logicalChannelId',TLogicalChannelId),('logicalChannelGrId',TLogicalChannelGrId),('logicalChannelIndex',TLcp),('rlcMode',ERlcMode),('rlcAmParameters',SRlcAmParameters),('container',UWmpDcmSrbContainer)]
	
	