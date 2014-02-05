import aprot

class MAC_DisableDiscTimerInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',TUeId),('ueIndex',TUeIndex)]
	
	