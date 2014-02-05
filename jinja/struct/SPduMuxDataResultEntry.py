import aprot

class SPduMuxDataResultEntry(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('crnti',TCrntiU16),('ueIndex',TUeIndex),('cw0',EPduMuxDataResultCause),('cw1',EPduMuxDataResultCause)]
	
	