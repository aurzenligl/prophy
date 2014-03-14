import prophy 
from externals import *
from globals import *


TRSW_MAX_IP_ADDR_LEN = 16
TRSW_MAX_NUM_META_PARAMS = 2
TRSW_MAX_NUM_CONNECTIONS = 40

TTrswMetaParamLen = prophy.u16
TTrswParamLen = prophy.u8
TTrswFlag = prophy.u8
TTrswFieldLen = prophy.u8
TTrswListLen = prophy.u8
TTrswListId = prophy.u16
TTrswOsaid = prophy.u32
TTrswDsaid = prophy.u32
TTrswEteid = prophy.u32
TTrswArpPriority = prophy.u8
TTrswPteid = prophy.u32
TTrswIpOctet = prophy.u8
TTrswNodeId = prophy.u16
TTrswCpId = prophy.u16
TTrswIpBitRate = prophy.u32
TTrswIpPacketSize = prophy.u16
TTrswPecUsage = prophy.u8

class ETrswMsgId(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETrswMsgId_Undefined',0), ('ETrswMsgId_GtpErq',193), ('ETrswMsgId_GtpEcf',194), ('ETrswMsgId_GtpRel',195), ('ETrswMsgId_GtpRlc',196), ('ETrswMsgId_GtpMod',197), ('ETrswMsgId_GtpMoa',198), ('ETrswMsgId_GtpMor',199), ('ETrswMsgId_GtpRes',200), ('ETrswMsgId_GtpRsc',201), ('ETrswMsgId_R3GtpErq',209), ('ETrswMsgId_R3GtpEcf',210), ('ETrswMsgId_R3GtpRel',211), ('ETrswMsgId_R3GtpRlc',212), ('ETrswMsgId_R3GtpMod',213), ('ETrswMsgId_R3GtpMoa',214), ('ETrswMsgId_R3GtpMor',215), ('ETrswMsgId_R3GtpRes',216), ('ETrswMsgId_R3GtpRsc',217)]
class ETrswQci(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETrswQci_Undefined',0), ('ETrswQci_1',1), ('ETrswQci_2',2), ('ETrswQci_3',3), ('ETrswQci_4',4)]
class ETrswFieldLen(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETrswFieldLen_Undefined',0), ('ETrswFieldLen_ipv4',4), ('ETrswFieldLen_ipv6',16)]
class ETrswParamId(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETrswParamId_Undefined',0), ('ETrswParamId_Cause',0x1), ('ETrswParamId_Osaid',0x6), ('ETrswParamId_IpLc',0x85), ('ETrswParamId_Euptid',0x87), ('ETrswParamId_Dsaid',0x88), ('ETrswParamId_Sicad',0x89), ('ETrswParamId_EnbTEID',0x8B), ('ETrswParamId_IpLp',0x8C), ('ETrswParamId_EstablishmentCause',0x8D), ('ETrswParamId_PeerTEID',0x8E), ('ETrswParamId_UniDirectional',0x91), ('ETrswParamId_Amode',0x92), ('ETrswParamId_Qarp',0x93)]
class ETrswPreemptVulnerability(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETrswPreemptVulnerability_MayBeReleased',0), ('ETrswPreemptVulnerability_MustNotBeReleased',1)]
class ETrswCompat(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETrswCompat_Undefined',0), ('ETrswCompat_Optional',0x1), ('ETrswCompat_Mandatory',0x2)]
class ETrswCause(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETrswCause_Undefined',0), ('ETrswCause_Unallocated',1), ('ETrswCause_NoRoute',3), ('ETrswCause_ExchangeRoutingError',25), ('ETrswCause_Normal',31), ('ETrswCause_NetworkOutOfOrder',38), ('ETrswCause_TemporaryFailure',41), ('ETrswCause_SwitchingEquipmentCongestion',42), ('ETrswCause_ResourceUnavailable',47), ('ETrswCause_InvalidMessage',95), ('ETrswCause_MandatoryIEMissing',96), ('ETrswCause_MessageTypeUndefined',97), ('ETrswCause_InvalidIEContents',100), ('ETrswCause_RecoveryOnTimerExpiry',102), ('ETrswCause_ParamUnrecognisedMsgDiscarded',110), ('ETrswCause_ProtocolError',111), ('ETrswCause_InsufficientTransportResources',112)]
class ETrswPreemptCapability(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETrswPreemptCapability_Allowed',0), ('ETrswPreemptCapability_NotAble',1)]
class ETrswEstablishmentCause(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETrswEstablishmentCause_NonGBRNormal',0), ('ETrswEstablishmentCause_GBRNormal',1), ('ETrswEstablishmentCause_GBREmergency',2), ('ETrswEstablishmentCause_GBRHandover',3)]
class ETrswAmode(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETrswAmode_PartialAdmittance',0), ('ETrswAmode_AllOrNothingAdmittance',1)]
class ETrswMetaParamId(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETrswMetaParamId_Undefined',0), ('ETrswMetaParamId_Cel',0xC0), ('ETrswMetaParamId_Sel',0xC1), ('ETrswMetaParamId_Uel',0xC2), ('ETrswMetaParamId_Crll',0xC3), ('ETrswMetaParamId_Srll',0xC4), ('ETrswMetaParamId_Crsl',0xC6), ('ETrswMetaParamId_Srsl',0xC7), ('ETrswMetaParamId_Cml',0xC9), ('ETrswMetaParamId_Sml',0xCA), ('ETrswMetaParamId_Uml',0xCB), ('ETrswMetaParamId_Pecl',0xCC)]

class STrswParamQarp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('paramID',ETrswParamId), ('compatibility',ETrswCompat), ('len',TTrswParamLen), ('prio',TTrswArpPriority), ('capability',ETrswPreemptCapability), ('vulnerability',ETrswPreemptVulnerability), ('qci',ETrswQci)]
class STrswMsgHeader(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dsaid',TTrswDsaid), ('msgId',ETrswMsgId), ('compatibility',ETrswCompat)]
class STrswPecEntry(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('eteid',TTrswEteid), ('usage',TTrswPecUsage)]
class STrswParamDsaid(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('paramID',ETrswParamId), ('compatibility',ETrswCompat), ('len',TTrswParamLen), ('dsaid',TTrswDsaid)]
class STrswParamOsaid(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('paramID',ETrswParamId), ('compatibility',ETrswCompat), ('len',TTrswParamLen), ('osaid',TTrswOsaid)]
class STrswParamSicad(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('paramID',ETrswParamId), ('compatibility',ETrswCompat), ('len',TTrswParamLen), ('nodeId',TTrswNodeId), ('cpId',TTrswCpId)]
class STrswParamEuptid(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('paramID',ETrswParamId), ('compatibility',ETrswCompat), ('len',TTrswParamLen), ('eteid',TTrswEteid), ('fieldLen',ETrswFieldLen), ('tmpName',TNumberOfItems), ('dspIpAddr',prophy.array(TTrswIpOctet,bound='tmpName'))]
class STrswParamEnbTEID(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('paramID',ETrswParamId), ('compatibility',ETrswCompat), ('len',TTrswParamLen), ('enbteid',TTrswEteid)]
class STrswParamPeerTEID(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('paramID',ETrswParamId), ('compatibility',ETrswCompat), ('len',TTrswParamLen), ('peerteid',TTrswPteid)]
class STrswIpLc(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('guaranteedBitRate',TTrswIpBitRate), ('maximumBitRate',TTrswIpBitRate), ('maxPacketSize',TTrswIpPacketSize), ('avgPacketSize',TTrswIpPacketSize)]
class STrswParamIpLc(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('paramID',ETrswParamId), ('compatibility',ETrswCompat), ('len',TTrswParamLen), ('ipLc',STrswIpLc)]
class STrswParamCause(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('paramID',ETrswParamId), ('compatibility',ETrswCompat), ('len',TTrswParamLen), ('cause',ETrswCause), ('diagLen',TTrswFieldLen)]
class STrswParamEstablishmentCause(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('paramID',ETrswParamId), ('compatibility',ETrswCompat), ('len',TTrswParamLen), ('cause',ETrswEstablishmentCause)]
class STrswParamIpLcDl(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('paramID',ETrswParamId), ('compatibility',ETrswCompat), ('len',TTrswParamLen), ('ipLc',STrswIpLc)]
class STrswParamIpLp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('paramID',ETrswParamId), ('compatibility',ETrswCompat), ('len',TTrswParamLen), ('qos',TTrswIpOctet), ('fieldLenEnb',ETrswFieldLen), ('tmpName',TNumberOfItems), ('enbIpAddr',prophy.array(TTrswIpOctet,bound='tmpName')), ('fieldLenPeer',ETrswFieldLen), ('tmpName',TNumberOfItems), ('peerIpAddr',prophy.array(TTrswIpOctet,bound='tmpName'))]
class STrswParamUniDirectional(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('paramID',ETrswParamId), ('compatibility',ETrswCompat), ('len',TTrswParamLen), ('flag',TTrswFlag)]
class STrswParamAmode(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('paramID',ETrswParamId), ('compatibility',ETrswCompat), ('len',TTrswParamLen), ('amode',ETrswAmode)]
class STrswConnection(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dsaid',STrswParamDsaid), ('osaid',STrswParamOsaid), ('sicad',STrswParamSicad), ('euptid',STrswParamEuptid), ('enbTEID',STrswParamEnbTEID), ('peerTEID',STrswParamPeerTEID), ('ipLc',STrswParamIpLc), ('cause',STrswParamCause), ('establishmentCause',STrswParamEstablishmentCause), ('ipLcDl',STrswParamIpLcDl), ('ipLp',STrswParamIpLp), ('uniDirectional',STrswParamUniDirectional), ('qarp',STrswParamQarp), ('amode',STrswParamAmode)]
class STrswList(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('paramID',ETrswMetaParamId), ('compatibility',ETrswCompat), ('len',TTrswMetaParamLen), ('listLen',TTrswListLen), ('listId',TTrswListId), ('tmpName',TNumberOfItems), ('pecList',prophy.array(STrswPecEntry,bound='tmpName')), ('tmpName',TNumberOfItems), ('connectionsList',prophy.array(STrswConnection,bound='tmpName'))]
class STrswMessage(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('msgHeader',STrswMsgHeader), ('uniqueParam',STrswConnection), ('tmpName',TNumberOfItems), ('paramsList',prophy.array(STrswList,bound='tmpName'))]
class TRSW_ReceiveIpcsInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('msgHeader',STrswMsgHeader), ('uniqueParam',STrswConnection), ('tmpName',TNumberOfItems), ('paramsList',prophy.array(STrswList,bound='tmpName'))]
class TRSW_SendIpcsReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('msgHeader',STrswMsgHeader), ('uniqueParam',STrswConnection), ('tmpName',TNumberOfItems), ('paramsList',prophy.array(STrswList,bound='tmpName'))]
