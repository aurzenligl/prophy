import aprot

class SRlcUmParameters(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('umRlcSnFieldLengthDownlink',TSnFieldLength),('umRlcSnFieldLengthUplink',TSnFieldLength),('umTimerReordering',TTimerReordering)]
	
	