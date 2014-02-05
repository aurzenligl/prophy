import aprot

class MAC_CaUserReconfigurationReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('crnti',TCrnti),('ueId',TUeId),('relatedProcedure',ERelatedProcedure),('aperiodicCsiTriggerParams',SAperiodicCsiTriggerParams),('container',UCaUserReconfigurationContainer),('r10n1PucchAnCsList', aprot.bytes(size = 2)),('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated),('sCellsRemove', aprot.bytes(size = 1)),('sCellsConfiguration', aprot.bytes(size = 1))]
	
	