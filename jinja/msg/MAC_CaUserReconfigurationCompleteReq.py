import aprot

class MAC_CaUserReconfigurationCompleteReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('crnti',TCrnti),('ueId',TUeId),('procedureResults',ECAProcedureResults)]
	
	