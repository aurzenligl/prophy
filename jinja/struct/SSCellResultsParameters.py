import aprot

class SSCellResultsParameters(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCellIdScell',TOaMLnCelId),('messageResult',SMessageResult)]
	
	