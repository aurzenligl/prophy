import aprot

class EPduMuxReqType(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('EPduMuxReqType_PduMuxData',0),
	 			    ('EPduMuxReqType_CcchDataReTransmit',2),
	 			    ('EPduMuxReqType_CcchData',1)]