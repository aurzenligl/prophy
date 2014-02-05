import aprot

class MAC_ResumeDiscTimerInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',TUeId),('ueIndex',TUeIndex)]
	
	