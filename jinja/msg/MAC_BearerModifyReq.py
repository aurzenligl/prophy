import aprot

class MAC_BearerModifyReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('crnti',TCrnti),('ueId',TUeId),('ttiBmMeasActivate',TBoolean),('ambrParams',SAmbrParams),('drbInfoList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]
	
	