import aprot

class SDRbList(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('drbId',TDrbId),('messageResult',SMessageResult)]
	
	