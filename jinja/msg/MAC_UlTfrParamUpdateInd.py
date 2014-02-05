import aprot

class MAC_UlTfrParamUpdateInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('container',UUlTfrParamContainer)]
	
	