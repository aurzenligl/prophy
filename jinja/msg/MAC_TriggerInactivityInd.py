import aprot

class MAC_TriggerInactivityInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('lnCellIdScell',TOaMLnCelId),('crnti',TCrnti),('ueId',TUeId),('direction',EDirection),('trigger',TTrigger)]
	
	