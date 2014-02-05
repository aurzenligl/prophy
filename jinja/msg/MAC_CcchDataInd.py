import aprot

class MAC_CcchDataInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellId),('crnti',TCrnti),('ueIndex',TUeIndex),('size',TL3MsgSize),('tempUeNeeded',TBoolean),('macCeFlag',TBoolean)]
	
	