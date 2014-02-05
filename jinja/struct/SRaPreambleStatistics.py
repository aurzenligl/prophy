import aprot

class SRaPreambleStatistics(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('pdfOfRaPreamblesReceived', aprot.bytes(size = 32))]
	
	