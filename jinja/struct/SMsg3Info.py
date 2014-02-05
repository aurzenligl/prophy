import aprot

class SMsg3Info(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('crnti',TCrnti),('ueGroup',TUeGroup),('data', aprot.bytes(size = MAX_CCCH_DATA_UL))]
	
	