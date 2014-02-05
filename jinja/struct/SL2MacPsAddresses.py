import aprot

class SL2MacPsAddresses(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('numOfUeGroups',TNumberOfItems),('psUserUl', aprot.bytes(size = MAX_NUM_UEGROUP_PER_BB_POOL)),('psUserDl', aprot.bytes(size = MAX_NUM_UEGROUP_PER_BB_POOL)),('dataCtrlDLPdcchClient',TAaSysComSicad)]
	
	