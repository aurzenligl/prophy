import prophy 
from externals import *
from globals import *


MAX_NUM_OF_RAD_DATA = 10
IPV4_ADDR_LEN = 4
MAX_G_PDU_SIZE = 8192
MAX_EXTENSION_HEADERS = 16
MAX_EXTENSION_HEADER_LENGTH = 64
LOM_MAX_FAULT_FILTERS = 256
LOM_FAULT_MANAGER_INIT_ACK_MSG = 32780
LOM_FAULT_MANAGER_INIT_REQ_MSG = 32779
LOM_FAULT_MONITORING_RESP_MSG = 61489
LOM_FAULT_MONITORING_REQ_MSG = 61488
MAX_NUM_OF_DYN_DATA = 255
MAX_NUM_OF_DYNAMIC_DATA = 512

TReportInterval = prophy.u32
TTimeStamp = prophy.u32
TBoard = prophy.u8
TCpu = prophy.u8
TTask = prophy.u16
TMsgLength = prophy.u16
TClientObjectHandle = prophy.u32
TLocalBrowserObjectHandle = prophy.u32
TMtuSize = prophy.u32
TCounter = prophy.u32

class EStatisticalMeas(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EStatisticalMeas_InvalidName',0), ('EStatisticalMeas_8000_LTE_S1AP',1), ('EStatisticalMeas_8001_LTE_CellLoad',2), ('EStatisticalMeas_8002_LTE_RLC',3), ('EStatisticalMeas_8003_LTE_PDCP_Data',4), ('EStatisticalMeas_8004_LTE_TransportLoad',5), ('EStatisticalMeas_8005_LTE_PowerAndQualityUL',6), ('EStatisticalMeas_8006_LTE_EPS_Bearer',7), ('EStatisticalMeas_8007_LTE_RadioBearer',8), ('EStatisticalMeas_8008_LTE_RRC',9), ('EStatisticalMeas_8009_LTE_Intra_eNB_Handover',10), ('EStatisticalMeas_8010_LTE_PowerAndQualityDL',11), ('EStatisticalMeas_8011_LTE_CellResource',12), ('EStatisticalMeas_8012_LTE_CellThroughput',13), ('EStatisticalMeas_8013_LTE_UE_State',14), ('EStatisticalMeas_8014_LTE_Inter_eNB_Handover',15), ('EStatisticalMeas_8015_LTE_NeighbourCellRelatedHandover',16), ('EStatisticalMeas_8016_LTE_InterSystemHandover',17), ('EStatisticalMeas_8017_LTE_InterSystemHandoverToUtranPerNeighbourCell',18), ('EStatisticalMeas_8018_LTE_eNB_Load',19), ('EStatisticalMeas_8019_LTE_InterSystemHandoverToGsmPerNeighbourCell',20), ('EStatisticalMeas_8020_LTE_CellAvailability',21), ('EStatisticalMeas_8021_LTE_Handover',22), ('EStatisticalMeas_8022_LTE_X2AP',23), ('EStatisticalMeas_8023_LTE_UeAndServiceDifferentiation',24), ('EStatisticalMeas_8024_LTE_NetworkSharing',25)]
class ERadParamState(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERadParamState_Ok',0), ('ERadParamState_OutOfRange',1), ('ERadParamState_Timeout',2)]
class ECountersRestart(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ECountersRestart_False',0), ('ECountersRestart_True',1)]
class EBrowserChangeType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EBrowserChangeType_Registered',0), ('EBrowserChangeType_Unregistered',1)]
class ELomMeasReportingMode(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ELomMeasReportingMode_SicapReliable',0), ('ELomMeasReportingMode_SicapUnreliable',1)]
class EObjectType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EObjectType_Unit',0), ('EObjectType_Cell',1), ('EObjectType_CellGroup',2), ('EObjectType_Bs',3), ('EObjectType_Adj',4)]
class EObjectClass(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EObjectClass_WCel',0), ('EObjectClass_LCG',1), ('EObjectClass_S1Interface',2), ('EObjectClass_X2Interface',3), ('EObjectClass_ENB',4), ('EObjectClass_Cell',5)]
class EExtensionHeaderType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EExtensionHeaderType_NoMoreExtensionHeaders',0), ('EExtensionHeaderType_MbmsSupportIndication',1), ('EExtensionHeaderType_MsInfoChangeReportingSupportIndication',2), ('EExtensionHeaderType_UdpPort',64), ('EExtensionHeaderType_PdcpPduNumber',192), ('EExtensionHeaderType_SuspendRequest',193), ('EExtensionHeaderType_SuspendResponse',194)]
class ERadSettingType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERadSettingType_FactoryDefaults',0), ('ERadSettingType_DynamicChanges',1), ('ERadSettingType_PersistentChanges',2)]
class ELomStatus(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ELomStatus_Ok',0), ('ELomStatus_Nok',1), ('ELomStatus_AlreadyRegistered',2), ('ELomStatus_UnknownObject',3), ('ELomStatus_NotEnoughMemory',4), ('ELomStatus_InvalidParameters',5)]
class ERadDomain(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERadDomain_Legacy',0), ('ERadDomain_Ccs',1), ('ERadDomain_HwApi',2), ('ERadDomain_Dft',3), ('ERadDomain_Telecom',4), ('ERadDomain_TUP',5), ('ERadDomain_DSPCodec',6), ('ERadDomain_DSPRake',7), ('ERadDomain_DSPMac_hs',8), ('ERadDomain_DSPHsupaL2',9), ('ERadDomain_LteMac',10), ('ERadDomain_LteMacUl',11), ('ERadDomain_LteMacDl',12), ('ERadDomain_LteTupUl',13), ('ERadDomain_LteTupDl',14), ('ERadDomain_LteCellC',15), ('ERadDomain_LteCommon',16), ('ERadDomain_LteEnbc',17), ('ERadDomain_LteRrom',18), ('ERadDomain_LteUec',19), ('ERadDomain_LteLom',20), ('ERadDomain_LteTupC',21), ('ERadDomain_LteUlPhy',22), ('ERadDomain_LteDlPhy',23)]
class EBrowserStatus(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EBrowserStatus_OK',0), ('EBrowserStatus_NOK',1), ('EBrowserStatus_FeatureNotSupported',2), ('EBrowserStatus_MergedToOngoing',3), ('EBrowserStatus_InvalidParameter',4), ('EBrowserStatus_ApplicationRejected',5)]
class ERecoveryState(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERecoveryState_Blocked',0), ('ERecoveryState_Idle',1), ('ERecoveryState_Running',2), ('ERecoveryState_Block',3), ('ERecoveryState_Terminating',4)]
class EBrowserRequestType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EBrowserRequestType_Get',0), ('EBrowserRequestType_Set',1)]

class SExtensionHeader(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('headerType',EExtensionHeaderType), ('tmpName',TNumberOfItems), ('undecodedExtensionHeader',prophy.array(u8,bound='tmpName'))]
class SGtpuRecovery(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('restartCounter',prophy.u32)]
class STunnelEndpointIdentifierDataI(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tunnelEndpointIdentifierDataI',prophy.u32)]
class SGsnAddress(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tmpName',TNumberOfItems), ('gsnAddress',prophy.array(u8,bound='tmpName'))]
class SPrivateExtension(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('extensionIdentifier',prophy.u32), ('tmpName',TNumberOfItems), ('extensionValue',prophy.array(u8,bound='tmpName'))]
class SGtpuHeader(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sinPort',prophy.u16), ('sinAddr',prophy.bytes(size=IPV4_ADDR_LEN)), ('tunnelEndpointIdentifier',prophy.u32), ('sequenceNumber',prophy.u32), ('nPduNumber',prophy.u32), ('tmpName',TNumberOfItems), ('extensionHeaders',prophy.array(SExtensionHeader,bound='tmpName'))]
class SBrowserObjectInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('objectName',EBrowserObjectName), ('objectId',TBrowserObjectId), ('objectHandle',TLomHandle)]
class SBrowserRequestor(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('board',TBoard), ('cpu',TCpu), ('task',TTask)]
class SAaTime1(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('year',prophy.u32), ('month',prophy.u32), ('day',prophy.u32), ('hour',prophy.u32), ('minute',prophy.u32), ('second',prophy.u32), ('millisec',prophy.u32)]
class SFaultFiltering(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('faultId',EFaultId), ('blocked',TBoolean), ('faultDetectionWindow',TCounter), ('faultIndFrequency',TCounter), ('recoveryState',ERecoveryState)]
class SSetRadParamReqData(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('index',prophy.u32), ('size',prophy.u32), ('paramterValue',prophy.u32)]
class GTPU_EchoReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('header',SGtpuHeader), ('privateExtension',SPrivateExtension)]
class GTPU_EchoResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('header',SGtpuHeader), ('recovery',SGtpuRecovery), ('privateExtension',SPrivateExtension)]
class GTPU_SupportedExtensionHeadersNotif(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('header',SGtpuHeader), ('tmpName',TNumberOfItems), ('extensionHeaderTypeList',prophy.array(EExtensionHeaderType,bound='tmpName'))]
class GTPU_ErrorInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('header',SGtpuHeader), ('tunnelEndpointIdentifierDataI',STunnelEndpointIdentifierDataI), ('gsnAddress',SGsnAddress), ('privateExtension',SPrivateExtension)]
class GTPU_EndMarkerInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('header',SGtpuHeader), ('tmpName',TNumberOfItems), ('gPdu',prophy.array(u8,bound='tmpName'))]
class GTPU_GPduReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('header',SGtpuHeader), ('tmpName',TNumberOfItems), ('gPdu',prophy.array(u8,bound='tmpName'))]
class LOM_BrowserUnregisterReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfHandles',TNumberOfItems), ('handles',prophy.array(TDynamicData,bound='numOfHandles'))]
class LOM_FaultInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('faultId',EFaultId), ('faultState',EFaultState), ('faultSeverity',EFaultSeverity), ('locationtype',EFaultLocationType), ('faultLocation',prophy.u32), ('extraFaultInfo',prophy.bytes(size=MAX_NUM_OF_FAULT_INFO))]
class LOM_MtuSizeConfigReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('internalMtuSize',TMtuSize)]
class LOM_MtuSizeConfigResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('status',EStatus)]
class LOM_PmServiceAvailInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sicad',prophy.u32)]
class LOM_PmServiceMeasTypeReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('spare',prophy.u32)]
class LOM_PmServiceMeasTypeResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfMeasTypes',TNumberOfItems), ('measTypes',prophy.array(TDynamicData,bound='numOfMeasTypes'))]
class LOM_PmValuesQueryReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('objectHandle',TLocalBrowserObjectHandle), ('clientObjectHandle',TClientObjectHandle), ('measId',EStatisticalMeas), ('resetNeeded',ECountersRestart)]
class LOM_PmValuesQueryResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('objectHandle',TLocalBrowserObjectHandle), ('measId',EStatisticalMeas), ('numOfCounters',TNumberOfItems), ('counterValues',prophy.array(TDynamicData,bound='numOfCounters'))]
class LOM_LteBrowserConnectionReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('clientName',EBrowserObjectName), ('measurementReportingMode',ELomMeasReportingMode), ('changeNotifFlag',TBoolean)]
class LOM_LteBrowserConnectionResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('status',EBrowserStatus), ('sessionId',TLomSessionId)]
class LOM_LteBrowserDisconnectionReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sessionId',TLomSessionId)]
class LOM_LteBrowserDisconnectionResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('status',EBrowserStatus), ('sessionId',TLomSessionId)]
class LOM_LteBrowserListReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('listName',EBrowserObjectName), ('contextId',TBrowserContextId), ('procedureId',TBrowserProcedureId), ('sessionId',TLomSessionId), ('objectHandler',TLomHandle)]
class LOM_LteBrowserObjectsReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('contextId',TBrowserContextId), ('procedureId',TBrowserProcedureId), ('sessionId',TLomSessionId), ('parentObjectHandle',TLomHandle)]
class LOM_LteBrowserObjectStateChangeNotif(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sessionId',TLomSessionId), ('changeType',EBrowserChangeType), ('parentObjectHandle',TLomHandle), ('objectData',SBrowserObjectInfo)]
class LOM_LteBrowserStartReportResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('reportName',EBrowserObjectName), ('status',EBrowserStatus), ('contextId',TBrowserContextId), ('procedureId',TBrowserProcedureId), ('sessionId',TLomSessionId)]
class LOM_LteBrowserStopReportReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('reportName',EBrowserObjectName), ('contextId',TBrowserContextId), ('procedureId',TBrowserProcedureId), ('sessionId',TLomSessionId), ('objectHandler',TLomHandle)]
class LOM_LteBrowserStopReportResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('reportName',EBrowserObjectName), ('status',EBrowserStatus), ('contextId',TBrowserContextId), ('procedureId',TBrowserProcedureId), ('sessionId',TLomSessionId)]
class LOM_LteBrowserObjectsResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('status',EBrowserStatus), ('contextId',TBrowserContextId), ('procedureId',TBrowserProcedureId), ('sessionId',TLomSessionId), ('sizeOfDynamicDataObject',TNumberOfItems), ('tmpName',TNumberOfItems), ('dynamicData',prophy.array(SBrowserObjectInfo,bound='tmpName'))]
class LOM_LteBrowserStartReportReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('requestor',SBrowserRequestor), ('reportName',EBrowserObjectName), ('contextId',TBrowserContextId), ('procedureId',TBrowserProcedureId), ('sessionId',TLomSessionId), ('itemCollectCount',TNumberOfItems), ('reportPeriod',TReportInterval), ('reportingDuration',TNumberOfItems), ('objectHandler',TLomHandle), ('tmpName',TNumberOfItems), ('dynamicData',prophy.array(TDynamicData,bound='tmpName'))]
class LOM_LteBrowserReportInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('timeStamp',SAaTime1), ('reportName',EBrowserObjectName), ('contextId',TBrowserContextId), ('procedureId',TBrowserProcedureId), ('sessionId',TLomSessionId), ('sizeOfDynamicDataObject',TNumberOfItems), ('tmpName',TNumberOfItems), ('dynamicData',prophy.array(u32,bound='tmpName'))]
class LOM_LteBrowserListResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('status',EBrowserStatus), ('contextId',TBrowserContextId), ('procedureId',TBrowserProcedureId), ('sessionId',TLomSessionId), ('sizeOfDynamicDataObject',TNumberOfItems), ('tmpName',TNumberOfItems), ('dynamicData',prophy.array(EBrowserObjectName,bound='tmpName'))]
class LOM_FaultManagerInitReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('recAddressForFaults',prophy.u32), ('blockAllFaults',TBoolean), ('numberOfFaultFilteringElements',TCounter), ('faultFiltering',prophy.array(SFaultFiltering,bound='numberOfFaultFilteringElements'))]
class LOM_FaultManagerInitAck(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('status',EStatus)]
class LOM_FaultReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('faultId',EFaultId), ('faultyUnit',prophy.u32), ('faultySubUnit',prophy.u32), ('faultyCpid',prophy.u32), ('faultState',EFaultState), ('faultSeverity',EFaultSeverity), ('objectType',ELomMeasReportingMode), ('detectingUnit',prophy.u32), ('detectingSubUnit',prophy.u32), ('faultInfo',prophy.bytes(size=MAX_NUM_OF_FAULT_INFO))]
class LOM_FaultAck(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('faultId',EFaultId), ('faultState',EFaultState)]
class RAD_SetRadParamsReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('btsSwSystemComponent',ERadDomain), ('radSettingType',ERadSettingType), ('tmpName',TNumberOfItems), ('data',prophy.array(SSetRadParamReqData,bound='tmpName'))]
class RAD_SetRadParamsResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('btsSwSystemComponent',ERadDomain), ('radParamState',ERadParamState)]
