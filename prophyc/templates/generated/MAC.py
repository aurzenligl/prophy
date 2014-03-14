import prophy 
from externals import *
from globals import *
from OAM_MERGED import *
from DCM_MAC_PS import *
from WMP_MAC_PS import *

UUlTfrParamContainer = prophy.i32
UBackoffIndIndexUpdateIndContainer = prophy.i32
UDedicRaPreParams = prophy.i32
UUeStatusReportRespContainerDcm = prophy.i32
UAdditionalMeasurementParameters = prophy.i32
UUlResCtrlParamContainer = prophy.i32
UWmpDcmUlResCtrlParamsContainer = prophy.i32
USystemInfoContainer = prophy.i32
UUlPowerControlUpdateIndContainer = prophy.i32
UWmpDcmSrbContainer = prophy.i32
UCaWmpDcmSCellContainer = prophy.i32
UlCtrlChannelMeasReportContainer = prophy.i32
UCaUserReconfigurationContainer = prophy.i32
UUeInfo = prophy.i32
UWmpDcmCellReconfigurationContainer = prophy.i32
UMeasGapOffset = prophy.i32
UUlCtrlChannelParams = prophy.i32
UCrntiParams = prophy.i32
UWmpDcmRbContainer = prophy.i32
UWmpDcmCellContainer = prophy.i32
UWmpDcmUserContainer = prophy.i32

SIZE_OF_SCELL_PARAMS_TABLE_DCM = 4
MAX_NUM_OF_TESTABILITY_SERVICES = 2
MAX_NUM_CA_UES = 50
MAX_NMBR_TRANSPORTBLOCKS = 2
MAX_NUM_CONT_RES_PER_MSG = 14
MAX_RB_PER_USER = 8
MAX_NUM_OF_SRB0_IN_TTI = 8
MAX_NUM_OF_SIS_IN_TTI = 1
MAX_NUM_OF_RA_RESP_IN_TTI = 8
MAX_NUM_OF_PRBS = 100
MAX_NUM_OF_PAGING_IN_TTI = 1
MAX_NUM_OF_CODEWORDS = 2
MAX_NUM_LCG_IDS = 4
MAX_NUM_GBR_BEARER_PER_UE = 3
MAX_PARALLEL_PREAMBLES_DCM = 64
MAX_PARALLEL_PREAMBLES_WMP_TDD = 10
UL_BSR_PARAM_NOT_PRESENT = 0xFFFFFFFF
TRACE_ID_TA = 4
TRACE_ID_RLC = 1
TRACE_ID_MAC = 2
SRB2 = 2
SRB1 = 1
SRB0 = 0
SIZE_OF_PADDING_HEADER = 1
SIZE_OF_MAC_SUBHEADER_7BIT_L_FIELD = 2
SIZE_OF_CRI_ELEMENT = 6
NBR_OF_BYTES_IN_KILOBYTE = 1000
MIN_CRNTI = 0x3D
MGMT_ASYNC_MESSAGE_TIMER_DURATION = 1000000
MAX_UE_CATEGORY = 8
MIN_UE_CATEGORY = 1
MAX_TRANSACTION_ID = 65535
MAX_TEMPORARY_UE_COUNT = 1000
MAX_SUPPORTED_TRACE_PROTOCOL = 7
MAX_RA_PREAMBLES = 64
MAX_NUMBER_OF_DCT_MEASUREMENT_SETS = 18
MAX_NUM_OF_SIMULT_MEAS_IN_TWO_CELLS = 30
MAX_NUM_OF_DRBS = 8
MAX_NBR_OF_RB_IDS = 35
MAX_DL_BUFF_STATUS_IND = 200
MAX_CRNTI = 65523
MAX_CELL_ID = 65535
MAC_MESSAGE_RECEIVE_INTERVAL = 2000000
LTE_MIB_BIT_LENGTH = 24
LTE_MAC_UL_CORE_UE_STACK_SIZE = 4096
LTE_MAC_FRAME_CYCLE = 1024
LTE_MAC_DL_SUPPORT_CELL_STACK_SIZE = 4096
LTE_MAC_DL_CORE_CELL_STACK_SIZE = 4096
INVALID_VALUE = 0xFFFFFFFF
INVALID_UE_IDI16 = 0x8000
INVALID_UE_ID = 0xFFFF
INVALID_TIMER_ID = 0xFFFFFFFF
INVALID_SICAD = 0xFFFFFFFF
INVALID_ROUTING_INDEX = 0xFFFFFFFF
INVALID_MEAS_ID = 0xFFFFFFFF
INVALID_MAC_SDU_SIZE = 0xFFFFFFFF
INVALID_LCID = 0xFFFFFFFF
INVALID_INDEX = 0xFFFFFFFF
INVALID_ID = 0xFFFFFFFF
INVALID_HP_ID = 0xFFFFFFFF
INVALID_CRNTI = 0xFFFFFFFF
INVALID_CELL_ID = 0xFFFFFFFF
IMMEDIATE_DCTSTART_SFN = 0xFFFFFFFF
DEFAULT_UE_CATEGORY = 1
MAX_NUM_OF_USERS_IN_TTI = 20
MAX_NUM_OF_RELEASED_UES = 8
SIZE_RINGBUF_PAYLOAD_UL = 9016
MAX_RINGBUF_CTRL_UL = 15
SIZE_RINGBUF_PAYLOAD_DL = 9016
MAX_RINGBUF_CTRL_DL = 12
MAX_NUM_OF_RI_PMI_INFORMATION = 2
MAX_NUM_SENDRESP_PACKET_IDS = 11
MAX_NUM_PACKET_IDS = 19
MAX_NUM_MEAS_REPORT_VALUE_MAC_WMP = 1820
MAX_NUM_MEAS_REPORT_VALUE_MAC = 2278
MAX_MEAS_GROUP_TYPE_ID_MAC_WMP = 6
MAX_MSG3_PER_TTI = 16
MAX_MEAS_GROUP_TYPE_ID_MAC = MAX_MEAS_GROUP_TYPE_ID
LTE_MAC_DL_CORE_CELL_EU_PRIORITY = EU_PRIORITY_11
LTE_MAC_DL_SUPPORT_CELL_EU_PRIORITY = EU_PRIORITY_20
LTE_MAC_UL_CORE_UE_EU_PRIORITY = EU_PRIORITY_15
MAC_TTI_TRACE_BUFFER_SIZE = (50*MAX_NUM_OF_USERS_IN_TTI)
MAX_NUM_OF_SIMULT_MEAS_IN_ONE_CELL = (MAX_NUM_OF_SIMULT_MEAS_IN_TWO_CELLS / 2)
MAX_UE_ID = (MAX_NUM_USER_ID_PER_ENB-1)
RA_RESP_MAX_UES = MAX_NUM_OF_USERS_IN_TTI
RA_RESP_DATA_SIZE = (2*RA_RESP_MAX_UES)
MAX_NUM_OF_DATA_RECEIVED_IND = MAX_NUM_OF_USERS_IN_TTI

TPacketId = prophy.u32
TLogicalChannelId = prophy.u32
TLogicalChannelGrId = prophy.u32
TMaxRlcReTrans = prophy.u32
TSnLength = prophy.u32
TPrachPreAmpl = prophy.u32
TRaNondedPreamb = prophy.u32
TPwrRampSetup = prophy.u32
TPrachTranmitPowerSetting = prophy.u32
TSnFieldLength = prophy.u32
TAmbr = prophy.u32
TTrigger = prophy.u32
TSiRepetition = prophy.u32
TRaPreambleIndex = prophy.u32
TRaRequestParameters = prophy.u32
TM = prophy.u32
TOffsetO = prophy.i32
TTaMaxOffset = prophy.u32
TDrxStartOffset = prophy.u32
TDrxOnDuratT = prophy.u32
TDrxInactivityT = prophy.u32
TDrxRetransT = prophy.u32
TDrxLongCycle = prophy.u32
TSrsBandwidth = prophy.u32
TFrequencyDomainPosition = prophy.u32
TSrsHoppingBw = prophy.u32
TSrsConfIndex = prophy.u32
TTransmissionComb = prophy.u32
TCyclicShift = prophy.u32
TReferenceChannelNumber = prophy.u32
TSrsSubframeConfiguration = prophy.u32
TSrsBandwidthConfiguration = prophy.u32
TMibSfnLength = prophy.u32
TMibSfnPosition = prophy.u32
TCycPrefix = prophy.u32
TBcchModPeriodNumber = prophy.u32
TBcchModPeriodLength = prophy.u32
TPrachMaskIndex = prophy.u32
TRaMsg3Thr = prophy.u32
TRntiTimer = prophy.u32
TBufferSize = prophy.u32
TThresholdRlc = prophy.u32
TThresholdRlcT = prophy.u32
TTpcRnti = prophy.u32
TTpcIndex = prophy.u32
TTimingAdvanceType2 = prophy.u32
TTimerRaComp = prophy.u32
TDataSize = prophy.u32
TDrxShortCycle = prophy.u32
TDrxShortCycleTimer = prophy.u32
TSmartStInactFactor = prophy.u32
TUeIdU16 = prophy.u16
TCellIdU16 = prophy.u16
TLogicalChannelIdU16 = prophy.u16
TNumBytesU16 = prophy.u16
TTfi = prophy.u32
TPagingMsgId = prophy.u32
TRadioBearerIdU8 = prophy.u8
TLogicalChannelIdU8 = prophy.u8
TMeasurementReportId = prophy.u32
TLogicalChannelGrIdU8 = prophy.u8
TCaCeValue = prophy.u8
TTaCeValue = prophy.u32
TServingCellIndex = prophy.u8
TMacTimerId = prophy.u32
TSpatialMode = prophy.u8
TNumOfLayersU8 = prophy.u8
TCodebookIndexU8 = prophy.u8
TCodeWordIndexU8 = prophy.u8
TMcs = prophy.u8
TEPduMuxReqTypeU8 = prophy.u8
TRaMsg3ThrLow = prophy.u32
TFlagCcchPriority = prophy.u32
TAperiodicCsiTrigger = prophy.u8
TNumOfLch = prophy.u32
TRaMsg3ThrCnt = prophy.u32
TRaMsg3ThrLowCnt = prophy.u32
TCntId = prophy.u32

class EMeasurementGroupTypeWmp(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EMeasurementGroupTypeWmp_NotDefined',0), ('EMeasurementGroupTypeWmp_GBR_load_cell_DL',1), ('EMeasurementGroupTypeWmp_GBR_load_cell_UL',2), ('EMeasurementGroupTypeWmp_GBR_load_UE_DL',3), ('EMeasurementGroupTypeWmp_GBR_load_UE_UL',4), ('EMeasurementGroupTypeWmp_nonGBR_load_cell_DL',5), ('EMeasurementGroupTypeWmp_Pdcch_load_cell',6), ('EMeasurementGroupTypeWmp_Last',7)]
class ERaContResoT(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERaContResoT_NotDefined',0), ('ERaContResoT_sf8',8), ('ERaContResoT_sf16',16), ('ERaContResoT_sf24',24), ('ERaContResoT_sf32',32), ('ERaContResoT_sf40',40), ('ERaContResoT_sf48',48), ('ERaContResoT_sf56',56), ('ERaContResoT_sf64',64), ('ERaContResoT_DCM',2000), ('ERaContResoT_DCM_SCT',3200)]
class ERaPreambGrASize(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERaPreambGrASize_NotConfigured',0), ('ERaPreambGrASize_n4',4), ('ERaPreambGrASize_n8',8), ('ERaPreambGrASize_n12',12), ('ERaPreambGrASize_n16',16), ('ERaPreambGrASize_n20',20), ('ERaPreambGrASize_n24',24), ('ERaPreambGrASize_n28',28), ('ERaPreambGrASize_n32',32), ('ERaPreambGrASize_n36',36), ('ERaPreambGrASize_n40',40), ('ERaPreambGrASize_n44',44), ('ERaPreambGrASize_n48',48), ('ERaPreambGrASize_n52',52), ('ERaPreambGrASize_n56',56), ('ERaPreambGrASize_n60',60)]
class EMeasurementGroupType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EMeasurementGroupType_NotDefined',0), ('EMeasurementGroupType_PRACH_UsageRatio',1), ('EMeasurementGroupType_Transmitted_And_Received_Power',2), ('EMeasurementGroupType_MAC_PDU_Transmission_Rate',3), ('EMeasurementGroupType_Nbr_Of_DRX_UE',4), ('EMeasurementGroupType_RLC_PDCP_Traffic',5), ('EMeasurementGroupType_Persistent_RB_Usage',6), ('EMeasurementGroupType_Channel_Usage_Status',7), ('EMeasurementGroupType_Interference_Level',8), ('EMeasurementGroupType_Pathloss',9), ('EMeasurementGroupType_Nbr_LogCH_Meas_Type1',10), ('EMeasurementGroupType_Nbr_LogCH_Meas_Type2',11), ('EMeasurementGroupType_Nbr_LogCH_Meas_Type3',12), ('EMeasurementGroupType_BB_Resource_Room',13), ('EMeasurementGroupType_PHICH_Transmit_Power',14), ('EMeasurementGroupType_RaPreambleStatistics',15), ('EMeasurementGroupType_Resource_Block_Usage_Ratio',16), ('EMeasurementGroupType_PDCCH_Usage_Ratio',17), ('EMeasurementGroupType_MAC_SDU_Transmission_And_Reception_Rate',18), ('EMeasurementGroupType_Number_Of_Voice_UE',19), ('EMeasurementGroupType_PRACH_UsageRatio_2',20), ('EMeasurementGroupType_SCell_Status',21), ('EMeasurementGroupType_Channel_Usage_Status2',22)]
class EUeRelease(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EUeRelease_Rel8',0), ('EUeRelease_Rel9',1), ('EUeRelease_Rel10',2), ('EUeRelease_Undefined',0xFFFF)]
class EPollPDU(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EPollPDU_p4',0), ('EPollPDU_p8',1), ('EPollPDU_p16',2), ('EPollPDU_p32',3), ('EPollPDU_p64',4), ('EPollPDU_p128',5), ('EPollPDU_p256',6), ('EPollPDU_pInfinity',7)]
class ERaRespWinSize(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERaRespWinSize_NotDefined',0), ('ERaRespWinSize_sf2',2), ('ERaRespWinSize_sf3',3), ('ERaRespWinSize_sf4',4), ('ERaRespWinSize_sf5',5), ('ERaRespWinSize_sf6',6), ('ERaRespWinSize_sf7',7), ('ERaRespWinSize_sf8',8), ('ERaRespWinSize_sf10',10)]
class ESysInfoTypeId(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ESysInfoTypeId_MIB',0), ('ESysInfoTypeId_SIB1',1), ('ESysInfoTypeId_SI_2',2), ('ESysInfoTypeId_SI_3',3), ('ESysInfoTypeId_SI_4',4), ('ESysInfoTypeId_SI_5',5), ('ESysInfoTypeId_SI_6',6), ('ESysInfoTypeId_SI_7',7), ('ESysInfoTypeId_SI_8',8), ('ESysInfoTypeId_SI_9',9), ('ESysInfoTypeId_SI_10',10), ('ESysInfoTypeId_SI_11',11), ('ESysInfoTypeId_SI_12',12), ('ESysInfoTypeId_SI_13',13), ('ESysInfoTypeId_SI_14',14), ('ESysInfoTypeId_SI_15',15), ('ESysInfoTypeId_SI_16',16)]
class ENoOfHarqTransmissions(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ENoOfHarqTransmissions_Undefined',0), ('ENoOfHarqTransmissions_1',1), ('ENoOfHarqTransmissions_2',2), ('ENoOfHarqTransmissions_3',3), ('ENoOfHarqTransmissions_4',4), ('ENoOfHarqTransmissions_5',5), ('ENoOfHarqTransmissions_6',6), ('ENoOfHarqTransmissions_7',7), ('ENoOfHarqTransmissions_8',8), ('ENoOfHarqTransmissions_10',10), ('ENoOfHarqTransmissions_12',12), ('ENoOfHarqTransmissions_16',16), ('ENoOfHarqTransmissions_20',20), ('ENoOfHarqTransmissions_24',24), ('ENoOfHarqTransmissions_28',28)]
class EDrbType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EDrbType_Gbr',0), ('EDrbType_NonGBR',1), ('EDrbType_Signalling',2), ('EDrbType_Gbr_Voice',3), ('EDrbType_NonGbr_Voice',4)]
class EPagingNB(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EPagingNB_FourT',0), ('EPagingNB_TwoT',1), ('EPagingNB_OneT',2), ('EPagingNB_HalfT',3), ('EPagingNB_QuarterT',4), ('EPagingNB_OneEighthT',5), ('EPagingNB_OneSixteenthT',6), ('EPagingNB_OneThirtySecondT',7)]
class EPduMuxDataResultCause(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EPduMuxDataResultCause_ResultOk',0), ('EPduMuxDataResultCause_TooLatePhase1',1), ('EPduMuxDataResultCause_TooLatePhase2',2), ('EPduMuxDataResultCause_Other',3), ('EPduMuxDataResultCause_NotRequested',4), ('EPduMuxDataResultCause_NotEnoughData',5)]
class EUeInfo(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EUeInfo_Undefined',0), ('EUeInfo_TAT2',1)]
class ECATypeOfOperation(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ECATypeOfOperation_CaCellSetup',0), ('ECATypeOfOperation_CaCellDelete',1)]
class ERelatedProcedure(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERelatedProcedure_sCellConfiguration',0), ('ERelatedProcedure_RA_SR',1), ('ERelatedProcedure_InSync',2), ('ERelatedProcedure_SCellRelease',3), ('ERelatedProcedure_TmSwitch',4), ('ERelatedProcedure_sCellConfigurationByHO',5)]
class ESchedulingTag(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ESchedulingTag_BroadcastPagingRachResponse',0), ('ESchedulingTag_Msg4CSS',1), ('ESchedulingTag_PreambleAssignmentCSS',2), ('ESchedulingTag_UlReTx',3), ('ESchedulingTag_Msg4USS',4), ('ESchedulingTag_PreambleAssignmentUSS',5), ('ESchedulingTag_DlReTx',6), ('ESchedulingTag_UlSr',7), ('ESchedulingTag_SemiPersistent',8), ('ESchedulingTag_DrxPrioritised',9), ('ESchedulingTag_SrbAllocation',10), ('ESchedulingTag_GbrAllocation',11), ('ESchedulingTag_DelaySensitiveAllocation',12), ('ESchedulingTag_NewAllocation',13), ('ESchedulingTag_ProactiveAssignment',14), ('ESchedulingTag_Qci234',15), ('ESchedulingTag_INVALID_SCHEDULING_TAG',16)]
class EPollByte(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EPollByte_kb25',0), ('EPollByte_kb50',1), ('EPollByte_kb75',2), ('EPollByte_kb100',3), ('EPollByte_kb125',4), ('EPollByte_kb250',5), ('EPollByte_kb375',6), ('EPollByte_kb500',7), ('EPollByte_kb750',8), ('EPollByte_kb1000',9), ('EPollByte_kb1250',10), ('EPollByte_kb1500',11), ('EPollByte_kb2000',12), ('EPollByte_kb3000',13), ('EPollByte_kbInfinity',14)]
class EIbType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EIbType_MIB',0), ('EIbType_SIB',1), ('EIbType_MIB_SIB',2)]
class ERlcDataSendRespCause(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERlcDataSendRespCause_RlcTransStatusOk',0), ('ERlcDataSendRespCause_InvalidParameter',1), ('ERlcDataSendRespCause_OutOfMemory',2), ('ERlcDataSendRespCause_MaxRlcRetransExceeded',3), ('ERlcDataSendRespCause_DiscardTimerExpired',4), ('ERlcDataSendRespCause_DiscardDcmUeBasedThresh',5), ('ERlcDataSendRespCause_DiscardDcmCellBasedThresh',6)]
class EPduMuxReqType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EPduMuxReqType_PduMuxData',0), ('EPduMuxReqType_CcchData',1), ('EPduMuxReqType_CcchDataReTransmit',2)]
class EActivationFlag(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EActivationFlag_Activate',0), ('EActivationFlag_Deactivate',1)]
class ECAProcedureResults(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ECAProcedureResults_sCellConfigurationComplete',0), ('ECAProcedureResults_sCellConfigurationCancel',1)]
class EHstConfig(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EHstConfig_NotApplied',0), ('EHstConfig_Hst',1), ('EHstConfig_HstPucch',2)]
class ERlsCause(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERlsCause_OutSync',0), ('ERlsCause_InSync',1), ('ERlsCause_TatExpiry',2), ('ERlsCause_RLF',3), ('ERlsCause_RA_SR',4), ('ERlsCause_AckNackRlf_ON',5), ('ERlsCause_AckNackRlf_OFF',6), ('ERlsCause_RA_Completed',7), ('ERlsCause_OutSyncFinal',8), ('ERlsCause_CqiRlf_ON',9), ('ERlsCause_CqiRlf_OFF',10), ('ERlsCause_PuschRlf_ON',11), ('ERlsCause_PuschRlf_OFF',12), ('ERlsCause_Bundling_ON',13), ('ERlsCause_Bundling_OFF',14), ('ERlsCause_SrsRlf_ON',15), ('ERlsCause_SrsRlf_OFF',16), ('ERlsCause_Tat2withLcg0Bsr',17), ('ERlsCause_SrsUpgrade',18), ('ERlsCause_SrsDowngrade',19), ('ERlsCause_TmSwitchToTm3',20), ('ERlsCause_TmSwitchToTm7',21), ('ERlsCause_TmSwitchToTm8',22)]
class EFrcValue(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EFrcValue_A1_3',0)]
class EDrxCommEnable(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EDrxCommEnable_On',0), ('EDrxCommEnable_Off',1)]
class ERandomAccessEvent(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERandomAccessEvent_InitialAccess',0), ('ERandomAccessEvent_Other',1)]
class ETestabilityServiceType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETestabilityServiceType_UlTtiTrace',0), ('ETestabilityServiceType_DlTtiTrace',1)]
class EGapPattern(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EGapPattern_measGap1',0), ('EGapPattern_measGap2',1)]

class SAmbrParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ambrUl',TAmbr), ('ambrDl',TAmbr)]
class SBitRateParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('minBitrateUl',TOaMMinBitrateUl), ('minBitrateDl',TOaMMinBitrateDl), ('maxBitrateUl',TOaMMaxBitrateUl), ('maxBitrateDl',TOaMMaxBitrateDl)]
class SUserInfoMac(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dedicRaPreParams',UDedicRaPreParams)]
class SSysInfoSchedule(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('siType',ESysInfoTypeId), ('siPeriodicity',TSiPeriodicity), ('siRepetition',TSiRepetition)]
class SRlcAmParameters(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('amRlcPollPdu',EPollPDU), ('amPollBytes',EPollByte), ('amRlcTimerPollReTransmit',TTimerPollReTransmit), ('amRlcTimerReordering',TTimerReordering), ('amRlcTimerStatusProhibit',TTimerStatusProhibit), ('maxRlcReTrans',TMaxRlcReTrans)]
class SSrbInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('srbId',TSrbId), ('logicalChannelId',TLogicalChannelId), ('logicalChannelGrId',TLogicalChannelGrId), ('logicalChannelIndex',TLcp), ('rlcMode',ERlcMode), ('rlcAmParameters',SRlcAmParameters), ('container',UWmpDcmSrbContainer)]
class SRlcUmParameters(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('umRlcSnFieldLengthDownlink',TSnFieldLength), ('umRlcSnFieldLengthUplink',TSnFieldLength), ('umTimerReordering',TTimerReordering)]
class SRbInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('drbId',TDrbId), ('drbType',EDrbType), ('logicalChannelId',TLogicalChannelId), ('logicalChannelGrId',TLogicalChannelGrId), ('logicalChannelIndex',TLcp), ('rlcMode',ERlcMode), ('rlcUmParameters',SRlcUmParameters), ('rlcAmParameters',SRlcAmParameters), ('container',UWmpDcmRbContainer)]
class SRaMsg3ThrLowParameters(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('raMsg3ThrLow',TRaMsg3ThrLow), ('raMsg3ThrLowCnt',TRaMsg3ThrLowCnt), ('flagCcchPriority',TFlagCcchPriority)]
class SRaMsg3ThrCntParameters(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('discardingCellGroupId',TCntId), ('raMsg3ThrCnt',TRaMsg3ThrCnt)]
class SRachParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('prachFreqOff',TPrachFreqOff), ('prachConfIndex',TOaMPrachConfIndex), ('raNondedPreamb',TRaNondedPreamb), ('raPreambGrASize',ERaPreambGrASize), ('raRespWinSize',ERaRespWinSize), ('crntiParams',UCrntiParams), ('raContResoT',ERaContResoT), ('prachCS',TOaMPrachCS), ('timerRaComp',TTimerRaComp), ('raMsg3Thr',TRaMsg3Thr), ('raMsg3ThrLowParameters',SRaMsg3ThrLowParameters), ('raMsg3ThrCntParameters',SRaMsg3ThrCntParameters), ('prachHsFlag',TBoolean)]
class STupUserAddress(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dlTupUserAddress',TAaSysComSicad)]
class SSiList(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('siType',ESysInfoTypeId), ('size',TL3MsgSize), ('data',prophy.array(u8,bound='size'))]
class SDRbList(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('drbId',TDrbId), ('messageResult',SMessageResult)]
class SPduTimeStamp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber)]
class SPagingItem(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('size',TL3MsgSize), ('data',prophy.array(u8,bound='size'))]
class SFrameConfTdd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tddFrameConf',TOaMTddFrameConf), ('tddSpecSubfConf',TOaMTddSpecSubfConf)]
class SCommonCellParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lCelId',TLocalCellResId), ('dlChBw',ECarrierBandwidth), ('ulChBw',ECarrierBandwidth), ('pMax',TMaxTxPower), ('dlPhyDataAddress',TAaSysComSicad), ('ulPhyDataAddress',TAaSysComSicad), ('maxNrSymPdcch',TOaMMaxNrSymPdcch), ('taTimer',ETimeAlignTimer), ('taMaxOffset',TTaMaxOffset), ('dlMimoMode',EDlMimoMode), ('cycPrefixDl',TCycPrefix), ('cycPreFixUl',TCycPrefix), ('frameConfTdd',SFrameConfTdd)]
class SPhichParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('phichRes',EOaMPhichRes), ('phichDur',EOaMPhichDur)]
class SCrntiParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('raContResoT',ERaContResoT), ('raCrntiReuseT',TOaMRaCrntiReuseT)]
class SDcmDedicRaParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dedicRaPreExpT',TDedicRaPreExpT), ('dedicRaPreIHoT',TDedicRaPreExpT)]
class SCqiParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cqiAperMode',ECqiAperMode), ('cqiPerEnable',ECqiPerEnable), ('numOfCqiPmi',prophy.u32), ('iCqiPmi',prophy.bytes(size=MAX_NUM_OF_RI_PMI_INFORMATION)), ('resourceIndexCqi',TResourceIndexCqi), ('cqiPerMode',ECqiPerMode), ('riEnable',TBoolean), ('numOfRi',prophy.u32), ('iRi',prophy.bytes(size=MAX_NUM_OF_RI_PMI_INFORMATION)), ('cqiPerSimulAck',ECqiPerSimulAck), ('cqiPerSbCycK',TCqiPerSbCycK), ('cqiPerSbPeriodFactor',EOaMCqiPerSbPeriodFactor)]
class SDrxParameters(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('drxCommEnable',EDrxCommEnable), ('drxLongEnable',TBoolean), ('drxStartOffset',TDrxStartOffset), ('drxOnDuratT',TDrxOnDuratT), ('drxInactivityT',TDrxInactivityT), ('drxRetransT',TDrxRetransT), ('drxLongCycle',TDrxLongCycle), ('drxShortEnable',TBoolean), ('drxShortCycle',TDrxShortCycle), ('drxShortCycleTimer',TDrxShortCycleTimer), ('smartStInactFactor',TSmartStInactFactor), ('drxProfileIndex',prophy.u32), ('drxConfigType',EDrxConfigType), ('drxConfigId',TConfigurationId)]
class SSoundingRsUlConfigDedicated(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('enableSRS',TBoolean), ('srsBandwidth',TSrsBandwidth), ('srsHoppingBw',TSrsHoppingBw), ('freqDomPos',TFrequencyDomainPosition), ('srsDuration',TBoolean), ('srsConfIndex',TSrsConfIndex), ('transComb',TTransmissionComb), ('cyclicShift',TCyclicShift)]
class SSoundingRsUlConfigCommon(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('enableSRS',TBoolean), ('srsBwConf',TSrsBandwidthConfiguration), ('srsSubfrConf',TSrsSubframeConfiguration), ('anSrsSimulTx',TBoolean), ('srsMaxUpPts',TOaMSrsMaxUpPts)]
class SUeHoParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueCategory',TUeCategory), ('ueCategoryR10',TUeCategory), ('ambrParams',SAmbrParams), ('bitRateParams',SBitRateParams), ('drxParameters',SDrxParameters)]
class SUeParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('transmMode',ETransmMode), ('accessStratumRelease',EUeRelease), ('ueHoParams',SUeHoParams)]
class SSRbList(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('srbId',TSrbId), ('messageResult',SMessageResult)]
class SUeSetupParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('srEnable',TBoolean), ('pucchResourceIndex',TPucchResourceIndex), ('srPeriod',ESrPeriod), ('srOffset',TSrOffset)]
class SDuration(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('bcchModPeriodLength',TBcchModPeriodLength), ('bcchModPeriodNumber',TBcchModPeriodNumber)]
class SSpsCrntiReleaseInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('status',EStatusLte), ('specificCause',ESpecificCauseLte)]
class SSiSegmentSize(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('siSegmentSize',TL3MsgSize)]
class SMacCoefficientValues(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('caBw',ECarrierBandwidth), ('cDlMac1',TCoEffValue), ('cDlMac2',TCoEffValue), ('cDlMac3',TCoEffValue), ('cUlMac1',TCoEffValue), ('cUlMac2',TCoEffValue), ('cUlMac3',TCoEffValue), ('cDlMacPs1',TCoEffValue), ('cDlMacPs2',TCoEffValue), ('cDlMacPs3',TCoEffValue), ('cDlMacPs4',TCoEffValue), ('cUlMacPs1',TCoEffValue), ('cUlMacPs2',TCoEffValue), ('culMacPs3',TCoEffValue), ('cUlMacPs4',TCoEffValue)]
class SRlcLcpInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('umReorderingBufferSize',TBufferSize), ('umTransmitBufferSize',TBufferSize), ('bufferingTimeTh',TThresholdRlcT), ('rlcDiscardTh',TThresholdRlc)]
class STpcPdcchConfigParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tpcPucchRnti',TTpcRnti), ('tpcPucchIndexOfFormat3',TTpcIndex), ('tpcPuschRnti',TTpcRnti), ('tpcPuschIndexOfFormat3',TTpcIndex)]
class SRbStopSchedulingInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('drbId',TDrbId), ('dataForwardingType',EDataForwarding)]
class SUeRbPacketId(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueId',TUeId), ('radioBearerId',TRadioBearerId), ('packetId',TPacketId)]
class SRingBufferDlParam(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('destinationSrioId',TAaSysComNid), ('addressLastReadMarkerPtr',prophy.u32), ('startAddressBlocks',prophy.u32), ('lengthBlocks',prophy.u32)]
class SRingBufferUlParam(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('destinationSrioId',TAaSysComNid), ('addressLastReadMarkerPtr',prophy.u32), ('startAddressBlocks',prophy.u32), ('lengthBlocks',prophy.u32)]
class SRingBufferSendReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueId',prophy.u16), ('radioBearerId',prophy.u8), ('validDrxConfigId',prophy.u8), ('drxConfigId',TConfigurationId), ('packetId',prophy.u16), ('frameNumber',prophy.u16), ('harqRespFlag',prophy.u8), ('subFrameNumber',prophy.u8), ('size',prophy.u16), ('dataPtr',prophy.u32)]
class SRingBufferDlCtrl(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numberOfSendReq',u32), ('sendReq',prophy.array(SRingBufferSendReq,bound='numberOfSendReq')), ('padding',prophy.u32), ('nextMarkerPtr',prophy.u32), ('marker',prophy.u32)]
class SRingBufferDlPayload(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('d',prophy.bytes(size=SIZE_RINGBUF_PAYLOAD_DL))]
class SRingBufferDlBlock(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('data',SRingBufferDlPayload), ('ctrl',SRingBufferDlCtrl)]
class SRingBufferUlItem(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueId',prophy.u16), ('radioBearerId',prophy.u8), ('subFrameNumber',prophy.u8), ('frameNumber',prophy.u16), ('lastUlSdu',prophy.u8), ('unused1',prophy.u8), ('unused2',prophy.u16), ('size',prophy.u16), ('dataPtr',prophy.u32)]
class SRingBufferUlCtrl(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numberOfItem',u32), ('item',prophy.array(SRingBufferUlItem,bound='numberOfItem')), ('totalPayloadLen',prophy.u32), ('nextMarkerPtr',prophy.u32), ('marker',prophy.u32)]
class SRingBufferUlPayload(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('d',prophy.bytes(size=SIZE_RINGBUF_PAYLOAD_UL))]
class SRingBufferUlBlock(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('data',SRingBufferUlPayload), ('ctrl',SRingBufferUlCtrl)]
class SMeasurementA7or8(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('enableTwoUserMeasurement',TBoolean), ('stationaryUeResources',TBoolean)]
class SUlTestModelConfig(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('noOfHarqTransmissions',ENoOfHarqTransmissions), ('hstConfig',EHstConfig), ('resourceIndexCqi',TResourceIndexCqi), ('iCqiPmi',TICqiPmi)]
class SMeasurementDcm5toDcm8(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('mcsIndex',prophy.u32)]
class SBearerList(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('drbId',TDrbId), ('packetId',TPacketId)]
class SRbUePacketId(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('rlcDataSendRespCause',ERlcDataSendRespCause), ('ueId',TUeId), ('radioBearerId',TRadioBearerId), ('packetIdLow',TPacketId), ('packetIdHigh',TPacketId)]
class SBufferDiscardParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('thOverflowDiscard',TThOverflowDiscard), ('flagOverflowDiscard',TFlagOverflowDiscard), ('discBuffThrAct',TBoolean), ('discBuffHighThr',TDiscBuffThr)]
class SMsg3Info(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrnti), ('ueGroup',TUeGroup), ('size',TL3MsgSize), ('data',prophy.array(u8,bound='size'))]
class SNodeAddress(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ulCellMac',TAaSysComNid), ('ulUeMac',TAaSysComNid), ('ulSchedulerMac',TAaSysComNid), ('dlCellMac',TAaSysComNid), ('dlUeMac',TAaSysComNid), ('dlSchedulerMac',TAaSysComNid), ('cellManager',TAaSysComNid)]
class SUeList(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueId',TUeId), ('drbIdList',prophy.bytes(size=4)), ('bearerReleaseIndCause',ESpecificCauseLte)]
class SRbModifyQciInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('schedulWeight',TSchedulingWeight), ('qci',prophy.u32)]
class SRbModifyInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('drbId',TDrbId), ('congestionWeight',prophy.u32), ('qciInfo',SRbModifyQciInfo)]
class SUePhr(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueIndex',TUeIndex), ('paddingUeIndex',prophy.u16), ('crnti',prophy.u16), ('powerLevel',prophy.u16)]
class SAmountOctets(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('rbId',TRadioBearerId), ('isDataOctetsLeft',prophy.u8), ('isCtrlOctetsLeft',prophy.u8)]
class SDlTbAttributes(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('maxNumOfHarqTx',TNumHarqTransmissions), ('ndiForPdcch',TNewDataIndicator)]
class SCaCqiParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cqiParams',SCqiParams), ('cqiParamsWmp',SCqiParamsWmp)]
class SVoLteThresholdParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ulTalkSpurtUpperDataTh',TDataSize), ('ulTalkSpurtLowerDataTh',TDataSize)]
class SR10n1PucchAnCsElement(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('pucchResourceIndex',prophy.bytes(size=4))]
class SDrxShortParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('drxShortEnable',TBoolean), ('drxShortCycle',TDrxShortCycle), ('drxShortCycleTimer',TDrxShortCycleTimer), ('smartStInactFactor',TSmartStInactFactor)]
class SUeInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrntiU16), ('ueIndex',TUeIndex)]
class SCaCeInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('caCeAvail',TBooleanU8), ('caCeValue',TCaCeValue), ('unused',prophy.u16)]
class SDlSchPduMuxAmountOctets(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('logicalChannelId',prophy.u16), ('ctrl',prophy.u16), ('data',prophy.u16)]
class SDlSchPduMuxCwAttributes(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tbSize',TTbSize), ('drxCommEnable',TBooleanU8), ('ueTaCeAvail',TBooleanU8), ('ueTaCeValue',prophy.u16), ('ueCaCeInfo',SCaCeInfo), ('tfi',TMcs), ('modulation',TEModulationU8), ('newDataIndicator',TNewDataIndicatorU8), ('redundancyVersion',TRedundancyVersionU8), ('codeWordIndex',TCodeWordIndexU8), ('harqIdCw',THarqProcessNumberU8), ('trnumCw',prophy.u8), ('amountRbs',prophy.u8), ('amountRbOctets',prophy.bytes(size=MAX_NUM_RB_PER_USER))]
class SHarqReleaseInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('servingCellIndex',prophy.u8), ('ueIndex',TUeIndex), ('crnti',prophy.u16), ('harqId1',prophy.u8), ('harqId2',prophy.u8), ('validHarqId1',prophy.u8), ('validHarqId2',prophy.u8), ('ackReceivedHarqId1',prophy.u8), ('ackReceivedHarqId2',prophy.u8), ('lnCellIdServCell',TOaMLnCelId)]
class SMgmtMeasurement(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('val',prophy.u32), ('offsetInGroup',prophy.u16), ('groupId',prophy.u8), ('status',prophy.u8)]
class SPduMuxDataResultEntry(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrntiU16), ('ueIndex',TUeIndex), ('cw0',EPduMuxDataResultCause), ('cw1',EPduMuxDataResultCause)]
class SMacMessageHeader(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('srioDioBufferAddr',prophy.u32), ('srioDioBufferSize',prophy.u32)]
class SLcgIds(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueBufferStatusReport',TBufferSize), ('receivedDataSize',TBufferSize)]
class SBearerIds(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('drbId',TRadioBearerIdU8), ('lcgId',TLogicalChannelGrIdU8), ('rcvdData',prophy.u16)]
class SUeBufferStatus(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueIndex',TUeIndex), ('crnti',TCrntiU16), ('usefulDataReceived',TBooleanU8), ('numBearerIdList',prophy.u8), ('dtchMacSduReceived',TBooleanU8), ('harqProcessNumber',THarqProcessNumberU8), ('lcgIdList',prophy.bytes(size=MAX_NUM_LCG_IDS)), ('bearerIdList',prophy.bytes(size=MAX_NUM_GBR_BEARER_PER_UE))]
class SUlBufStatusIndPayload(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numberOfUes',TNumberOfItems), ('ueIdInfo',prophy.array(SUeBufferStatus,bound='numberOfUes'))]
class SContentionResInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',prophy.u16), ('crnti',prophy.u16), ('ueIndex',TUeIndex), ('raEvent',prophy.u8), ('ueContentionResolutionId',prophy.u64)]
class SDlBufferStatusInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('amountDataOctets',prophy.u32), ('amountOfRlcSduData',prophy.u32), ('amountCtrlOctets',prophy.u16), ('ueIndex',TUeIndex), ('rbId',TRadioBearerIdU8), ('lcId',TLogicalChannelIdU8), ('xsfnTimeStamp',prophy.u16)]
class SLcgIdsWmp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueBufferStatusReport',TBufferSize), ('receivedDataSize',TBufferSize)]
class SUeBufferStatusWmp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrnti), ('ueIndex',TUeIndex), ('usefulDataReceived',TBooleanU8), ('lcgIdList',prophy.bytes(size=MAX_NUM_LCG_IDS))]
class SPduMuxDataReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueIndex',TUeIndex), ('macId',TCrntiU16), ('txPower',TTxPower), ('spatialMode',TSpatialMode), ('numOfLayers',TNumOfLayersU8), ('codebookIndex',TCodebookIndexU8), ('nIr',TNIr), ('resources',SPdschResources), ('mimoIndicator',TBooleanU8), ('servingCellIndex',TServingCellIndex), ('lnCellIdServCell',TOaMLnCelId), ('reqType',TEPduMuxReqTypeU8), ('hasDlBfTbFormat',TBooleanU8), ('dlBfTbFormat',SDlBfTbFormat), ('tbFlags',prophy.u32), ('cwAttributes',prophy.bytes(size=MAX_NMBR_CODEWORDS))]
class SDataReceived(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrntiU16), ('ueIndex',TUeIndex)]
class SPrachUsageRatio(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('nbrOfGroupARAPreambleReceived',TMeasurementValue), ('nbrOfGroupBRAPreambleReceived',TMeasurementValue), ('nbrOfRAPreambleReceivedDedicPreamble',TMeasurementValue), ('nbrOfRARespTransmitForGroupAPreamble',TMeasurementValue), ('nbrOfRARespTransmitForGroupBPreamble',TMeasurementValue), ('nbrOfRARespTransmitForDedicPreamble',TMeasurementValue), ('nbrOfAssignNGDedicPreambleSyncReq',TMeasurementValue), ('nbrOfOpportDedicPreambleReception',TMeasurementValue), ('nbrOfDedicPreambleAllocated',TMeasurementValue), ('nbrOfOpportGroupARAPreambleRecept',TMeasurementValue), ('nbrOfOpportGroupBRAPreambleRecept',TMeasurementValue)]
class STransmittedAndReceivedPower(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('phichTransmitPower',TMeasurementValue), ('transmitPowerOfControlPart',TMeasurementValue), ('totalTransmitPowerBranch1',TMeasurementValue), ('totalTransmitPowerBranch2',TMeasurementValue), ('receivedTotalPowerBranch1',TMeasurementValue), ('receivedTotalPowerBranch2',TMeasurementValue)]
class SMacPduTransmissionRate(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dlMacPduTransmissionRate1',TMeasurementValue), ('dlMacPduTransmissionRate2',TMeasurementValue), ('dlMacPduTransmissionRate3',TMeasurementValue), ('dlMacPduTransmissionRate4',TMeasurementValue), ('dlMacPduTransmissionRate5',TMeasurementValue), ('dlMacPduTransmissionRate6',TMeasurementValue), ('dlMacPduTransmissionRate7',TMeasurementValue), ('dlMacPduTransmissionRate8',TMeasurementValue), ('dlMacPduTransmissionRate9',TMeasurementValue), ('dlMacPduTransmissionRate10',TMeasurementValue), ('dlMacPduTransmissionRate11',TMeasurementValue), ('dlMacPduTransmissionRate12',TMeasurementValue), ('dlMacPduTransmissionRate13',TMeasurementValue), ('dlMacPduTransmissionRate14',TMeasurementValue), ('dlMacPduTransmissionRate15',TMeasurementValue), ('dlMacPduTransmissionRate16',TMeasurementValue), ('dlMacPduTransmissionRate17',TMeasurementValue), ('dlMacPduTransmissionRate18',TMeasurementValue), ('dlMacPduTransmissionRate19',TMeasurementValue), ('dlMacPduTransmissionRate20',TMeasurementValue), ('dlMacPduTransmissionRate21',TMeasurementValue), ('dlMacPduTransmissionRate22',TMeasurementValue), ('dlMacPduTransmissionRate23',TMeasurementValue), ('dlMacPduTransmissionRate24',TMeasurementValue), ('dlMacPduTransmissionRate25',TMeasurementValue), ('dlMacPduTransmissionRate26',TMeasurementValue), ('dlMacPduTransmissionRate27',TMeasurementValue), ('dlMacPduTransmissionRate28',TMeasurementValue), ('dlMacPduTransmissionRate29',TMeasurementValue), ('dlMacPduTransmissionRate30',TMeasurementValue), ('dlMacPduTransmissionRate31',TMeasurementValue), ('dlMacPduTransmissionRate32',TMeasurementValue), ('ulMacPduTransmissionRate0',TMeasurementValue), ('ulMacPduTransmissionRate1',TMeasurementValue), ('ulMacPduTransmissionRate2',TMeasurementValue), ('ulMacPduTransmissionRate3',TMeasurementValue), ('ulMacPduTransmissionRateCrcOked0',TMeasurementValue), ('ulMacPduTransmissionRateCrcOked1',TMeasurementValue), ('ulMacPduTransmissionRateCrcOked2',TMeasurementValue), ('ulMacPduTransmissionRateCrcOked3',TMeasurementValue)]
class SNbrOfDrxUe(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('nbrOfNonDrxUe',TMeasurementValue), ('nbrOfLongDrxUe',TMeasurementValue)]
class SRlcPdcpTraffic(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('transmittedDataRateIni',TMeasurementValue), ('transmittedDataRateReTrans',TMeasurementValue), ('receivedDataRate',TMeasurementValue), ('nbrOfReset',TMeasurementValue), ('amountOfDataBufferedRlcPdcp',TMeasurementValue)]
class SPersistentRbUsage(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dlResource0',TMeasurementValue), ('dlResource1',TMeasurementValue), ('dlResource2',TMeasurementValue), ('dlResource3',TMeasurementValue), ('dlResource4',TMeasurementValue), ('dlResource5',TMeasurementValue), ('dlResource6',TMeasurementValue), ('dlResource7',TMeasurementValue), ('dlResource8',TMeasurementValue), ('dlResource9',TMeasurementValue), ('dlResource10',TMeasurementValue), ('dlResource11',TMeasurementValue), ('dlResource12',TMeasurementValue), ('dlResource13',TMeasurementValue), ('dlResource14',TMeasurementValue), ('dlResource15',TMeasurementValue), ('dlResource16',TMeasurementValue), ('dlResource17',TMeasurementValue), ('dlResource18',TMeasurementValue), ('dlResource19',TMeasurementValue), ('ulResource0',TMeasurementValue), ('ulResource1',TMeasurementValue), ('ulResource2',TMeasurementValue), ('ulResource3',TMeasurementValue), ('ulResource4',TMeasurementValue), ('ulResource5',TMeasurementValue), ('ulResource6',TMeasurementValue), ('ulResource7',TMeasurementValue), ('ulResource8',TMeasurementValue), ('ulResource9',TMeasurementValue), ('ulResource10',TMeasurementValue), ('ulResource11',TMeasurementValue), ('ulResource12',TMeasurementValue), ('ulResource13',TMeasurementValue), ('ulResource14',TMeasurementValue), ('ulResource15',TMeasurementValue), ('ulResource16',TMeasurementValue), ('ulResource17',TMeasurementValue), ('ulResource18',TMeasurementValue), ('ulResource19',TMeasurementValue)]
class SChannelUsageStatus(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('nbrOfPdcchOfdmSymbol1',TMeasurementValue), ('nbrOfPdcchOfdmSymbol2',TMeasurementValue), ('nbrOfPdcchOfdmSymbol3',TMeasurementValue), ('nbrOfProcessingResourceShortageSituation',TMeasurementValue), ('nbrOfUnTransmitUesDueLackOfPdcchResource',TMeasurementValue), ('pdfOfWidebankCQI',prophy.bytes(size=256)), ('pdfOfDlAverageDataRate',prophy.bytes(size=240)), ('pdfOfUlAverageDataRate',prophy.bytes(size=60)), ('pdfOfUeInactiveTimer',prophy.bytes(size=11))]
class SInterferenceLevel(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('interferenceLevelPucch',TMeasurementValue), ('interferenceLevelPusch',TMeasurementValue), ('interferenceLevelPrach',TMeasurementValue)]
class SPathloss(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('nbrOfUes',prophy.bytes(size=124))]
class SNbrLogChMeasType1(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('nbrOfLogChHavingDataInBufferDl1',TMeasurementValue), ('nbrOfLogChHavingDataInBufferDl2',TMeasurementValue), ('nbrOfLogChHavingDataInBufferDl3',TMeasurementValue), ('nbrOfLogChHavingDataInBufferDl4',TMeasurementValue), ('nbrOfLogChHavingDataInBufferDl5',TMeasurementValue), ('nbrOfLogChHavingDataInBufferDl6',TMeasurementValue), ('nbrOfLogChHavingDataInBufferDl7',TMeasurementValue), ('nbrOfLogChHavingDataInBufferDl8',TMeasurementValue), ('nbrOfLogChHavingDataInBufferDl9',TMeasurementValue), ('nbrOfLogChHavingDataInBufferDl10',TMeasurementValue), ('nbrOfLogChHavingDataInBufferDl11',TMeasurementValue), ('nbrOfLogChHavingDataInBufferDl12',TMeasurementValue), ('nbrOfLogChHavingDataInBufferDl13',TMeasurementValue), ('nbrOfLogChHavingDataInBufferDl14',TMeasurementValue), ('nbrOfLogChHavingDataInBufferDl15',TMeasurementValue), ('nbrOfLogChHavingDataInBufferDl16',TMeasurementValue), ('nbrOfLogChHavingDataInBufferUl0',TMeasurementValue), ('nbrOfLogChHavingDataInBufferUl1',TMeasurementValue), ('nbrOfLogChHavingDataInBufferUl2',TMeasurementValue), ('nbrOfLogChHavingDataInBufferUl3',TMeasurementValue), ('nbrOfLogChAverageDataRateBelowThreshDl1',TMeasurementValue), ('nbrOfLogChAverageDataRateBelowThreshDl2',TMeasurementValue), ('nbrOfLogChAverageDataRateBelowThreshDl3',TMeasurementValue), ('nbrOfLogChAverageDataRateBelowThreshDl4',TMeasurementValue), ('nbrOfLogChAverageDataRateBelowThreshDl5',TMeasurementValue), ('nbrOfLogChAverageDataRateBelowThreshDl6',TMeasurementValue), ('nbrOfLogChAverageDataRateBelowThreshDl7',TMeasurementValue), ('nbrOfLogChAverageDataRateBelowThreshDl8',TMeasurementValue), ('nbrOfLogChAverageDataRateBelowThreshDl9',TMeasurementValue), ('nbrOfLogChAverageDataRateBelowThreshDl10',TMeasurementValue), ('nbrOfLogChAverageDataRateBelowThreshDl11',TMeasurementValue), ('nbrOfLogChAverageDataRateBelowThreshDl12',TMeasurementValue), ('nbrOfLogChAverageDataRateBelowThreshDl13',TMeasurementValue), ('nbrOfLogChAverageDataRateBelowThreshDl14',TMeasurementValue), ('nbrOfLogChAverageDataRateBelowThreshDl15',TMeasurementValue), ('nbrOfLogChAverageDataRateBelowThreshDl16',TMeasurementValue), ('nbrOfLogChAverageDataRateBelowThreshUl0',TMeasurementValue), ('nbrOfLogChAverageDataRateBelowThreshUl1',TMeasurementValue), ('nbrOfLogChAverageDataRateBelowThreshUl2',TMeasurementValue), ('nbrOfLogChAverageDataRateBelowThreshUl3',TMeasurementValue)]
class SNbrLogChMeasType2(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('nbrOfLogChBufferingTimeAboveTreshDl1',TMeasurementValue), ('nbrOfLogChBufferingTimeAboveTreshDl2',TMeasurementValue), ('nbrOfLogChBufferingTimeAboveTreshDl3',TMeasurementValue), ('nbrOfLogChBufferingTimeAboveTreshDl4',TMeasurementValue), ('nbrOfLogChBufferingTimeAboveTreshDl5',TMeasurementValue), ('nbrOfLogChBufferingTimeAboveTreshDl6',TMeasurementValue), ('nbrOfLogChBufferingTimeAboveTreshDl7',TMeasurementValue), ('nbrOfLogChBufferingTimeAboveTreshDl8',TMeasurementValue), ('nbrOfLogChBufferingTimeAboveTreshDl9',TMeasurementValue), ('nbrOfLogChBufferingTimeAboveTreshDl10',TMeasurementValue), ('nbrOfLogChBufferingTimeAboveTreshDl11',TMeasurementValue), ('nbrOfLogChBufferingTimeAboveTreshDl12',TMeasurementValue), ('nbrOfLogChBufferingTimeAboveTreshDl13',TMeasurementValue), ('nbrOfLogChBufferingTimeAboveTreshDl14',TMeasurementValue), ('nbrOfLogChBufferingTimeAboveTreshDl15',TMeasurementValue), ('nbrOfLogChBufferingTimeAboveTreshDl16',TMeasurementValue)]
class SNbrLogChMeasType3(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('nbrOfLogChDataDiscardDueDelayDl1',TMeasurementValue), ('nbrOfLogChDataDiscardDueDelayDl2',TMeasurementValue), ('nbrOfLogChDataDiscardDueDelayDl3',TMeasurementValue), ('nbrOfLogChDataDiscardDueDelayDl4',TMeasurementValue), ('nbrOfLogChDataDiscardDueDelayDl5',TMeasurementValue), ('nbrOfLogChDataDiscardDueDelayDl6',TMeasurementValue), ('nbrOfLogChDataDiscardDueDelayDl7',TMeasurementValue), ('nbrOfLogChDataDiscardDueDelayDl8',TMeasurementValue), ('nbrOfLogChDataDiscardDueDelayDl9',TMeasurementValue), ('nbrOfLogChDataDiscardDueDelayDl10',TMeasurementValue), ('nbrOfLogChDataDiscardDueDelayDl11',TMeasurementValue), ('nbrOfLogChDataDiscardDueDelayDl12',TMeasurementValue), ('nbrOfLogChDataDiscardDueDelayDl13',TMeasurementValue), ('nbrOfLogChDataDiscardDueDelayDl14',TMeasurementValue), ('nbrOfLogChDataDiscardDueDelayDl15',TMeasurementValue), ('nbrOfLogChDataDiscardDueDelayDl16',TMeasurementValue)]
class SBbResourceRoom(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('nbrOfDlSpsUe',TMeasurementValue), ('nbrOfUlSpsUe',TMeasurementValue), ('unsuccessDlSpsAssignsNdiscDlAck',TMeasurementValue), ('unsuccessDlSpsAssignsNdiscDl',TMeasurementValue), ('unsuccessDlSpsAssignsNdiscUl',TMeasurementValue)]
class SPhichTransmitPower(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('phichTransmitPowerForPersistentSched',TMeasurementValue)]
class SRaPreambleStatistics(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('pdfOfRaPreamblesReceived',prophy.bytes(size=32))]
class SResourceBlockUsageRatio(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dlRbUsageRatio',TMeasurementValue), ('ulRbUsageRatio',TMeasurementValue), ('dlRbUsageRatioDbch',TMeasurementValue), ('dlRbUsageRatioPch',TMeasurementValue), ('dlRbUsageRatioRar',TMeasurementValue), ('dlRbUsageRatioVoice',TMeasurementValue), ('ulRbUsageRatioVoice',TMeasurementValue)]
class SPdcchUsageRatio(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('nbrOfMultiplexedPdcchDl',TMeasurementValue), ('nbrOfMultiplexedPdcchUl',TMeasurementValue), ('nbrOfMultiplexedPdcchVoiceDl',TMeasurementValue), ('nbrOfMultiplexedPdcchVoiceUl',TMeasurementValue), ('totalNbrOfCces',TMeasurementValue), ('nbrOfCcesAssignedToPdcch',TMeasurementValue), ('nbrOfCcesAssignedToPdcchVoice',TMeasurementValue)]
class SMacSduTransmAndReceptRate(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('nbrOfSubFramesDlSdusTransmLchPrio1',TMeasurementValue), ('nbrOfSubFramesDlSdusTransmLchPrio2',TMeasurementValue), ('nbrOfSubFramesDlSdusTransmLchPrio3',TMeasurementValue), ('nbrOfSubFramesDlSdusTransmLchPrio4',TMeasurementValue), ('nbrOfSubFramesDlSdusTransmLchPrio5',TMeasurementValue), ('nbrOfSubFramesDlSdusTransmLchPrio6',TMeasurementValue), ('nbrOfSubFramesDlSdusTransmLchPrio7',TMeasurementValue), ('nbrOfSubFramesDlSdusTransmLchPrio8',TMeasurementValue), ('nbrOfSubFramesDlSdusTransmLchPrio9',TMeasurementValue), ('nbrOfSubFramesDlSdusTransmLchPrio10',TMeasurementValue), ('nbrOfSubFramesDlSdusTransmLchPrio11',TMeasurementValue), ('nbrOfSubFramesDlSdusTransmLchPrio12',TMeasurementValue), ('nbrOfSubFramesDlSdusTransmLchPrio13',TMeasurementValue), ('nbrOfSubFramesDlSdusTransmLchPrio14',TMeasurementValue), ('nbrOfSubFramesDlSdusTransmLchPrio15',TMeasurementValue), ('nbrOfSubFramesDlSdusTransmLchPrio16',TMeasurementValue), ('amountOfTransmDataDlSdusLchPrio1',TMeasurementValue), ('amountOfTransmDataDlSdusLchPrio2',TMeasurementValue), ('amountOfTransmDataDlSdusLchPrio3',TMeasurementValue), ('amountOfTransmDataDlSdusLchPrio4',TMeasurementValue), ('amountOfTransmDataDlSdusLchPrio5',TMeasurementValue), ('amountOfTransmDataDlSdusLchPrio6',TMeasurementValue), ('amountOfTransmDataDlSdusLchPrio7',TMeasurementValue), ('amountOfTransmDataDlSdusLchPrio8',TMeasurementValue), ('amountOfTransmDataDlSdusLchPrio9',TMeasurementValue), ('amountOfTransmDataDlSdusLchPrio10',TMeasurementValue), ('amountOfTransmDataDlSdusLchPrio11',TMeasurementValue), ('amountOfTransmDataDlSdusLchPrio12',TMeasurementValue), ('amountOfTransmDataDlSdusLchPrio13',TMeasurementValue), ('amountOfTransmDataDlSdusLchPrio14',TMeasurementValue), ('amountOfTransmDataDlSdusLchPrio15',TMeasurementValue), ('amountOfTransmDataDlSdusLchPrio16',TMeasurementValue), ('nbrOfSubFramesUlSdusTransmLchPrio0',TMeasurementValue), ('nbrOfSubFramesUlSdusTransmLchPrio1',TMeasurementValue), ('nbrOfSubFramesUlSdusTransmLchPrio2',TMeasurementValue), ('nbrOfSubFramesUlSdusTransmLchPrio3',TMeasurementValue), ('amountOfTransmDataUlSdusLchPrio0',TMeasurementValue), ('amountOfTransmDataUlSdusLchPrio1',TMeasurementValue), ('amountOfTransmDataUlSdusLchPrio2',TMeasurementValue), ('amountOfTransmDataUlSdusLchPrio3',TMeasurementValue)]
class SNumberOfVoiceUE(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('nbrOfVoiceUePerDelayPackedIndex0',TMeasurementValue), ('nbrOfVoiceUePerDelayPackedIndex1',TMeasurementValue), ('nbrOfVoiceUePerDelayPackedIndex2',TMeasurementValue), ('nbrOfVoiceUePerDelayPackedIndex3',TMeasurementValue), ('nbrOfVoiceUePerPeriodicGrantIndex0TtiBundlOn',TMeasurementValue), ('nbrOfVoiceUePerPeriodicGrantIndex1TtiBundlOn',TMeasurementValue), ('nbrOfVoiceUePerPeriodicGrantIndex2TtiBundlOn',TMeasurementValue), ('nbrOfVoiceUePerPeriodicGrantIndex3TtiBundlOn',TMeasurementValue), ('nbrOfVoiceUePerPeriodicGrantIndex0TtiBundlOff',TMeasurementValue), ('nbrOfVoiceUePerPeriodicGrantIndex1TtiBundlOff',TMeasurementValue), ('nbrOfVoiceUePerPeriodicGrantIndex2TtiBundlOff',TMeasurementValue), ('nbrOfVoiceUePerPeriodicGrantIndex3TtiBundlOff',TMeasurementValue), ('nbrOfDlPduPerDelayPackedIndex0',TMeasurementValue), ('nbrOfDlPduPerDelayPackedIndex1',TMeasurementValue), ('nbrOfDlPduPerDelayPackedIndex2',TMeasurementValue), ('nbrOfDlPduPerDelayPackedIndex3',TMeasurementValue), ('nbrOfDlHarqTxPerDelayPackedIndex0',TMeasurementValue), ('nbrOfDlHarqTxPerDelayPackedIndex1',TMeasurementValue), ('nbrOfDlHarqTxPerDelayPackedIndex2',TMeasurementValue), ('nbrOfDlHarqTxPerDelayPackedIndex3',TMeasurementValue), ('nbrOfUlPduPerPeriodicGrantIndex0TtiBundOn',TMeasurementValue), ('nbrOfUlPduPerPeriodicGrantIndex1TtiBundOn',TMeasurementValue), ('nbrOfUlPduPerPeriodicGrantIndex2TtiBundOn',TMeasurementValue), ('nbrOfUlPduPerPeriodicGrantIndex3TtiBundOn',TMeasurementValue), ('nbrOfUlHarqTxPerPeriodicGrantIndex0TtiBundOn',TMeasurementValue), ('nbrOfUlHarqTxPerPeriodicGrantIndex1TtiBundOn',TMeasurementValue), ('nbrOfUlHarqTxPerPeriodicGrantIndex2TtiBundOn',TMeasurementValue), ('nbrOfUlHarqTxPerPeriodicGrantIndex3TtiBundOn',TMeasurementValue), ('nbrOfUlPduPerPeriodicGrantIndex0TtiBundOff',TMeasurementValue), ('nbrOfUlPduPerPeriodicGrantIndex1TtiBundOff',TMeasurementValue), ('nbrOfUlPduPerPeriodicGrantIndex2TtiBundOff',TMeasurementValue), ('nbrOfUlPduPerPeriodicGrantIndex3TtiBundOff',TMeasurementValue), ('nbrOfUlHarqTxPerPeriodicGrantIndex0TtiBundlOff',TMeasurementValue), ('nbrOfUlHarqTxPerPeriodicGrantIndex1TtiBundlOff',TMeasurementValue), ('nbrOfUlHarqTxPerPeriodicGrantIndex2TtiBundlOff',TMeasurementValue), ('nbrOfUlHarqTxPerPeriodicGrantIndex3TtiBundlOff',TMeasurementValue), ('nbrOfAckPduPerDelayPackedIndex0',TMeasurementValue), ('nbrOfAckPduPerDelayPackedIndex1',TMeasurementValue), ('nbrOfAckPduPerDelayPackedIndex2',TMeasurementValue), ('nbrOfAckPduPerDelayPackedIndex3',TMeasurementValue), ('nbrOfExceedMaxTransmPerDelayPackedIndex0',TMeasurementValue), ('nbrOfExceedMaxTransmPerDelayPackedIndex1',TMeasurementValue), ('nbrOfExceedMaxTransmPerDelayPackedIndex2',TMeasurementValue), ('nbrOfExceedMaxTransmPerDelayPackedIndex3',TMeasurementValue), ('nbrOfAckPduPerPeriodicGrantIndex0TtiBundlOn',TMeasurementValue), ('nbrOfAckPduPerPeriodicGrantIndex1TtiBundlOn',TMeasurementValue), ('nbrOfAckPduPerPeriodicGrantIndex2TtiBundlOn',TMeasurementValue), ('nbrOfAckPduPerPeriodicGrantIndex3TtiBundlOn',TMeasurementValue), ('nbrOfExceedTransmPeriodicGrantIndex0TtiBundlOn',TMeasurementValue), ('nbrOfExceedTransmPeriodicGrantIndex1TtiBundlOn',TMeasurementValue), ('nbrOfExceedTransmPeriodicGrantIndex2TtiBundlOn',TMeasurementValue), ('nbrOfExceedTransmPeriodicGrantIndex3TtiBundlOn',TMeasurementValue), ('nbrOfAckPduPerPeriodicGrantIndex0TtiBundlOff',TMeasurementValue), ('nbrOfAckPduPerPeriodicGrantIndex1TtiBundlOff',TMeasurementValue), ('nbrOfAckPduPerPeriodicGrantIndex2TtiBundlOff',TMeasurementValue), ('nbrOfAckPduPerPeriodicGrantIndex3TtiBundlOff',TMeasurementValue), ('nbrOfExceedMaxTransmPeriodicGrantIndex0TtiBundlOff',TMeasurementValue), ('nbrOfExceedMaxTransmPeriodicGrantIndex1TtiBundlOff',TMeasurementValue), ('nbrOfExceedMaxTransmPeriodicGrantIndex2TtiBundlOff',TMeasurementValue), ('nbrOfExceedMaxTransmPeriodicGrantIndex3TtiBundlOff',TMeasurementValue)]
class SGbrLoadCellDl(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('nbrOfUsedPrbsForGbrTrafficDl',TMeasurementValue), ('averageNbrOfAvailablePrbsForGbrDl',TMeasurementValue), ('initTransmEfficiencyDl',TMeasurementValue), ('ratioOfPdcchUtilizUesWithGbrBearersDl',TMeasurementValue)]
class SGbrLoadCellUl(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('nbrOfUsedPrbsForGbrTrafficUl',TMeasurementValue), ('averageNbrOfAvailablePrbsForGbrUl',TMeasurementValue), ('initTransmEfficiencyUl',TMeasurementValue), ('ratioOfPdcchUtilizUesWithGbrBearersUl',TMeasurementValue)]
class SDrbData(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('drbId',TMeasurementValue), ('nbrOfAllocatedPrbs',TMeasurementValue)]
class SGbrLoadUe(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueId',TMeasurementValue), ('transmEfficiency',TMeasurementValue), ('nbrOfBearers',TMeasurementValue), ('drbData',prophy.bytes(size=4))]
class SGbrLoadUeDl(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('nbrOfUesInReport',TMeasurementValue), ('gbrLoadUeDl',prophy.array(SGbrLoadUe,bound='nbrOfUesInReport'))]
class SGbrLoadUeUl(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('nbrOfUesInReport',TMeasurementValue), ('gbrLoadUeUl',prophy.array(SGbrLoadUe,bound='nbrOfUesInReport'))]
class SNonGbrLoadCellDl(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('averAvailNbrOfPrbsNonGbrTraffDl',TMeasurementValue), ('averSumOfWeightsBearersWithDataTransmDl',TMeasurementValue)]
class SPdcchLoadCell(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('averCellsPdcchLoad',TMeasurementValue)]
class SSCellsConfiguration(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCellIdScell',TOaMLnCelId), ('sCellServCellIndex',TSCellServCellIndex), ('transmModeScell',ETransmMode), ('maxNumOfLayersScell',EMaxNumOfLayers), ('cqiParamsScell',SCqiParamsScell), ('container',UCaWmpDcmSCellContainer)]
class SSCellsRemove(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCellIdScell',TOaMLnCelId)]
class SServiceInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('serviceType',ETestabilityServiceType), ('serviceAddr',TAaSysComSicad)]
class SL2DlPhyAddressess(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('pdschCw0SendReqAddress',TAaSysComSicad), ('pdschCw1SendReqAddress',TAaSysComSicad), ('srioType9Cos',prophy.u32), ('srioType9StreamId',prophy.u32), ('pdschEventQueueId',prophy.u32)]
class SL2MacPsAddresses(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfUeGroups',TNumberOfItems), ('psUserUl',prophy.bytes(size=MAX_NUM_UEGROUP_PER_BB_POOL)), ('psUserDl',prophy.bytes(size=MAX_NUM_UEGROUP_PER_BB_POOL)), ('dataCtrlDLPdcchClient',TAaSysComSicad)]
class SPrachUsageRatio2(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('nbrOfDicardedRACHMessage3Meas',TMeasurementValue), ('nbrOfDicardedNonPrioritizedRACHMessage3Meas',TMeasurementValue)]
class SAperiodicCsiTriggerParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('aperiodicCsiTrigger1',TAperiodicCsiTrigger), ('aperiodicCsiTrigger2',TAperiodicCsiTrigger), ('padding',prophy.u16)]
class SSCellResultsParameters(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCellIdScell',TOaMLnCelId), ('messageResult',SMessageResult)]
class MAC_CellSetupReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('phyCellId',TPhyCellId), ('commonCellParams',SCommonCellParams), ('phichParams',SPhichParams), ('pucchParams',SPucchConfiguration), ('soundingRsUlConfigCommon',SSoundingRsUlConfigCommon), ('hsTrainScenario',EHsTrainScenario), ('harqMaxMsg3',TOaMHarqMaxMsg3), ('bufferDiscardParams',SBufferDiscardParams), ('voLteThresholdParams',SVoLteThresholdParams), ('tmpName',TNumberOfItems), ('rlcDlLcpInfo',prophy.array(SRlcLcpInfo,bound='tmpName')), ('container',UWmpDcmCellContainer)]
class MAC_CellSetupResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('macUser',TAaSysComSicad), ('macSgnl',TAaSysComSicad), ('macCellMeas',TAaSysComSicad), ('macTest',TAaSysComSicad), ('macUserPsService',TAaSysComSicad)]
class MAC_CellReconfigurationReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('activationTimeSFN',TSfn), ('commonCellParams',SCommonCellParams), ('phichParams',SPhichParams), ('pucchParams',SPucchConfiguration), ('soundingRsUlConfigCommon',SSoundingRsUlConfigCommon), ('hsTrainScenario',EHsTrainScenario), ('harqMaxMsg3',TOaMHarqMaxMsg3), ('container',UWmpDcmCellContainer)]
class MAC_CellReconfigurationResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TOaMLnCelId)]
class MAC_RachSetupReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('lCelId',TLocalCellResId), ('rachParams',SRachParams)]
class MAC_RachSetupResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class MAC_CellDeleteReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId)]
class MAC_CellDeleteResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class MAC_TxAntennaConfChangeReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('numAvailableTxAntennas',TNumAntennas)]
class MAC_TxAntennaConfChangeResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class MAC_UserSetupReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('ueGroup',TUeGroup), ('transactionId',TTransactionID), ('numOfScellIds',TNumberOfItems), ('lnCelIdSCell',prophy.array(TOaMLnCelId,bound='numOfScellIds')), ('spsCrntiAllocationReq',TBoolean), ('handoverType',EHandoverType), ('ueSetupParams',SUeSetupParams), ('container',UWmpDcmUserContainer), ('cqiParams',SCqiParams), ('controlOffsets',SPuschControlOffsets), ('ueParams',SUeParams), ('ttiBundlingEnable',TBoolean), ('tpcPdcchConfigParams',STpcPdcchConfigParams), ('ulPCUeParams',SUlPCUeParams), ('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated), ('numSRbs',TNumberOfItems), ('sRbInfoList',prophy.array(SSrbInfo,bound='numSRbs')), ('numRbs',TNumberOfItems), ('rbInfoList',prophy.array(SRbInfo,bound='numRbs'))]
class MAC_UserSetupResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('ueGroup',TUeGroup), ('transactionId',TTransactionID), ('spsCrnti',TCrnti), ('macUserAddress',TAaSysComSicad), ('raPreambleIndex',TRaPreambleIndex), ('prachMaskIndex',TPrachMaskIndex), ('numSRbs',TNumberOfItems), ('sRbList',prophy.array(SSRbList,bound='numSRbs')), ('numDRbs',TNumberOfItems), ('dRbList',prophy.array(SDRbList,bound='numDRbs'))]
class MAC_L2CallConfigReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('ueGroup',TUeGroup), ('transactionId',TTransactionID), ('numOfScellIds',TNumberOfItems), ('lnCelIdSCell',prophy.array(TOaMLnCelId,bound='numOfScellIds')), ('spsCrntiAllocationReq',TBoolean), ('handoverType',EHandoverType), ('ueSetupParams',SUeSetupParams), ('container',UWmpDcmUserContainer), ('cqiParams',SCqiParams), ('controlOffsets',SPuschControlOffsets), ('ueParams',SUeParams), ('ttiBundlingEnable',TBoolean), ('tpcPdcchConfigParams',STpcPdcchConfigParams), ('ulPCUeParams',SUlPCUeParams), ('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated), ('numSRbs',TNumberOfItems), ('sRbInfoList',prophy.array(SSrbInfo,bound='numSRbs')), ('numRbs',TNumberOfItems), ('rbInfoList',prophy.array(SRbInfo,bound='numRbs'))]
class MAC_L2CallConfigResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('ueGroup',TUeGroup), ('transactionId',TTransactionID), ('spsCrnti',TCrnti), ('macUserAddress',TAaSysComSicad), ('raPreambleIndex',TRaPreambleIndex), ('prachMaskIndex',TPrachMaskIndex), ('numSRbs',TNumberOfItems), ('sRbList',prophy.array(SSRbList,bound='numSRbs')), ('numDRbs',TNumberOfItems), ('dRbList',prophy.array(SDRbList,bound='numDRbs'))]
class MAC_UserModifyReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('crnti',TCrnti), ('ueId',TUeId), ('measGapStopRequired',TBoolean), ('gapPattern',EMeasGapOffset), ('measGapOffset',TMeasGapOffset), ('ambrParams',SAmbrParams), ('drxParameters',SDrxParameters), ('actNewTransmMode',ETransmMode), ('cqiParams',SCqiParams), ('ueInactivityTimer',TOaMInactivityTimer)]
class MAC_UserModifyResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TOaMLnCelId), ('crnti',TCrnti), ('ueId',TUeId)]
class MAC_UserDeleteReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('validUeId',TBoolean), ('ueId',TUeId), ('transactionId',TTransactionID), ('spsCrntiReleaseReq',TBoolean), ('ueReleaseCause',ECauseLte), ('specificUeReleaseCause',ESpecificCauseLte)]
class MAC_UserDeleteResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class MAC_RadioBearerSetupReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('spsCrntiAllocationReq',TBoolean), ('ueSetupParams',SUeSetupParams), ('container',UWmpDcmUserContainer), ('cqiParams',SCqiParams), ('ueParams',SUeParams), ('tpcPdcchConfigParams',STpcPdcchConfigParams), ('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated), ('numSRbs',TNumberOfItems), ('sRbInfoList',prophy.array(SSrbInfo,bound='numSRbs')), ('numDRbs',TNumberOfItems), ('drbInfoList',prophy.array(SRbInfo,bound='numDRbs'))]
class MAC_RadioBearerSetupResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('spsCrnti',TCrnti), ('container',UUlTfrParamContainer), ('numSRbs',TNumberOfItems), ('sRbList',prophy.array(SSRbList,bound='numSRbs')), ('numDRbs',TNumberOfItems), ('dRbList',prophy.array(SDRbList,bound='numDRbs'))]
class MAC_RadioBearerDeleteReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('spsCrntiReleaseReq',TBoolean), ('spsCrnti',TCrnti), ('container',UWmpDcmUserContainer), ('ueParams',SUeParams), ('numSRbs',TNumberOfItems), ('sRbList',prophy.array(TSrbId,bound='numSRbs')), ('numDRbs',TNumberOfItems), ('dRbList',prophy.array(TDrbId,bound='numDRbs'))]
class MAC_RadioBearerDeleteResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('container',UUlTfrParamContainer), ('numSRbs',TNumberOfItems), ('sRbList',prophy.array(SSRbList,bound='numSRbs')), ('numDRbs',TNumberOfItems), ('dRbList',prophy.array(SDRbList,bound='numDRbs'))]
class MAC_RadioBearerModifyReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('spsCrntiAllocationReq',TBoolean), ('ueSetupParams',SUeSetupParams), ('container',UWmpDcmUserContainer), ('cqiParams',SCqiParams), ('ueParams',SUeParams), ('tpcPdcchConfigParams',STpcPdcchConfigParams), ('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated), ('tmpName',TNumberOfItems), ('cqiParamsScell',prophy.array(SCqiParamsScell,bound='tmpName')), ('numSRbs',TNumberOfItems), ('sRbInfoList',prophy.array(SSrbInfo,bound='numSRbs')), ('numRbs',TNumberOfItems), ('rbInfoList',prophy.array(SRbInfo,bound='numRbs'))]
class MAC_RadioBearerModifyResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('spsCrnti',TCrnti), ('container',UUlTfrParamContainer), ('numSRbs',TNumberOfItems), ('sRbList',prophy.array(SSRbList,bound='numSRbs')), ('numDRbs',TNumberOfItems), ('dRbList',prophy.array(SDRbList,bound='numDRbs'))]
class MAC_TriggerInactivityInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('lnCellIdScell',TOaMLnCelId), ('crnti',TCrnti), ('ueId',TUeId), ('direction',EDirection), ('trigger',TTrigger)]
class MAC_DefaultUserConfigReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('l3Address',TAaSysComSicad), ('userInfo',SUserInfoMac)]
class MAC_DefaultUserConfigResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('tmpName',TNumberOfItems), ('nodeAddress',prophy.array(TAaSysComNid,bound='tmpName'))]
class MAC_PcchDataSendReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('numberOfPagingItems',TNumberOfItems), ('pagingItems',prophy.array(SPagingItem,bound='numberOfPagingItems'))]
class MAC_CcchDataSendReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('size',TL3MsgSize), ('data',prophy.array(u8,bound='size'))]
class MAC_CcchDataReceiveInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('maxNumOfUes',u32), ('msg3Info',prophy.array(SMsg3Info,bound='maxNumOfUes'))]
class MAC_RadioLinkStatusInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('sCellServCellIndex',TSCellServCellIndex), ('srbId',TSrbId), ('drbId',TDrbId), ('rlsCause',ERlsCause)]
class MAC_UlResourceControlReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('cqiParams',SCqiParams), ('ueSetupParams',SUeSetupParams), ('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated), ('tpcPdcchConfigParams',STpcPdcchConfigParams), ('container',UUlResCtrlParamContainer), ('tmpName',TNumberOfItems), ('cqiParamsScell',prophy.array(SCqiParamsScell,bound='tmpName'))]
class MAC_UlResourceControlResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('sCellServCellIndex',TSCellServCellIndex), ('container',UUlTfrParamContainer)]
class MAC_ErrorInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('numSRbs',TNumberOfItems), ('sRbList',prophy.array(SSRbList,bound='numSRbs')), ('numDRbs',TNumberOfItems), ('dRbList',prophy.array(SDRbList,bound='numDRbs'))]
class MAC_CrntiReserveReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('numCrnti',TNumberOfItems), ('crntiList',prophy.array(TCrnti,bound='numCrnti'))]
class MAC_CrntiReserveResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class MAC_CrntiFreeReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId)]
class MAC_CrntiFreeResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class MAC_SpsCrntiAllocationReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class MAC_SpsCrntiAllocationResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('spsCrnti',TCrnti)]
class MAC_SpsCrntiReleaseReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('spsCrnti',TCrnti)]
class MAC_SpsCrntiReleaseResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class MAC_SystemInfoScheduleReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('transactionId',TTransactionID), ('activationTimePresent',TBoolean), ('activationTime',TFrameNumber), ('mibSfnPosition',TMibSfnPosition), ('mibSfnLength',TMibSfnLength), ('siWindowLen',EOaMSiWindowLen), ('numSIs',TNumberOfItems), ('siSchedule',prophy.array(SSysInfoSchedule,bound='numSIs')), ('numberOfSIs',TNumberOfItems), ('siList',prophy.array(SSiList,bound='numberOfSIs')), ('container',USystemInfoContainer), ('siTypeSegmented',ESysInfoTypeId), ('numOfSiSegments',TNumberOfItems), ('siSegmentSize',prophy.array(SSiSegmentSize,bound='numOfSiSegments')), ('numOfSiBytes',TNumberOfItems), ('siSegmentData',prophy.array(u8,bound='numOfSiBytes'))]
class MAC_SystemInfoScheduleResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('transactionId',TTransactionID)]
class MAC_SystemInfoInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('gpsTimeAvailable',TBoolean)]
class MAC_EnableSystemInfoReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('ibType',EIbType), ('activationFlag',EActivationFlag)]
class MAC_EnableSystemInfoResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class MAC_SIB12BroadcastReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('transactionId',TTransactionID), ('messageIdentifier',prophy.u16), ('serialNumber',prophy.u16), ('numberOfBroadcastsRequested',prophy.u16), ('padding',prophy.u16), ('repetitionPeriod',prophy.u32), ('killFlag',TBoolean), ('numOfSiSegments',TNumberOfItems), ('siSegmentSize',prophy.array(SSiSegmentSize,bound='numOfSiSegments')), ('numOfSiBytes',TNumberOfItems), ('siSegmentData',prophy.array(u8,bound='numOfSiBytes'))]
class MAC_SIB12BroadcastResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('transactionId',TTransactionID), ('messageIdentifier',prophy.u16), ('serialNumber',prophy.u16), ('messageResult',SMessageResult)]
class MAC_SIB12BroadcastInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('messageIdentifier',prophy.u16), ('serialNumber',prophy.u16), ('numberOfBroadcasts',prophy.u16)]
class MAC_BcchModIndReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('transactionId',TTransactionID), ('activationTimePresent',TBoolean), ('activationTime',TFrameNumber), ('duration',SDuration), ('pagingNb',EPagingNB), ('pagingBitmapSize',TL3MsgSize), ('pagingBitmapData',prophy.array(u8,bound='pagingBitmapSize')), ('size',TL3MsgSize), ('data',prophy.array(u8,bound='size'))]
class MAC_BcchModIndResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('transactionId',TTransactionID), ('activationTime',TFrameNumber)]
class MAC_UeStatusReportReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class MAC_UeStatusReportResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('container',UUeStatusReportRespContainerDcm)]
class MAC_UlTfrParamUpdateInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('container',UUlTfrParamContainer)]
class MAC_UlTfrParamReportReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class MAC_UlTfrParamReportResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('container',UUlTfrParamContainer)]
class MAC_UlPowerOffsetControlUpdateInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('container',UUlPowerControlUpdateIndContainer)]
class MAC_BackOffIndIndexUpdateInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('container',UBackoffIndIndexUpdateIndContainer)]
class MAC_RlcDataRegisterReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueId',TUeId), ('tupUserAddress',STupUserAddress)]
class MAC_RlcDataRegisterResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('ueId',TUeId)]
class MAC_RlcDataReceiveInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sRingBufferUlItem',SRingBufferUlItem)]
class MAC_RlcDataTestSupportReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('c',SRingBufferSendReq), ('size',TL3MsgSize), ('data',prophy.array(u8,bound='size'))]
class MAC_RlcDataTestSupportUlReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('c',SRingBufferUlItem), ('size',TL3MsgSize), ('data',prophy.array(u8,bound='size'))]
class MAC_RlcDataSendReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sRingBufferSendReq',SRingBufferSendReq)]
class MAC_RlcDataSendResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tmpName',TNumberOfItems), ('ueRbPacketIdList',prophy.array(SRbUePacketId,bound='tmpName'))]
class MAC_RlcDataDiscardInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tmpName',TNumberOfItems), ('ueRbPacketId',prophy.array(SUeRbPacketId,bound='tmpName'))]
class MAC_StopSchedulingReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueId',TUeId), ('handoverType',EHandoverType), ('enableRlcBufferStateReport',TBoolean), ('numDRbs',TNumberOfItems), ('rbStopSchedulingInfo',prophy.array(SRbStopSchedulingInfo,bound='numDRbs'))]
class MAC_StopSchedulingResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('ueId',TUeId), ('numBearers',TNumberOfItems), ('bearerList',prophy.array(SBearerList,bound='numBearers'))]
class MAC_StartSchedulingReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueId',TUeId)]
class MAC_StartSchedulingResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('ueId',TUeId)]
class MAC_StopSchedulingCellReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId)]
class MAC_StopSchedulingCellResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class MAC_RlcDataBufferResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dlRbMasterParam',SRingBufferDlParam), ('dlRbSlaveParam',SRingBufferDlParam), ('ulRbMasterParam',SRingBufferUlParam)]
class MAC_InternalAddressReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('transactionId',TTransactionID), ('nodeAddress',SNodeAddress)]
class MAC_InternalAddressResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('transactionId',TTransactionID)]
class MAC_MeasurementInitiationReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('measurementId',TMeasurementId), ('reportPeriod',TPeriod), ('samplingPeriod',TPeriod), ('tmpName',TNumberOfItems), ('measurementGroupTypeList',prophy.array(EMeasurementGroupType,bound='tmpName'))]
class MAC_MeasurementInitiationResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('measurementId',TMeasurementId)]
class MAC_MeasurementReportInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('measurementId',TMeasurementId), ('tmpName',TNumberOfItems), ('measurementGroupTypeList',prophy.array(EMeasurementGroupType,bound='tmpName')), ('tmpName',TNumberOfItems), ('measReportValue',prophy.array(SMeasReportValue,bound='tmpName'))]
class MAC_MeasurementTerminationReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('measurementId',TMeasurementId)]
class MAC_MeasurementTerminationResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('measurementId',TMeasurementId)]
class MAC_CoefficientRequestReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tmpName',TNumberOfItems), ('caBw',prophy.array(ECarrierBandwidth,bound='tmpName'))]
class MAC_CoefficientRequestResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('tmpName',TNumberOfItems), ('macCoefficientValues',prophy.array(SMacCoefficientValues,bound='tmpName'))]
class MAC_StartUlTestModelReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('referenceChannelNumber',EReferenceChannelNumber), ('resourceBlockOffset',TResourceBlock), ('reportingTimeInterval',TReportingTimeInterval), ('harqUsed',TBoolean), ('digitalOutputEnabled',TBoolean), ('ulTestModelDigitalOutputParams',SUlTestModelsDigitalOutputParams), ('additionalMeasurementParameters',UAdditionalMeasurementParameters)]
class MAC_StartUlTestModelResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class MAC_ThroughputMeasurementReportInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('resultStatus',EStatusLte), ('throughputResult',TThroughputResult), ('resultCounters',SResultCounters), ('throughputResultStationaryUe',TThroughputResult), ('resultCountersStationaryUe',SResultCounters)]
class MAC_StopUlTestModelReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId)]
class MAC_StopUlTestModelResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class MAC_StartUlCtrlChannelMeasReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('measType',EUlCtrlChannelMeasType), ('reportingTimeInterval',TReportingTimeInterval), ('receptionSubframe',TSubframes), ('expectionSubframe',TSubframes), ('ulCtrlChannelParams',UUlCtrlChannelParams)]
class MAC_StartUlCtrlChannelMeasResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class MAC_UlCtrlChannelMeasReportInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('resultStatus',EStatusLte), ('UlCtrlChannelMeasCounters',SUlCtrlChannelMeasCounters), ('container',UlCtrlChannelMeasReportContainer)]
class MAC_StopUlCtrlChannelMeasReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId)]
class MAC_StopUlCtrlChannelMeasResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class MAC_MeasGapStartReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('measGapOffset',UMeasGapOffset)]
class MAC_MeasGapStartResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class MAC_MeasGapStopReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class MAC_MeasGapStopResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class MAC_StartRfLoopTestReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('reportingTimeInterval',TReportingTimeInterval)]
class MAC_StartRfLoopTestResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class MAC_StopRfLoopTestReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId)]
class MAC_StopRfLoopTestResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class MAC_CellReconfigurationDeltaReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('dcmContainer',UWmpDcmCellReconfigurationContainer)]
class MAC_CellReconfigurationDeltaResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class MAC_DisableDiscTimerInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueId',TUeId), ('ueIndex',TUeIndex)]
class MAC_ResumeDiscTimerInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueId',TUeId), ('ueIndex',TUeIndex)]
class MAC_RaPdcchOrderReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('crnti',TCrnti), ('ueId',TUeId)]
class MAC_UeInfoReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('ueId',TUeId), ('ueInfo',EUeInfo)]
class MAC_UeInfoResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TOaMLnCelId), ('ueId',TUeId), ('ueInfo',UUeInfo)]
class MAC_TestRlcDataInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueId',TUeId), ('radioBearerId',TRadioBearerId), ('size',TL3MsgSize), ('data',prophy.bytes(size=1))]
class MAC_StartRefSyncSReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId)]
class MAC_StartRefSyncSResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class MAC_StopRefSyncSReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId)]
class MAC_StopRefSyncSResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class MAC_RadioBearerReleaseInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLCelId), ('numOfUsers',TNumberOfItems), ('ueList',prophy.array(SUeList,bound='numOfUsers'))]
class MAC_CongestionInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('gbrCongestionCause',ESpecificCauseLte), ('numOfExceedingRb',prophy.u32), ('cellResourceGroupId',TCellResourceGroupId)]
class MAC_CongestionIndAck(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('cellResourceGroupId',TCellResourceGroupId), ('congestionResolutionResult',SMessageResult)]
class MAC_BearerModifyReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('crnti',TCrnti), ('ueId',TUeId), ('ttiBmMeasActivate',TBoolean), ('ambrParams',SAmbrParams), ('numDrbs',TNumberOfItems), ('drbInfoList',prophy.array(SRbModifyInfo,bound='numDrbs'))]
class MAC_BearerModifyResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TOaMLnCelId), ('crnti',TCrnti), ('ueId',TUeId)]
class MAC_WmpMeasurementInitiationReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCellId',TCellId), ('tmpName',TNumberOfItems), ('measurementGroupTypeList',prophy.array(EMeasurementGroupTypeWmp,bound='tmpName'))]
class MAC_WmpMeasurementInitiationResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCellId',TCellId), ('requestResult',SMessageResult), ('tmpName',TNumberOfItems), ('measurementGroupTypeList',prophy.array(EMeasurementGroupTypeWmp,bound='tmpName')), ('tmpName',TNumberOfItems), ('measReportValue',prophy.array(TMeasurementValue,bound='tmpName'))]
class MAC_WmpMeasurementReportInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCellId',TCellId), ('tmpName',TNumberOfItems), ('measurementGroupTypeList',prophy.array(EMeasurementGroupTypeWmp,bound='tmpName')), ('tmpName',TNumberOfItems), ('measReportValue',prophy.array(TMeasurementValue,bound='tmpName'))]
class MAC_WmpMeasurementTerminationReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId)]
class MAC_WmpMeasurementTerminationResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class MAC_PowerHeadroomBundledInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('numOfUePhr',u32), ('uePhrList',prophy.array(SUePhr,bound='numOfUePhr'))]
class MAC_CaUserReconfigurationReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('crnti',TCrnti), ('ueId',TUeId), ('relatedProcedure',ERelatedProcedure), ('aperiodicCsiTriggerParams',SAperiodicCsiTriggerParams), ('container',UCaUserReconfigurationContainer), ('tmpName',TNumberOfItems), ('r10n1PucchAnCsList',prophy.array(SR10n1PucchAnCsElement,bound='tmpName')), ('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated), ('tmpName',TNumberOfItems), ('sCellsRemove',prophy.array(SSCellsRemove,bound='tmpName')), ('tmpName',TNumberOfItems), ('sCellsConfiguration',prophy.array(SSCellsConfiguration,bound='tmpName'))]
class MAC_CaUserReconfigurationResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('crnti',TCrnti), ('ueId',TUeId), ('tmpName',TNumberOfItems), ('sCellResultsForRemoval',prophy.array(SSCellResultsParameters,bound='tmpName')), ('tmpName',TNumberOfItems), ('sCellResultsForConfiguration',prophy.array(SSCellResultsParameters,bound='tmpName')), ('messageResult',SMessageResult)]
class MAC_RrcConnectionReconfCompletedReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('ueId',TUeId), ('relatedProcedure',ERelatedProcedure), ('sCellServCellIndex',TSCellServCellIndex), ('cqiParams',SCqiParams), ('cqiParamsScell',SCqiParamsScell), ('actNewTransmMode',ETransmMode), ('actNewTransmModeScell',ETransmMode)]
class MAC_UlVoLteReceptionInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('numUes',TNumberOfItems), ('ueInfoList',prophy.array(SUeInfo,bound='numUes'))]
class MAC_UserGroupReserveReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('ueId',TUeId)]
class MAC_UserGroupReserveResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TOaMLnCelId), ('ueId',TUeId), ('ueGroup',TUeGroup)]
class MAC_UserGroupFreeReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('ueId',TUeId), ('ueGroup',TUeGroup)]
class MAC_UserGroupFreeResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TOaMLnCelId), ('ueId',TUeId)]
class MAC_BufferStatusTriggerReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('lnCellIdServCell',TOaMLnCelId), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber)]
class MAC_BundledContentionResInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numberOfContResMsg',TNumberOfItems), ('pduMuxContentionResInd',prophy.bytes(size=MAX_NUM_CONT_RES_PER_MSG))]
class MAC_ConfigChangeInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('ueIndex',TUeIndex), ('hasDrxConfigId',TBooleanU8), ('drxConfigId',TConfigurationId)]
class MAC_CcchDataInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('ueIndex',TUeIndex), ('size',TL3MsgSize), ('tempUeNeeded',TBoolean), ('macCeFlag',TBoolean)]
class MAC_DlBufferStatusBundleInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('numOfLchHaveData',TNumOfLch), ('numOfMessages',TNumberOfItems), ('dlBsr',prophy.array(SDlBufferStatusInd,bound='numOfMessages'))]
class MAC_HarqReleaseReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('tmpName',TNumberOfItems), ('harqReleaseInfo',prophy.array(SHarqReleaseInfo,bound='tmpName'))]
class MAC_MacCrntiCeInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('tempCrnti',TCrnti), ('ueIndex',TUeIndex), ('tempUeIndex',TUeIndex), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber)]
class MAC_MeasInitReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('reportClientSicad',TAaSysComSicad), ('cellId',TCellId), ('reportId',TMeasurementReportId), ('period',TPeriod), ('samplingPeriod',TPeriod), ('groupCount',TNumberOfItems), ('groupList',prophy.array(EMeasurementGroupType,bound='groupCount'))]
class MAC_MeasInitResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('reportId',TMeasurementReportId), ('messageResult',SMessageResult)]
class MAC_MeasReportInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('reportId',TMeasurementReportId), ('measurementCount',u32), ('measurementValues',prophy.array(SMgmtMeasurement,bound='measurementCount'))]
class MAC_MeasTermInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId)]
class MAC_MeasTermReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('reportId',TMeasurementReportId)]
class MAC_MeasTermResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('reportId',TMeasurementReportId), ('messageResult',SMessageResult)]
class MAC_OverloadInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('numberOfOverloadTtis',TNumberOfItems), ('maxNumberOfUesPerOverloadTti',TNumberOfItems)]
class MAC_PduMuxBundledDataReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellIdU16), ('frameNumber',prophy.u16), ('subFrameNumber',prophy.u8), ('cfi',TCfiU8), ('lastTbInTti',TBooleanU8), ('latencyBudgetExceeded',TBooleanU8), ('numOfBundledPduMuxMsgs',prophy.u8), ('data',prophy.bytes(size=1))]
class MAC_PduMuxDataResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('frameNumber',prophy.u16), ('subFrameNumber',prophy.u16), ('resLength',prophy.u32), ('resArray',prophy.bytes(size=1))]
class MAC_TCrntiDeleteInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('ueIndex',TUeIndex), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('sendDeleteReqToMacData',TBoolean)]
class MAC_UlBufferStatusInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('header',SMacMessageHeader), ('payload',SUlBufStatusIndPayload)]
class MAC_UlDataReceivedReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('tmpName',TNumberOfItems), ('data',prophy.array(SDataReceived,bound='tmpName'))]
class MAC_UlDataReceivedResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('tmpName',TNumberOfItems), ('data',prophy.array(SDataReceived,bound='tmpName'))]
class MAC_AddressConfigReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('transactionId',TTransactionID), ('poolId',TPoolId), ('enbId',TOaMLnBtsId), ('numOfPools',TNumberOfItems), ('poolInfo',prophy.array(SL2PoolInfo,bound='numOfPools'))]
class MAC_AddressConfigResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('transactionId',TTransactionID), ('numOfTestabilityServices',TNumberOfItems), ('serviceInfo',prophy.array(SServiceInfo,bound='numOfTestabilityServices'))]
class MAC_CaCellConfigReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('poolId',TPoolId), ('transactionId',TTransactionID), ('typeOfOperation',ECATypeOfOperation), ('l2DlPhyAddressess',SL2DlPhyAddressess), ('l2MacPsAddresses',SL2MacPsAddresses)]
class MAC_CaCellConfigResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TOaMLnCelId), ('poolId',TPoolId), ('transactionId',TTransactionID)]
class MAC_UeMeasReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID)]
class MAC_UeMeasResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TOaMLnCelId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('roundTripDelayEstimate',prophy.u32)]
class MAC_RemoveUesInCellReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('pCelId',TOaMLnCelId), ('tmpName',TNumberOfItems), ('ueToRemove',prophy.array(TUeIndex,bound='tmpName'))]
class MAC_RemoveUesInCellResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TOaMLnCelId)]
class MAC_CaUserReconfigurationCompleteReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('crnti',TCrnti), ('ueId',TUeId), ('procedureResults',ECAProcedureResults)]
class MAC_CaUserReconfigurationCompleteResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TOaMLnCelId), ('crnti',TCrnti), ('ueId',TUeId)]
class MAC_PduMuxExceptionInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('frameNumber',prophy.u16), ('subFrameNumber',prophy.u16), ('resLength',prophy.u32), ('resArray',prophy.bytes(size=1))]
