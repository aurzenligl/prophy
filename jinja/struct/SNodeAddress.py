import aprot

class SNodeAddress(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ulCellMac',TAaSysComNid),('ulUeMac',TAaSysComNid),('ulSchedulerMac',TAaSysComNid),('dlCellMac',TAaSysComNid),('dlUeMac',TAaSysComNid),('dlSchedulerMac',TAaSysComNid),('cellManager',TAaSysComNid)]
	
	