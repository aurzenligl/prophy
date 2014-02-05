import aprot

class SSRbList(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('srbId',TSrbId),('messageResult',SMessageResult)]
	
	