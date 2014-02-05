import aprot

class SRlcLcpInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('umReorderingBufferSize',TBufferSize),('umTransmitBufferSize',TBufferSize),('bufferingTimeTh',TThresholdRlcT),('rlcDiscardTh',TThresholdRlc)]
	
	