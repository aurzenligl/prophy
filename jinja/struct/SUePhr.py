import aprot

class SUePhr(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueIndex',TUeIndex),('paddingUeIndex',aprot.u16),('crnti',aprot.u16),('powerLevel',aprot.u16)]
	
	