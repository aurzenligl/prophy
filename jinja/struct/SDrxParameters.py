import aprot

class SDrxParameters(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('drxCommEnable',EDrxCommEnable),('drxLongEnable',TBoolean),('drxStartOffset',TDrxStartOffset),('drxOnDuratT',TDrxOnDuratT),('drxInactivityT',TDrxInactivityT),('drxRetransT',TDrxRetransT),('drxLongCycle',TDrxLongCycle),('drxShortEnable',TBoolean),('drxShortCycle',TDrxShortCycle),('drxShortCycleTimer',TDrxShortCycleTimer),('smartStInactFactor',TSmartStInactFactor),('drxProfileIndex',aprot.u32),('drxConfigType',EDrxConfigType),('drxConfigId',TConfigurationId)]
	
	