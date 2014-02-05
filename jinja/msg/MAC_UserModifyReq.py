import aprot

class MAC_UserModifyReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('crnti',TCrnti),('ueId',TUeId),('measGapStopRequired',TBoolean),('gapPattern',EMeasGapOffset),('measGapOffset',TMeasGapOffset),('ambrParams',SAmbrParams),('drxParameters',SDrxParameters),('actNewTransmMode',ETransmMode),('cqiParams',SCqiParams),('ueInactivityTimer',TOaMInactivityTimer)]
	
	