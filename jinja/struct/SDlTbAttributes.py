import aprot

class SDlTbAttributes(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('maxNumOfHarqTx',TNumHarqTransmissions),('ndiForPdcch',TNewDataIndicator)]
	
	