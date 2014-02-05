import aprot

class SRlcAmParameters(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('amRlcPollPdu',EPollPDU),('amPollBytes',EPollByte),('amRlcTimerPollReTransmit',TTimerPollReTransmit),('amRlcTimerReordering',TTimerReordering),('amRlcTimerStatusProhibit',TTimerStatusProhibit),('maxRlcReTrans',TMaxRlcReTrans)]
	
	