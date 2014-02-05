import aprot

class MAC_BackOffIndIndexUpdateInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('container',UBackoffIndIndexUpdateIndContainer)]
	
	