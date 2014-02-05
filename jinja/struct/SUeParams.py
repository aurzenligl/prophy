import aprot

class SUeParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('transmMode',ETransmMode),('accessStratumRelease',EUeRelease),('ueHoParams',SUeHoParams)]
	
	