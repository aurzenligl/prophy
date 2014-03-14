import prophy 
from externals import *
from globals import *
from ASN import *
from ASN import *
from DCM_MAC_PS import *
from WMP_MAC_PS import *
from DCT import *
from OAM_MERGED import *


MAX_NUM_DRB_PER_USER_FOR_UE_CONTEXT = 6
MAX_NUM_OF_PARALLEL_USER_DELETIONS = 200
MAX_NUM_OF_ROHC_PROFILES = 3
MAX_PDCP_HFN = 1048575
MAX_PDCP_SN = 4095
MAX_NUM_MEAS_REPORT_VALUE_TUP = 145
MAX_MEAS_GROUP_TYPE_ID_TUP = 2
PDCP_RECEIVE_STATUS_SIZE = 512
KEY_SIZE = 16
MAX_NUM_UE_PER_MSG = MAX_NUM_USER_PER_CELL / 8

TTupRadRohcUpwFO = prophy.u32
TTupRadRohcUpwSO = prophy.u32
TTupRadRohcAckInter = prophy.u32
TKey = prophy.u8
TPdcpHfn = prophy.u32
TPdcpSn = prophy.u32
TPdcpReceiveStatus = prophy.u8
TPdcpSnLength = prophy.u32
TPdcpDiscardTimer = prophy.u32
TQci = prophy.u32
TQciCounterGroup = prophy.u32
TS1DataRetardTimer = prophy.u32
TPathSupervisInterval = prophy.u32
TRespTime = prophy.u32
TMinUnansweredReqs = prophy.u32
TDrbIndex = prophy.u32
class EPdcpRohcProfile(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EPdcpRohcProfile_NoCompression',0), ('EPdcpRohcProfile_RtpUdpIp',0x0001), ('EPdcpRohcProfile_UdpIp',0x0002), ('EPdcpRohcProfile_Undefined',0xffff)]

TRohcProfileList = EPdcpRohcProfile
TRohcCID = prophy.u32
TRohcValue = prophy.u32

class EStatusReport(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EStatusReport_NoStatusReport',0), ('EStatusReport_eNbStatusReport',1), ('EStatusReport_UeStatusReport',2), ('EStatusReport_eNbUeStatusReport',3)]
class EIntAlgorithm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EIntAlgorithm_Null',0), ('EIntAlgorithm_Snow3G',1), ('EIntAlgorithm_AES',2), ('EIntAlgorithm_ZUC',3)]
class ECountStatus(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ECountStatus_KeyRefresh',0), ('ECountStatus_KeyMaxCount',1)]
class EEncAlgorithm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EEncAlgorithm_Null',0), ('EEncAlgorithm_Snow3G',1), ('EEncAlgorithm_AES',2), ('EEncAlgorithm_ZUC',3)]
class EIntegrityCheckResult(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EIntegrityCheckResult_Pass',0), ('EIntegrityCheckResult_Fail',1)]
class EMeasurementGroupTypeTup(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EMeasurementGroupTypeTup_DataForwarding',0), ('EMeasurementGroupTypeTup_PdcpTraffic',1)]
class EDataPathStatus(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EDataPathStatus_GTPSupervisionOk',0), ('EDataPathStatus_GTPSupervisionFailure',1)]
class EHandoverStatusFlag(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EHandoverStatusFlag_ReleaseDataForwardingTunnels',0), ('EHandoverStatusFlag_CancelHandover',1)]

class STupSecurityInformation(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('kRrcInt',TKey), ('kRrcEnc',TKey), ('kUpEnc',TKey), ('intAlgorithm',EIntAlgorithm), ('encAlgorithm',EEncAlgorithm), ('keyRefreshMargin',prophy.u32)]
class STupSrbInfoResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('srbId',TSrbId), ('messageResult',SMessageResult)]
class STupPdcpSrbInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('pdcpSnLength',TPdcpSnLength)]
class STupSrbInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('srbId',TSrbId), ('rlcMode',ERlcMode), ('pdcpInfo',STupPdcpSrbInfo)]
class STupRbInfoUserContext(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('drbId',TDrbId), ('ulPdcpSnValue',TPdcpSn), ('ulHfnValue',TPdcpHfn), ('dlPdcpSnValue',TPdcpSn), ('dlHfnValue',TPdcpHfn)]
class STupUeInfoUserContext(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueId',TUeId), ('tmpName',TNumberOfItems), ('ueRadioBearerList',prophy.array(STupRbInfoUserContext,bound='tmpName'))]
class SGtpInfoUserSetup(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('trswSicad',TAaSysComSicad), ('trswGcad',SGcadAddress), ('sGwTransportLayerAddress',STransportLayerAddress), ('enbTransportLayerAddress',STransportLayerAddress), ('sGwTeid',TGtpTeid), ('enbS1Teid',TGtpTeid), ('enbX2DlTeid',TGtpTeid), ('enbX2UlTeid',TGtpTeid), ('dscp',TDscp)]
class SPdcpRbInfoUserSetup(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tDiscard',TPdcpDiscardTimer), ('pdcpSnLength',TPdcpSnLength), ('statusReportReq',EStatusReport), ('rohcEnable',TBoolean), ('rohcProfileList',TRohcProfileList), ('rohcMaxCidDl',TRohcCID), ('rohcMaxCidUl',TRohcCID)]
class STupRbInfoUserSetup(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('drbId',TDrbId), ('rlcMode',ERlcMode), ('dataForwardingType',EDataForwarding), ('gtpInfo',SGtpInfoUserSetup), ('pdcpInfo',SPdcpRbInfoUserSetup), ('qci',TQci), ('qciCounterGroup',TQciCounterGroup), ('logicalChannelIndex',TLcp)]
class STupRbInfoResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('drbId',TDrbId), ('messageResult',SMessageResult)]
class SGtpInfoBearerSetup(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('trswSicad',TAaSysComSicad), ('trswGcad',SGcadAddress), ('sGwTransportLayerAddress',STransportLayerAddress), ('enbTransportLayerAddress',STransportLayerAddress), ('sGwTeid',TGtpTeid), ('enbS1Teid',TGtpTeid), ('dscp',TDscp), ('nullTermination',TBoolean)]
class SPdcpRbInfoBearerSetup(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tDiscard',TPdcpDiscardTimer), ('pdcpSnLength',TPdcpSnLength), ('rohcEnable',TBoolean), ('rohcProfileList',TRohcProfileList), ('rohcMaxCidDl',TRohcCID), ('rohcMaxCidUl',TRohcCID)]
class STupRbInfoBearerSetup(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('drbId',TDrbId), ('rlcMode',ERlcMode), ('gtpInfo',SGtpInfoBearerSetup), ('pdcpInfo',SPdcpRbInfoBearerSetup), ('qci',TQci), ('qciCounterGroup',TQciCounterGroup), ('logicalChannelIndex',TLcp)]
class SGtpInfoDataForwardSetup(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('targetSicad',TAaSysComSicad), ('targetGcad',SGcadAddress), ('peerEntityTransportLayerAddress',STransportLayerAddress), ('peerEntityTeid',TGtpTeid), ('dscp',TDscp)]
class STupRbInfoDataForwardSetup(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('drbId',TDrbId), ('dataForwardingType',EDataForwarding), ('gtpInfoDl',SGtpInfoDataForwardSetup), ('gtpInfoUl',SGtpInfoDataForwardSetup), ('index',TDrbIndex)]
class STupRbInfoDataForwardSetupResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('drbId',TDrbId), ('tmpName',TNumberOfItems), ('rxStatusOfUlPdcpSdus',prophy.array(u8,bound='tmpName')), ('ulHfnValue',TPdcpHfn), ('ulPdcpSnValue',TPdcpSn), ('dlHfnValue',TPdcpHfn), ('dlPdcpSnValue',TPdcpSn), ('messageResult',SMessageResult)]
class STupRbInfoPdcpEnable(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('drbId',TDrbId), ('tS1DataRetard',TS1DataRetardTimer), ('tmpName',TNumberOfItems), ('rxStatusOfUlPdcpSdus',prophy.array(u8,bound='tmpName')), ('ulHfnValue',TPdcpHfn), ('ulPdcpSnValue',TPdcpSn), ('dlHfnValue',TPdcpHfn), ('dlPdcpSnValue',TPdcpSn)]
class SGtpInfoPathSwitch(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sGwTransportLayerAddress',STransportLayerAddress), ('sGwTeid',TGtpTeid), ('trswSicad',TAaSysComSicad), ('trswGcad',SGcadAddress)]
class STupRbInfoPathSwitch(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('drbId',TDrbId), ('gtpInfo',SGtpInfoPathSwitch)]
class STupRbInfoBearerModify(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('drbId',TDrbId), ('dscp',TDscp), ('qci',TQci), ('qciCounterGroup',TQciCounterGroup), ('logicalChannelIndex',TLcp)]
class STupCoefficientValues(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('carrierBw',ECarrierBandwidth), ('cDlTup1',TCoEffValue), ('cDlTup2',TCoEffValue), ('cDlTup3',TCoEffValue), ('cUlTup1',TCoEffValue), ('cUlTup2',TCoEffValue), ('cUlTup3',TCoEffValue)]
class SRohcCellParameters(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('rohcFullHdCount',TRohcValue), ('rohcHdRefreshPeriod',TRohcValue), ('rohcK1',TRohcValue), ('rohcN1',TRohcValue), ('rohcK2',TRohcValue), ('rohcN2',TRohcValue), ('rohcHdDecomOmodeEnable',TBoolean)]
class STupDiscardParameters(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('thOverflowDiscard',TThOverflowDiscard), ('flagOverflowDiscard',TFlagOverflowDiscard), ('discBuffThrAct',TBoolean), ('discBuffHighThr',TDiscBuffThr), ('discBuffHighThrList',prophy.bytes(size=8)), ('chBw',ECarrierBandwidth)]
class TUP_CellSetupReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('primaryPLMNId',SPlmnId), ('tmpName',TNumberOfItems), ('plmnIdList',prophy.array(SPlmnId,bound='tmpName')), ('rohcCellParameters',SRohcCellParameters), ('sysTimeCorrectValue',prophy.u32), ('bufferDiscardParams',STupDiscardParameters)]
class TUP_CellSetupResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('tupUserAddress',TAaSysComSicad), ('tupSgnlSrbAddress',TAaSysComSicad), ('tupCellMeas',TAaSysComSicad)]
class TUP_CellDeleteReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId)]
class TUP_CellDeleteResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class TUP_SrbReceiveInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('srbId',TSrbId), ('rrcIntegrityCheckResult',EIntegrityCheckResult), ('tmpName',TL3MsgSize), ('srbPayload',prophy.array(u8,bound='tmpName'))]
class TUP_SrbSendReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('drxConfigId',TConfigurationId), ('srbId',TSrbId), ('respFlag',TBoolean), ('harqRespFlag',TBoolean), ('mui',TMui), ('integrityActivationPreFlag',TBoolean), ('dlCipherActivationPostFlag',TBoolean), ('tmpName',TL3MsgSize), ('l3Payload',prophy.array(u8,bound='tmpName'))]
class TUP_SrbSendResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('srbId',TSrbId), ('mui',TMui), ('tmpName',TL3MsgSize), ('l3Payload',prophy.array(u8,bound='tmpName'))]
class TUP_UserSetupReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('plmnId',SPlmnId), ('tupUserAddress',TAaSysComSicad), ('tupSgnlSrbAddress',TAaSysComSicad), ('macUserAddr',TAaSysComSicad), ('handoverType',EHandoverType), ('sourceUeId',TUeId), ('suspendUlTx',TBoolean), ('uecategory',TUeCategory), ('tmpName',TNumberOfItems), ('srbList',prophy.array(STupSrbInfo,bound='tmpName')), ('tmpName',TNumberOfItems), ('rbList',prophy.array(STupRbInfoUserSetup,bound='tmpName'))]
class TUP_UserSetupResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('tmpName',TNumberOfItems), ('srbList',prophy.array(STupSrbInfoResp,bound='tmpName')), ('tmpName',TNumberOfItems), ('rbList',prophy.array(STupRbInfoResp,bound='tmpName'))]
class TUP_UserDeleteReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class TUP_UserDeleteResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class TUP_BearerSetupReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('securityInformation',STupSecurityInformation), ('uecategory',TUeCategory), ('tmpName',TNumberOfItems), ('srbList',prophy.array(STupSrbInfo,bound='tmpName')), ('tmpName',TNumberOfItems), ('rbList',prophy.array(STupRbInfoBearerSetup,bound='tmpName'))]
class TUP_BearerSetupResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('tmpName',TNumberOfItems), ('srbList',prophy.array(STupSrbInfoResp,bound='tmpName')), ('tmpName',TNumberOfItems), ('rbList',prophy.array(STupRbInfoResp,bound='tmpName'))]
class TUP_BearerDeleteReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('tmpName',TNumberOfItems), ('srbList',prophy.array(TSrbId,bound='tmpName')), ('tmpName',TNumberOfItems), ('rbIdList',prophy.array(TDrbId,bound='tmpName'))]
class TUP_BearerDeleteResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('tmpName',TNumberOfItems), ('srbList',prophy.array(STupSrbInfoResp,bound='tmpName')), ('tmpName',TNumberOfItems), ('rbList',prophy.array(STupRbInfoResp,bound='tmpName'))]
class TUP_DataForwardSetupReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('destinationUeId',TUeId), ('transactionId',TTransactionID), ('handoverType',EHandoverType), ('dcmDlInterRatFoType',TBoolean), ('tmpName',TNumberOfItems), ('rbList',prophy.array(STupRbInfoDataForwardSetup,bound='tmpName'))]
class TUP_DataForwardSetupResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('tmpName',TNumberOfItems), ('rbList',prophy.array(STupRbInfoDataForwardSetupResp,bound='tmpName'))]
class TUP_PdcpEnableReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('handoverType',EHandoverType), ('tmpName',TNumberOfItems), ('rbList',prophy.array(STupRbInfoPdcpEnable,bound='tmpName'))]
class TUP_PdcpEnableResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('tmpName',TNumberOfItems), ('rbList',prophy.array(STupRbInfoResp,bound='tmpName'))]
class TUP_EndMarkerInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('drbId',TDrbId), ('direction',EDirection)]
class TUP_DataForwardDeleteReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('handoverStatusFlag',EHandoverStatusFlag)]
class TUP_DataForwardDeleteResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class TUP_ErrorInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('interfaceInfo',EInterfaceType), ('tmpName',TNumberOfItems), ('srbList',prophy.array(STupSrbInfoResp,bound='tmpName')), ('tmpName',TNumberOfItems), ('rbList',prophy.array(STupRbInfoResp,bound='tmpName'))]
class TUP_MaxCountInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('isSrbId',TBoolean), ('rbId',TRadioBearerId), ('countStatus',ECountStatus)]
class TUP_ProceedLockStepReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class TUP_ProceedLockStepResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class TUP_SecurityActivationReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class TUP_SecurityActivationResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class TUP_InternalAddressReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('transactionId',TTransactionID), ('ulMasterNid',TAaSysComNid), ('dlMasterNid',TAaSysComNid), ('dlSlaveNid',TAaSysComNid), ('macDataServiceNid',TAaSysComNid), ('enbId',TOaMLnBtsId)]
class TUP_InternalAddressResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('transactionId',TTransactionID)]
class TUP_DataPathStatusInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('remoteTransportLayerAddress',STransportLayerAddress), ('uPlaneIpAddress',STransportLayerAddress), ('status',EDataPathStatus)]
class TUP_NetworkConfigReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('transactionId',TTransactionID), ('dscp',TDscp), ('pdcpTxSnLimit',TBoolean), ('tmpName',TNumberOfItems), ('uPlaneIpAddress',prophy.array(STransportLayerAddress,bound='tmpName'))]
class TUP_NetworkConfigResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('transactionId',TTransactionID), ('numOfUeGroups',TNumberOfItems), ('tupGtpuReceiveAddress',prophy.bytes(size=MAX_NUM_UEGROUP_PER_BB_POOL)), ('tupGtpuReceiveEqId',prophy.bytes(size=MAX_NUM_UEGROUP_PER_BB_POOL))]
class TUP_DataPathSupervisionReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('enbcDatapathStatusAddress',TAaSysComSicad), ('trswConfigSicad',TAaSysComSicad), ('initialStatusReportRequested',TBoolean), ('uPlaneIpAddress',STransportLayerAddress), ('gtpuPathSupint',TPathSupervisInterval), ('gtpuT3Resp',TRespTime), ('gtpuN3Reqs',TMinUnansweredReqs), ('transportNwId',TTransportNetworkId), ('tmpName',TNumberOfItems), ('sgwIpAddress',prophy.array(STransportLayerAddress,bound='tmpName'))]
class TUP_DataPathSupervisionResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult)]
class TUP_CoefficientRequestReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tmpName',TNumberOfItems), ('carrierBw',prophy.array(ECarrierBandwidth,bound='tmpName'))]
class TUP_CoefficientRequestResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('tmpName',TNumberOfItems), ('coefficients',prophy.array(STupCoefficientValues,bound='tmpName'))]
class TUP_SecurityConfReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('securityInformation',STupSecurityInformation)]
class TUP_SecurityConfResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class TUP_PathSwitchReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('tmpName',TNumberOfItems), ('rbList',prophy.array(STupRbInfoPathSwitch,bound='tmpName'))]
class TUP_PathSwitchResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('tmpName',TNumberOfItems), ('rbList',prophy.array(STupRbInfoResp,bound='tmpName'))]
class TUP_MeasurementInitiationReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('measurementId',TMeasurementId), ('reportPeriod',TPeriod), ('samplingPeriod',TPeriod), ('tmpName',TNumberOfItems), ('measurementGroupTypeList',prophy.array(EMeasurementGroupTypeTup,bound='tmpName'))]
class TUP_MeasurementInitiationResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('measurementId',TMeasurementId)]
class TUP_MeasurementReportInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('measurementId',TMeasurementId), ('tmpName',TNumberOfItems), ('measGroupReportList',prophy.array(EMeasurementGroupTypeTup,bound='tmpName')), ('tmpName',TNumberOfItems), ('measReportValue',prophy.array(SMeasReportValue,bound='tmpName'))]
class TUP_MeasurementTerminationReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('measurementId',TMeasurementId)]
class TUP_MeasurementTerminationResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('measurementId',TMeasurementId)]
class TUP_ResumeReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class TUP_ResumeResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class TUP_ResumeUlTxReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class TUP_ResumeUlTxResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class TUP_BearerModifyReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('tmpName',TNumberOfItems), ('rbList',prophy.array(STupRbInfoBearerModify,bound='tmpName'))]
class TUP_BearerModifyResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('tmpName',TNumberOfItems), ('rbList',prophy.array(STupRbInfoResp,bound='tmpName'))]
class TUP_SecurityDeActivationReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class TUP_SecurityDeActivationResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class TUP_UserContextReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('transactionId',TTransactionID)]
class TUP_UserContextResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('transactionId',TTransactionID), ('tmpName',TNumberOfItems), ('ueList',prophy.array(STupUeInfoUserContext,bound='tmpName'))]
class TUP_BlockUsersReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('transactionId',TTransactionID), ('tmpName',TNumberOfItems), ('listOfUes',prophy.array(TUeId,bound='tmpName'))]
class TUP_BlockUsersResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('transactionId',TTransactionID)]
class TUP_CellReconfigReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('tmpName',TNumberOfItems), ('plmnIdList',prophy.array(SPlmnId,bound='tmpName'))]
class TUP_CellReconfigResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class TUP_UserSetPlmnReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('plmnId',SPlmnId)]
