import aprot

class SDrxShortParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('drxShortEnable',TBoolean),('drxShortCycle',TDrxShortCycle),('drxShortCycleTimer',TDrxShortCycleTimer),('smartStInactFactor',TSmartStInactFactor)]
	
	