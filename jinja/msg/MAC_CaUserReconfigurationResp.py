import aprot

class MAC_CaUserReconfigurationResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('crnti',TCrnti),('ueId',TUeId),('sCellResultsForRemoval', aprot.bytes(size = 1)),('sCellResultsForConfiguration', aprot.bytes(size = 1)),('messageResult',SMessageResult)]
	
	