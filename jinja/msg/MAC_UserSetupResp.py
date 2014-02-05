import aprot

class MAC_UserSetupResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('ueGroup',TUeGroup),('transactionId',TTransactionID),('spsCrnti',TCrnti),('macUserAddress',TAaSysComSicad),('raPreambleIndex',TRaPreambleIndex),('prachMaskIndex',TPrachMaskIndex),('sRbList', aprot.bytes(size = MAX_NUM_SRB_PER_USER)),('dRbList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]
	
	