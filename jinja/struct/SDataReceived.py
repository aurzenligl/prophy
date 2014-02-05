import aprot

class SDataReceived(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('crnti',TCrntiU16),('ueIndex',TUeIndex)]
	
	