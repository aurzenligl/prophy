import prophy 
from externals import *


NUM_K2_PER_LSP_IN_LRC = 3
NUM_PHY_PER_LSP_IN_LRC = 6
MAX_NUM_OF_POOLS_IN_SUPER_POOL = 2
INVALID_UEGROUP = 0xFFFFFFFF
MAX_NUM_OF_L2DEPLOYABLE_NODE = 8
MAX_NUM_CELL_PER_ADJ_ENB = 24
MAX_NUM_OF_SUBCELLS = 12
MAX_NUM_OF_ANT_IN_CELL = 12
INVALID_UEINDEX = 0xFFFF
UE_INDEX_INVALID = 0xFFFF
MAX_NUM_USER_PER_BB_POOL_HIGH = 1200
MAX_NUM_USER_TEMP_PER_BB_POOL_DCM = 200
MAX_NUM_USER_PER_BB_POOL_TDD_SUPER_CELL = 480
MAX_NUM_USER_PERM_PER_BB_POOL_HIGH = 1200
MAX_NUM_USER_PERM_PER_BB_POOL_LOW = 840
MAX_NUM_UEGROUP_PER_BB_POOL_RL70 = 16
NUM_UEGROUP_PER_BB_POOL_FSM3_RL70 = 12
NUM_UEGROUP_PER_BB_POOL_FSM3 = 4
NUM_UEGROUP_PER_BB_POOL_FSM2 = 1
NUM_UEGROUP_BITS_FSM3_RL70 = 4
NUM_UEGROUP_BITS_FSM3 = 2
NUM_UEGROUP_BITS_FSM2 = 0
MAX_LCID = 10
NUM_OF_ANTENNAGROUPS = 4
MAX_NUM_OF_PARALLEL_PROCEDURES = 40
MAX_NUM_USER_PER_BB_POOL_TDD = 600
MAX_NUM_CELL_PER_BB_POOL_TDD = 1
MAX_NUM_USER_PER_BB_POOL_FDD = 840
MAX_NUM_CELL_PER_BB_POOL_FDD = 2
MAX_NUM_USER_PER_BB_POOL = 840
MAX_NUM_CELL_PER_BB_POOL = 2
MAX_NUM_USER_PER_MCU = 2520
MAX_NUM_CELL_PER_MCU = 6
MAX_NUM_CUPLANE_ADDRESSES = 6
MAX_NUM_OF_S1_LINK_ID = 16
TIMEOUT_PATH_SUP_RESP_FROM_TRSW = 1000
ANTENNA_PORT_ALL = 65535
ANTENNA_PORT_PORT3 = 8
ANTENNA_PORT_PORT2 = 4
ANTENNA_PORT_PORT1 = 2
ANTENNA_PORT_PORT0 = 1
MAX_NUM_SERVED_PLMN = 32
MAX_LENGTH_MMENAME = 150
MAX_LENGTH_FILENAME = 300
MAX_NUM_COEFF_BW = 8
VARIABLE_SIZE_ARRAY_DUMMY = 65535
MAX_SI_SEGMENT_DATA = 10240
MAX_NUM_SI_SEGMENT = 64
MAX_PAGING_BITMAP_DATA = 4
MAX_NUM_MEAS_REPORT_VALUE = 6
TUP_MAX_PAYLOAD_SIZE = 8188
TUP_DATA_BLOCK_SIZE = 2048
MAX_MEAS_TYPE_ID = 18
MAX_MEAS_GROUP_TYPE_ID = 22
MAX_PAGING_ITEMS = 8
MAX_TRANSPORT_LAYER_ADDRESS_LENGTH = 16
MAX_NUM_SRB_PER_USER_WO_SRB1 = 1
MAX_NUM_OF_ENB_IP_ADDR = 4
MAX_NUM_SIS = 17
MAX_CCCH_DATA_UL = 6
MAX_CCCH_DATA = 5120
MAX_PCCH_DATA = 425
MAX_RLC_DATA = 8193
MAX_SI_DATA = 280
MAX_NUM_S1_SCTP_LINKS = 16
MAX_NUM_X2_SCTP_LINKS = 256
MAX_NUM_USER_ID_RESERVED_FOR_TM = 71
MAX_NUM_USER_PER_CELL = 840
MAX_NUM_CELL_PER_ENB = 6
MAX_USERS_IN_NODEB_LTE = 2520
MAX_NUM_OF_S1_LINK = 300
MAX_NMBR_CODEWORDS = 2
MAX_NUM_DRB_PER_USER = 8
MAX_NUM_SRB_PER_USER = 2
MAX_NUM_OF_LCR = 18
MAX_NUM_OF_CORES_IN_FARADAY = 3
MAX_NUM_OF_DSP = 9
MAX_NUM_OF_BB_UNIT = 3
MAX_NUM_OF_C_UNIT = 1
MAX_NR_OF_PHY_ENTITY = 2
MAX_NUM_PRBS_DIV32 = 4
MAX_RB_ID = 34
MAX_SRB_ID = 2
MAX_DRB_ID = 32
MAX_SINT16 = 0x7FFF
MAX_UINT16 = 0xFFFF
MAX_SINT32 = 0x7FFFFFFF
MAX_UINT32 = 0xFFFFFFFF
OAM_EARFCNDL_MAX = 65535
OAM_EARFCNDL_MIN = 0
MAX_NUM_RB_PER_USER = (MAX_NUM_SRB_PER_USER + MAX_NUM_DRB_PER_USER)
MAX_NMBR_OF_TEIDS = (2 * MAX_NUM_DRB_PER_USER)
MAX_NUM_USER_ID_PER_ENB = (((MAX_NUM_CELL_PER_ENB*MAX_NUM_USER_PER_CELL)) + MAX_NUM_USER_ID_RESERVED_FOR_TM)
MAX_NUM_SCTP_ASSOCIATIONS = (MAX_NUM_S1_SCTP_LINKS+MAX_NUM_X2_SCTP_LINKS)
TIMEOUT_PATH_SUP_RESP_FROM_TUPU = (TIMEOUT_PATH_SUP_RESP_FROM_TRSW + 1000)
MAX_NUM_UEGROUP_PER_BB_POOL = NUM_UEGROUP_PER_BB_POOL_FSM3
MAX_NUM_USER_PER_BB_POOL_LOW = (MAX_NUM_USER_PERM_PER_BB_POOL_LOW+MAX_NUM_USER_TEMP_PER_BB_POOL_DCM)
MAX_UE_INDEX = (MAX_NUM_USER_PER_BB_POOL_HIGH-1)
MAX_UE_INDEX_TDD = (MAX_NUM_USER_PER_BB_POOL_TDD-1)

TOaMEarfcnDL = prophy.u16
TTaReportValue = prophy.u16
TBcchId = prophy.u32
TPcchId = prophy.u32
THbc = prophy.u32
TSubFrameNumber = prophy.u32
TCrnti = prophy.u32
TL3LinkId = prophy.u32
TGtpTeid = prophy.u32
TMui = prophy.u32
TNewDataIndicator = prophy.u32
THarqProcessNumber = prophy.u32
TRxPower = prophy.i32
TAbsoluteTimingAdvance = prophy.u32
TRadioBearerId = prophy.u32
TUeId = prophy.u32
TFamUeId = prophy.u32
TL3MsgSize = prophy.u32
TL3ConnectionId = prophy.u32
TUeContextId = prophy.u32
TTrackingAreaCode = prophy.u32
TMncLength = prophy.u32
TMnc = prophy.u32
TMcc = prophy.u32
TTxPower = prophy.i32
TMaxTxPower = prophy.i32
TPowerLoop = prophy.i32
TNumAntennas = prophy.u32
TFrameRepeatRate = prophy.u32
TMmeCode = prophy.u8
TMTMsi = prophy.u32
TImsi = prophy.u64
TTrackingAreaId = prophy.u32
TNumEnbIpAddr = prophy.u32
TSchedulingWeight = prophy.u32
TSiPeriodicity = prophy.u32
TSrOffset = prophy.u32
TPucchResourceIndex = prophy.u32
TResourceIndexCqi = prophy.u32
TSrbId = prophy.u32
TDrbId = prophy.u32
TConfigurationId = prophy.u32
TN1PucchAn = prophy.u32
TDeltaPucchShift = prophy.u32
TPucchNAnCs = prophy.u32
TNCqiRb = prophy.u32
TCqiPerMaxNumOfUesTti = prophy.u32
TMmeGroupId = prophy.u16
TDciFormatType = prophy.u8
TRelativeMMECapacity = prophy.u8
TResourceBlock = prophy.u32
TSubframes = prophy.u32
TTransportNetworkId = prophy.u32
TS1LinkId = prophy.u32
TNumHarqTransmissions = prophy.i32
TTimerPollReTransmit = prophy.u32
TTimerReordering = prophy.u32
TTimerStatusProhibit = prophy.u32
TReportingTimeInterval = prophy.u32
TThroughputResult = prophy.u32
TDscp = prophy.u32
TCounterLte = prophy.u64
TCounterCtrlLte = prophy.u32
TPuschControlOffsetIndex = prophy.u32
TPrachConfIndex = prophy.u32
TTddSpecialSubframeConf = prophy.u32
TPrachFreqOff = prophy.u32
TTddUplinkDownlinkConf = prophy.u32
TCoEffValue = prophy.u32
TAntennaPort = prophy.u32
TLomHandle = prophy.u32
TLomSessionId = prophy.u32
TUeS1X2Id = prophy.u32
TCellcMaxDrbBitrateUl = prophy.u32
TCellcMaxDrbBitrateDl = prophy.u32
TCellcMinDrbBitrateUl = prophy.u32
TCellcMinDrbBitrateDl = prophy.u32
TNumOfLayers = prophy.u32
TCodebookIndex = prophy.u32
TNIr = prophy.u32
TNumPrbs = prophy.u32
TStBFWeightPointer = prophy.u32
TTbSize = prophy.u32
TRedundancyVersion = prophy.u32
TCodeWordIndex = prophy.u32
TCfi = prophy.u32
TCrntiU16 = prophy.u16
TBooleanU8 = prophy.u8
TCfiU8 = prophy.u8
THarqProcessNumberU8 = prophy.u8
TNewDataIndicatorU8 = prophy.u8
TRedundancyVersionU8 = prophy.u8
TEModulationU8 = prophy.u8
TPoolId = prophy.u32
TUeCategory = prophy.u32
TRxPowerScaling = prophy.u32
TTxPowerScaling = prophy.u32
TPeriod = prophy.u32
TMeasurementId = prophy.u32
TMeasurementValue = prophy.u32
TPhyCellId = prophy.u32
TLcp = prophy.u32
TFlagOverflowDiscard = prophy.u32
TThOverflowDiscard = prophy.u32
TDiscBuffThr = prophy.u32
TRaPreamble = prophy.u32
TRaContResoT = prophy.u32
TUeGroup = prophy.u32
TUeIndex = prophy.u16
TEqId = prophy.u32
TCcId = prophy.u32

class ECauseLte(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ECauseLte_NotDefined',0), ('ECauseLte_RadioNetworkLayer_Unspecified',1), ('ECauseLte_RadioNetworkLayer_HandoverTriggered',2), ('ECauseLte_RadioNetworkLayer_Tx2RelocOverallExpiry',3), ('ECauseLte_RadioNetworkLayer_ReleaseDueToEUtranGeneratedReason',4), ('ECauseLte_RadioNetworkLayer_HandoverCancelled',5), ('ECauseLte_RadioNetworkLayer_PartialHandover',6), ('ECauseLte_RadioNetworkLayer_HoFailureInTargetEpcEnbOrTargetSystem',7), ('ECauseLte_RadioNetworkLayer_HoTargetNotAllowed',8), ('ECauseLte_RadioNetworkLayer_TS1RelocOverallExpiry',9), ('ECauseLte_RadioNetworkLayer_TS1RelocPrepExpiry',10), ('ECauseLte_RadioNetworkLayer_CellNotAvailable',11), ('ECauseLte_RadioNetworkLayer_UnknownTargetId',12), ('ECauseLte_RadioNetworkLayer_NoRadioResourcesAvailableInTargetCell',13), ('ECauseLte_RadioNetworkLayer_UnknownMmeUeS1ApId',14), ('ECauseLte_RadioNetworkLayer_UnknownEnbUeS1ApId',15), ('ECauseLte_RadioNetworkLayer_UnknownPairUeS1ApId',16), ('ECauseLte_RadioNetworkLayer_GracefulCellShutdownAborted',17), ('ECauseLte_RadioNetworkLayer_RadioConnectionWithUELost',18), ('ECauseLte_TransportLayer_TransportResourceUnavailable',101), ('ECauseLte_TransportLayer_Unspecified',102), ('ECauseLte_Nas_NormalRelease',201), ('ECauseLte_Nas_AuthenticationFailure',202), ('ECauseLte_Nas_Detach',203), ('ECauseLte_Nas_Unspecified',204), ('ECauseLte_Protocol_TransferSyntaxError',301), ('ECauseLte_Protocol_AbstractSyntaxErrorReject',302), ('ECauseLte_Protocol_AbstractSyntaxErrorIgnoreAndNotify',303), ('ECauseLte_Protocol_MessageNotCompatibleWithReceiverState',304), ('ECauseLte_Protocol_SemanticError',305), ('ECauseLte_Protocol_AbstractSyntaxErrorFalselyConstructedMessage',306), ('ECauseLte_Protocol_Unspecified',307), ('ECauseLte_Misc_ControlProcessingOverload',401), ('ECauseLte_Misc_NotEnoughUserPlaneProcessingResourcesAvailable',402), ('ECauseLte_Misc_HardwareFailure',403), ('ECauseLte_Misc_OmIntervention',404), ('ECauseLte_Misc_Unspecified',405), ('ECauseLte_Misc_UnknownPlmn',406), ('ECauseLte_BCCHSchedulingError',500), ('ECauseLte_MaxRlcRetransExceeded',501)]
class EResetRequestType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EResetRequestType_NoReset',0), ('EResetRequestType_BtsSiteReset',1), ('EResetRequestType_BtsReset',2)]
class ECarrierBandwidth(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ECarrierBandwidth_NotDefined',0), ('ECarrierBandwidth_1_4MHz',6), ('ECarrierBandwidth_3MHz',15), ('ECarrierBandwidth_5MHz',25), ('ECarrierBandwidth_10MHz',50), ('ECarrierBandwidth_15MHz',75), ('ECarrierBandwidth_20MHz',100), ('ECarrierBandwidth_05_05MHz',2525), ('ECarrierBandwidth_05_10MHz',2550), ('ECarrierBandwidth_10_05MHz',5025), ('ECarrierBandwidth_10_10MHz',5050)]
class EL2DeployableNode(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EL2DeployableNode_Basic1',0), ('EL2DeployableNode_Basic2',1), ('EL2DeployableNode_Basic3',2), ('EL2DeployableNode_Basic4',3), ('EL2DeployableNode_Extended1',10), ('EL2DeployableNode_Extended2',11), ('EL2DeployableNode_Extended3',12), ('EL2DeployableNode_Extended4',13), ('EL2DeployableNode_Extended5',14), ('EL2DeployableNode_Extended6',15), ('EL2DeployableNode_Extended7',16), ('EL2DeployableNode_Extended8',17), ('EL2DeployableNode_ArmL2Master',20), ('EL2DeployableNode_ArmL2Slave',21), ('EL2DeployableNode_DcmLrcPsMaster',22), ('EL2DeployableNode_DcmLrcPsSlave',23)]
class EUlCtrlChannelMeasType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EUlCtrlChannelMeasType_PucchAck',0), ('EUlCtrlChannelMeasType_Prach',1), ('EUlCtrlChannelMeasType_PucchCqi',2), ('EUlCtrlChannelMeasType_PuschHarqAck',3), ('EUlCtrlChannelMeasType_PucchAckFormat1bWithChannelSelection',4)]
class ERlcMode(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERlcMode_TM',0), ('ERlcMode_UM',1), ('ERlcMode_AM',2)]
class ESrPeriod(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ESrPeriod_5ms',0), ('ESrPeriod_10ms',1), ('ESrPeriod_20ms',2), ('ESrPeriod_40ms',3), ('ESrPeriod_80ms',4)]
class EStatusLte(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EStatusLte_Ok',0), ('EStatusLte_NotOk',1), ('EStatusLte_None',2)]
class EModulation(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EModulation_Bpsk',0), ('EModulation_Qpsk',1), ('EModulation_16qam',2), ('EModulation_64qam',3)]
class EBrowserObjectName(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EBrowserObjectName_Undefined',0), ('EBrowserObjectName_LteCell',1000), ('EBrowserObjectName_LteUser',1001), ('EBrowserObjectName_LteRadioBearer',1002), ('EBrowserObjectName_LteAccessBearerUser',1003), ('EBrowserObjectName_LtePlmn',1004), ('EBrowserObjectName_LteRepositoryL3',1050), ('EBrowserObjectName_LocalBrowserRepository',1051), ('EBrowserObjectName_LteMacTtiTrace',1100), ('EBrowserObjectName_LtePhyTtiTrace',1101), ('EBrowserObjectName_LteRssi',1102), ('EBrowserObjectName_LteModulationConstellation',1103), ('EBrowserObjectName_LteInterferencePlusNoisePerPrb',1104), ('EBrowserObjectName_LteSnr',1105), ('EBrowserObjectName_LteCellTotalRxPower',1106), ('EBrowserObjectName_LteBler',1107), ('EBrowserObjectName_LteSpectrumSnapshot',1108), ('EBrowserObjectName_LteCounter',1123), ('EBrowserObjectName_LteStatisticalMeas',1124), ('EBrowserObjectName_LteMeasS1Tup',1125), ('EBrowserObjectName_LteMeasX2Tup',1126), ('EBrowserObjectName_LteMeasEnbTup',1127), ('EBrowserObjectName_LteMeasCellTup',1128), ('EBrowserObjectName_LteMeasUserTup',1129), ('EBrowserObjectName_LteMeasS1AP',1130), ('EBrowserObjectName_LteMeasCellLoad',1131), ('EBrowserObjectName_LteMeasRLC',1132), ('EBrowserObjectName_LteMeasPDCPData',1133), ('EBrowserObjectName_LteMeasTransportLoad',1134), ('EBrowserObjectName_LteMeasPowerAndQualityUL',1135), ('EBrowserObjectName_LteMeasEPSBearer',1136), ('EBrowserObjectName_LteMeasRadioBearer',1137), ('EBrowserObjectName_LteMeasRRC',1138), ('EBrowserObjectName_LteMeasIntraENBHandover',1139), ('EBrowserObjectName_LteMeasPowerAndQualityDL',1140), ('EBrowserObjectName_LteMeasCellResource',1141), ('EBrowserObjectName_LteMeasCellThroughput',1142), ('EBrowserObjectName_LteMeasUEState',1143), ('EBrowserObjectName_LteMeasInterENBHandover',1144), ('EBrowserObjectName_LteMeasNeighbourCellRelatedHandover',1145), ('EBrowserObjectName_LteMeasInterSystemHandover',1146), ('EBrowserObjectName_LteMeasGeneralHandover',1147), ('EBrowserObjectName_LteCellPhy',1200), ('EBrowserObjectName_LteCellPlmnPhy',1201), ('EBrowserObjectName_LteCellUlPhy',1230), ('EBrowserObjectName_LteCellDlPhy',1270), ('EBrowserObjectName_LteCellMac',1301), ('EBrowserObjectName_LteUserMac',1302), ('EBrowserObjectName_LteMacDlCqiCirTable',1303), ('EBrowserObjectName_LteMacDlPsCellParams',1304), ('EBrowserObjectName_LteCellMacTm',1305), ('EBrowserObjectName_LteUserMacTm',1306), ('EBrowserObjectName_LteMacUlBasicDelayWeightQ10Table',1307), ('EBrowserObjectName_LteMacDlDelayBasedPrioQ10Table',1308), ('EBrowserObjectName_LteMacCqi2AggregationTable',1309), ('EBrowserObjectName_LteMacActivityFactorTenthTable',1310), ('EBrowserObjectName_LteCellPlmnMac',1311), ('EBrowserObjectName_LteCellTup',1401), ('EBrowserObjectName_LteAccessBearerTup',1402), ('EBrowserObjectName_LteUserTup',1403), ('EBrowserObjectName_LteS1Tup',1404), ('EBrowserObjectName_LteX2Tup',1405), ('EBrowserObjectName_LteEnbTup',1406), ('EBrowserObjectName_LteCellPlmnTup',1407), ('EBrowserObjectName_LteCellL3',1501), ('EBrowserObjectName_LteUserL3',1502), ('EBrowserObjectName_LteRadioBearerL3',1503), ('EBrowserObjectName_LteEnbL3',1504), ('EBrowserObjectName_LteEnbL3Uec',1505), ('EBrowserObjectName_LteEnbL3Enbc',1506), ('EBrowserObjectName_LteCellInfo',1601), ('EBrowserObjectName_ClientLteBr',1702), ('EBrowserObjectName_MeasurementListLteBr',1704), ('EBrowserObjectName_LteCpu',1801), ('EBrowserObjectName_LteTraceS1Enbc',1901), ('EBrowserObjectName_LteTraceX2Enbc',1902), ('EBrowserObjectName_LteTraceS1Uec',1903), ('EBrowserObjectName_LteTraceX2Uec',1904), ('EBrowserObjectName_LteTraceDlCellL2',1905), ('EBrowserObjectName_LteTraceUlCellL2',1906), ('EBrowserObjectName_LteTraceS1',1907), ('EBrowserObjectName_LteTraceX2',1908), ('EBrowserObjectName_LteTraceRrcCellc',1909), ('EBrowserObjectName_LteTraceRrcUec',1910), ('EBrowserObjectName_LteTraceRrc',1911), ('EBrowserObjectName_CombinedMeasurements',2001), ('EBrowserObjectName_IPDataRateForUL',2002), ('EBrowserObjectName_IPDataRateForDL',2003), ('EBrowserObjectName_LteCellEnbc',2101), ('EBrowserObjectName_LteCellPlmnEnbc',2102), ('EBrowserObjectName_LteCellUec',2201), ('EBrowserObjectName_LteCellAdjUec',2202), ('EBrowserObjectName_LteCellAdjUtraUec',2203), ('EBrowserObjectName_LteCellAdjGsmUec',2204), ('EBrowserObjectName_LteCellPlmnUec',2205), ('EBrowserObjectName_HrpdBandClassUec',2206), ('EBrowserObjectName_LteCellCellc',2301), ('EBrowserObjectName_LteRawData',2401), ('EBrowserObjectName_ClientDct',10001), ('EBrowserObjectName_MeasurementListDct',10002), ('EBrowserObjectName_LteMacGenCell',10003), ('EBrowserObjectName_LteMacGenUser',10004), ('EBrowserObjectName_LteMacPsCell',10005), ('EBrowserObjectName_LteMacPsUser',10006), ('EBrowserObjectName_LteCellL2',10007), ('EBrowserObjectName_LteUserL2',10008), ('EBrowserObjectName_DctDlLevL1Cell',10010), ('EBrowserObjectName_DctDlPdcpSdu',10011), ('EBrowserObjectName_DctDlsch0',10012), ('EBrowserObjectName_DctDlsch1',10013), ('EBrowserObjectName_DctDlschData0',10014), ('EBrowserObjectName_DctDlschData1',10015), ('EBrowserObjectName_DctMacPduDump',10016), ('EBrowserObjectName_DctPersistentUlschData',10017), ('EBrowserObjectName_DctPersistentDlschData',10018), ('EBrowserObjectName_DctRlcAmPdu',10019), ('EBrowserObjectName_DctRlcUmPdu',10020), ('EBrowserObjectName_DctUlLevL1Cell',10021), ('EBrowserObjectName_DctUlLevL1Ue',10022), ('EBrowserObjectName_DctUlPdpcPdu',10023), ('EBrowserObjectName_DctUlsch0',10024), ('EBrowserObjectName_DctUlsch1',10025), ('EBrowserObjectName_DctUlschData0',10026), ('EBrowserObjectName_DctUlschData1',10027), ('EBrowserObjectName_DctDlschData2',10028), ('EBrowserObjectName_DctDlRlcAmPdu',10029), ('EBrowserObjectName_DctDlRlcUmPdu',10030), ('EBrowserObjectName_DctDlMacPduDump',10031), ('EBrowserObjectName_DctUlMacPduDump',10032), ('EBrowserObjectName_DctUlRlcAmPdu',10033), ('EBrowserObjectName_DctUlRlcUmPdu',10034), ('EBrowserObjectName_DctUci',10035), ('EBrowserObjectName_DctRa',10036), ('EBrowserObjectName_DctUlsch1Tm',10037), ('EBrowserObjectName_DctDlsch1Tm',10038), ('EBrowserObjectName_DctDlschData2Tm',10039), ('EBrowserObjectName_DctUlschData1Tm',10040), ('EBrowserObjectName_DctUlschData0Tm',10041), ('EBrowserObjectName_DctUlLevL1CellTm',10042), ('EBrowserObjectName_DctDlschData3',10043), ('EBrowserObjectName_DctUlschData2',10044), ('EBrowserObjectName_DctUlschData2Tm',10045), ('EBrowserObjectName_DctDlRlcSdu',10046), ('EBrowserObjectName_LteCpuLoad',10047), ('EBrowserObjectName_LteCycleCpuLoad',10048), ('EBrowserObjectName_Last',10049)]
class ESupportedTracingFunctionalities(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ESupportedTracingFunctionalities_SubscriberTrace',0), ('ESupportedTracingFunctionalities_CellTrafficTraceReporting',1)]
class EDlMimoMode(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EDlMimoMode_SingleTx',0), ('EDlMimoMode_TxDiversity',1), ('EDlMimoMode_DualStreamMimo',2), ('EDlMimoMode_DynMimoOpenLoop',3), ('EDlMimoMode_DynMimoClosedLoop',4), ('EDlMimoMode_SingleStreamBF',5), ('EDlMimoMode_DualStreamBF',6), ('EDlMimoMode_Dyn4x2MimoClosedLoop',7), ('EDlMimoMode_TxDiversity4Ant',8), ('EDlMimoMode_Dyn8x2MimoClosedLoop',9)]
class ETimeAlignTimer(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETimeAlignTimer_NotDefined',0), ('ETimeAlignTimer_500',500), ('ETimeAlignTimer_750',750), ('ETimeAlignTimer_1280',1280), ('ETimeAlignTimer_1920',1920), ('ETimeAlignTimer_2560',2560), ('ETimeAlignTimer_5120',5120), ('ETimeAlignTimer_10240',10240)]
class EInterfaceType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EInterfaceType_AIF',0), ('EInterfaceType_S1',1), ('EInterfaceType_X2_DlFwd',2), ('EInterfaceType_X2_UlFwd',3)]
class ESectorBeamformingWeightMode(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ESectorBeamformingWeightMode_8PipeCmcc',0), ('ESectorBeamformingWeightMode_8PipeNsn',1), ('ESectorBeamformingWeightMode_2Pipe',2), ('ESectorBeamformingWeightMode_4Pipe',3)]
class EExtraFaultInfo(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EExtraFaultInfo_GlobalEnbIdDuplication',0), ('EExtraFaultInfo_PhyCellIdDuplication',1), ('EExtraFaultInfo_EnbInitiated',2), ('EExtraFaultInfo_MmeInitiated',3), ('EExtraFaultInfo_AdjEnbInitiated',4), ('EExtraFaultInfo_SetupRejectedByMme',5), ('EExtraFaultInfo_NoResponseFroMme',6), ('EExtraFaultInfo_SetupRejectedByEnb',7), ('EExtraFaultInfo_NoResponseFromAdjEnb',8), ('EExtraFaultInfo_SetupRejectedByAdjEnb',9), ('EExtraFaultInfo_NotNeeded',10), ('EExtraFaultInfo_IpAdressNotPresentInPciIpAdrMap',11), ('EExtraFaultInfo_IpAdressPresentInPciIpAdrMapX2LinkAlreadyEstablished',12), ('EExtraFaultInfo_IpAdressPresentInPciIpAdrMapSctpAssociationEstablishmentFailed',13), ('EExtraFaultInfo_TraceReferenceInUseTraceCannotBeStarted',14), ('EExtraFaultInfo_MaxNumberOfUeTraceSessionExceededTraceCannotBeStarted',15), ('EExtraFaultInfo_SubscriberAndEquipmentTraceFeatureNotEnabled',16), ('EExtraFaultInfo_TraceSessionCannotBeStartedDueToOngoingHandoverForTheUe',17), ('EExtraFaultInfo_TraceSessionCannotBeStoppedDueToOngoingHandoverForTheUe',18), ('EExtraFaultInfo_CellTraceFeatureIsNotEnabled',19), ('EExtraFaultInfo_CsgIdReceived',20)]
class EAaMemLteDspPoolCategory(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EAaMemLteDspPoolCategory_RequiredBySACK',0), ('EAaMemLteDspPoolCategory_System',2), ('EAaMemLteDspPoolCategory_Phy',2 + 1), ('EAaMemLteDspPoolCategory_Mac',2 + 2), ('EAaMemLteDspPoolCategory_Tup',2 + 3), ('EAaMemLteDspPoolCategory_Lom',2 + 4), ('EAaMemLteDspPoolCategory_Shared',2 + 5), ('EAaMemLteDspPoolCategory_NumberOf',2 + 6)]
class ESectorBeamformingMode(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ESectorBeamformingMode_Solution1',0), ('ESectorBeamformingMode_Solution2',1)]
class ESysInfoPhichResourceSize(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ESysInfoPhichResourceSize_ResourceSize1',0), ('ESysInfoPhichResourceSize_ResourceSize2',1), ('ESysInfoPhichResourceSize_ResourceSize3',2), ('ESysInfoPhichResourceSize_ResourceSize4',3)]
class EBrowserObjectIdType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EBrowserObjectIdType_Ue',0), ('EBrowserObjectIdType_Cell',1)]
class ESpatialMode(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ESpatialMode_SingleTx',0), ('ESpatialMode_TxDiversity',1), ('ESpatialMode_SpatialMultiplexing',2), ('ESpatialMode_SingleStreamBF',3), ('ESpatialMode_TM8_Port7',4), ('ESpatialMode_TM8_Port8',5), ('ESpatialMode_TM8_Port78',6), ('ESpatialMode_TM9_Port7',7), ('ESpatialMode_TM9_Port8',8), ('ESpatialMode_TM9_UpTo8LayersTx',9)]
class EOaMDlChBw(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EOaMDlChBw_Undefined',0), ('EOaMDlChBw_1Dot4MHzFdd',14), ('EOaMDlChBw_3MHzFdd',30), ('EOaMDlChBw_5MHzFdd',2), ('EOaMDlChBw_10MHz',3), ('EOaMDlChBw_15MHzFdd',4), ('EOaMDlChBw_20MHz',5)]
class EDigitalOutputType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EDigitalOutputType_BinaryHarq',0), ('EDigitalOutputType_SerialAgilent',1), ('EDigitalOutputType_SerialRs',2)]
class ESysInfoPhichDuration(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ESysInfoPhichDuration_Normal',0), ('ESysInfoPhichDuration_Extended',1)]
class EReferenceChannelNumber(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EReferenceChannelNumber_Invalid',0), ('EReferenceChannelNumber_A1_1',101), ('EReferenceChannelNumber_A1_2',102), ('EReferenceChannelNumber_A1_3',103), ('EReferenceChannelNumber_A1_4',104), ('EReferenceChannelNumber_A1_5',105), ('EReferenceChannelNumber_A2_1',201), ('EReferenceChannelNumber_A2_2',202), ('EReferenceChannelNumber_A2_3',203), ('EReferenceChannelNumber_A3_1',301), ('EReferenceChannelNumber_A3_2',302), ('EReferenceChannelNumber_A3_3',303), ('EReferenceChannelNumber_A3_4',304), ('EReferenceChannelNumber_A3_5',305), ('EReferenceChannelNumber_A3_6',306), ('EReferenceChannelNumber_A3_7',307), ('EReferenceChannelNumber_A4_1',401), ('EReferenceChannelNumber_A4_2',402), ('EReferenceChannelNumber_A4_3',403), ('EReferenceChannelNumber_A4_4',404), ('EReferenceChannelNumber_A4_5',405), ('EReferenceChannelNumber_A4_6',406), ('EReferenceChannelNumber_A4_7',407), ('EReferenceChannelNumber_A4_8',408), ('EReferenceChannelNumber_A5_1',501), ('EReferenceChannelNumber_A5_2',502), ('EReferenceChannelNumber_A5_3',503), ('EReferenceChannelNumber_A5_4',504), ('EReferenceChannelNumber_A5_5',505), ('EReferenceChannelNumber_A5_6',506), ('EReferenceChannelNumber_A5_7',507), ('EReferenceChannelNumber_A7_1',701), ('EReferenceChannelNumber_A7_2',702), ('EReferenceChannelNumber_A7_3',703), ('EReferenceChannelNumber_A7_4',704), ('EReferenceChannelNumber_A7_5',705), ('EReferenceChannelNumber_A7_6',706), ('EReferenceChannelNumber_A8_1',801), ('EReferenceChannelNumber_A8_2',802), ('EReferenceChannelNumber_A8_3',803), ('EReferenceChannelNumber_A8_4',804), ('EReferenceChannelNumber_A8_5',805), ('EReferenceChannelNumber_A8_6',806), ('EReferenceChannelNumber_DCM_1',1001), ('EReferenceChannelNumber_DCM_2',1002), ('EReferenceChannelNumber_DCM_3',1003), ('EReferenceChannelNumber_DCM_4',1004), ('EReferenceChannelNumber_DCM_5',1005), ('EReferenceChannelNumber_DCM_6',1006), ('EReferenceChannelNumber_DCM_7',1007), ('EReferenceChannelNumber_DCM_8',1008)]
class EDataForwarding(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EDataForwarding_NoForwarding',0), ('EDataForwarding_DlForwarding',1), ('EDataForwarding_UlForwarding',2), ('EDataForwarding_DlUlForwarding',3)]
class EFaultLocationType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EFaultLocationType_NoLocation',0), ('EFaultLocationType_SICAD',1), ('EFaultLocationType_UnitAddr',2), ('EFaultLocationType_CellId',3), ('EFaultLocationType_LcrId',4), ('EFaultLocationType_LcgId',5), ('EFaultLocationType_UserId',6), ('EFaultLocationType_LinkId',7), ('EFaultLocationType_Other',8), ('EFaultLocationType_LnAdjId',9), ('EFaultLocationType_LnMmeId',10), ('EFaultLocationType_SCTP',11), ('EFaultLocationType_LNBTS',12), ('EFaultLocationType_LnAdjgId',13)]
class EL3SignallingType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EL3SignallingType_Common',0), ('EL3SignallingType_Dedicated',1)]
class EUlCombinationMode(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EUlCombinationMode_MRC',0), ('EUlCombinationMode_IRC',1)]
class EDigitalOutputBBSelector(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EDigitalOutputBBSelector_00',0), ('EDigitalOutputBBSelector_01',1), ('EDigitalOutputBBSelector_10',2), ('EDigitalOutputBBSelector_11',3)]
class ECellOperationalState(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ECellOperationalState_disabled',0), ('ECellOperationalState_enabled',1)]
class ELinkType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ELinkType_S1',0), ('ELinkType_X2',1)]
class EHandoverType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EHandoverType_NoHandover',0), ('EHandoverType_IntraFspx',1), ('EHandoverType_InterFspx',2), ('EHandoverType_InterFtmFsm',3), ('EHandoverType_InterEnb',4), ('EHandoverType_IntraCell',5), ('EHandoverType_InterRatToLte',6), ('EHandoverType_InterRatToWcdma',7), ('EHandoverType_IntraCellReestablishment',8), ('EHandoverType_IntraFspxReestablishment',9), ('EHandoverType_InterFspxReestablishment',10), ('EHandoverType_IntraEnbSourceIntraCellReestablishmentWithHO',11), ('EHandoverType_IntraEnbSourceIntraFspxReestablishmentWithHO',12), ('EHandoverType_IntraEnbSourceInterFspxReestablishmentWithHO',13), ('EHandoverType_InterEnbX2SourceIntraCellReestablishmentWithHO',14), ('EHandoverType_InterEnbX2SourceIntraFspxReestablishmentWithHO',15), ('EHandoverType_InterEnbX2SourceInterFspxReestablishmentWithHO',16), ('EHandoverType_InterRatToWcdmaIntraCellReestablishmentWithHO',17), ('EHandoverType_InterRatToWcdmaIntraFspxReestablishmentWithHO',18), ('EHandoverType_InterRatToWcdmaInterFspxReestablishmentWithHO',19), ('EHandoverType_IntraEnbTargetIntraCellReestablishmentWithHO',20), ('EHandoverType_IntraEnbTargetIntraFspxReestablishmentWithHO',21), ('EHandoverType_IntraEnbTargetInterFspxReestablishmentWithHO',22), ('EHandoverType_InterEnbX2TargetIntraCellReestablishmentWithHO',23), ('EHandoverType_InterEnbX2TargetIntraFspxReestablishmentWithHO',24), ('EHandoverType_InterEnbX2TargetInterFspxReestablishmentWithHO',25), ('EHandoverType_InterRatToLteIntraCellReestablishmentWithHO',26), ('EHandoverType_InterRatToLteIntraFspxReestablishmentWithHO',27), ('EHandoverType_InterRatToLteInterFspxReestablishmentWithHO',28)]
class EDirection(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EDirection_Dl',0), ('EDirection_Ul',1), ('EDirection_Dl_Ul',2)]
class ETechnology(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETechnology_Fdd',0), ('ETechnology_Tdd',1)]
class ETestModelId(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETestModelId_Invalid',0), ('ETestModelId_E_TM1_1',101), ('ETestModelId_E_TM1_2',102), ('ETestModelId_E_TM2',200), ('ETestModelId_E_TM3_1',301), ('ETestModelId_E_TM3_2',302), ('ETestModelId_E_TM3_3',303), ('ETestModelId_MIMO_TM3_1',1000)]
class EHsTrainScenario(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EHsTrainScenario_NotApplied',0), ('EHsTrainScenario_1',1), ('EHsTrainScenario_3',2)]
class EDigitalOutputBitRate(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EDigitalOutputBitRate_115Dot2Kbps',0), ('EDigitalOutputBitRate_460Dot8Kbps',1), ('EDigitalOutputBitRate_1Dot92Mbps',2)]
class EDeploymentInfo(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EDeploymentInfo_NotUsed',0), ('EDeploymentInfo_TDD_2_pipe',1), ('EDeploymentInfo_TDD_4_pipe',2), ('EDeploymentInfo_TDD_8_pipe',3), ('EDeploymentInfo_FDD_2DspPool',4), ('EDeploymentInfo_FDD_3DspPool',5), ('EDeploymentInfo_FDD_4DspPool',6), ('EDeploymentInfo_TDD_2DspPool',7), ('EDeploymentInfo_TDD_3DspPool',8), ('EDeploymentInfo_TDD_4DspPool',9), ('EDeploymentInfo_TDD_5DspPool',10), ('EDeploymentInfo_FZM_FDD_8Core',11), ('EDeploymentInfo_TDD_3DspPool_8Pipe',12), ('EDeploymentInfo_FDD_4DspPool_Part1',13), ('EDeploymentInfo_FDD_4DspPool_Part2',14), ('EDeploymentInfo_FDD_4DspPool_2DspPool',15), ('EDeploymentInfo_FZM_TDD_8Core',16)]
class EAaMemLteDspPoolIdShared(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EAaMemLteDspPoolIdShared_FirstMemberSackRequirement',0), ('EAaMemLteDspPoolIdShared_PhyDataUplink',2)]
class EL3LinkDirection(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EL3LinkDirection_Incoming',0), ('EL3LinkDirection_Outgoing',1)]
class ESpecificCauseLte(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ESpecificCauseLte_NotDefined',0), ('ESpecificCauseLte_TUP_Unspecified',1), ('ESpecificCauseLte_TUP_AlreadyActivated_Allocated',2), ('ESpecificCauseLte_TUP_ParameterOutOfRange',3), ('ESpecificCauseLte_TUP_ResourceUnavailable_Unspecified',4), ('ESpecificCauseLte_TUP_ResourceUnavailable',5), ('ESpecificCauseLte_TUP_NotEnoughResources',6), ('ESpecificCauseLte_TUP_UnsuccessfulTransmission',7), ('ESpecificCauseLte_TUP_OutOfMemory',8), ('ESpecificCauseLte_TUP_LinkUnavailable',9), ('ESpecificCauseLte_TUP_ConnectionUnavailable',10), ('ESpecificCauseLte_TUP_LinkAlreadyActivated_Allocated',11), ('ESpecificCauseLte_TUP_ConnectionAlreadyActivated_Allocated',12), ('ESpecificCauseLte_TUP_ResourceInUse',13), ('ESpecificCauseLte_TUP_UeConfigurationError',14), ('ESpecificCauseLte_TUP_BearerConfigurationError',15), ('ESpecificCauseLte_TUP_MaximumNumberOfUesExceeded',16), ('ESpecificCauseLte_MAC_Unspecified',1000), ('ESpecificCauseLte_MAC_AlreadyActivated_Allocated',1001), ('ESpecificCauseLte_MAC_InvalidParameter',1002), ('ESpecificCauseLte_MAC_ResourceUnavailable',1003), ('ESpecificCauseLte_MAC_OutOfMemory',1004), ('ESpecificCauseLte_MAC_NoAnswerFromMacSubSys',1005), ('ESpecificCauseLte_MAC_NoAnswerFromPhy',1006), ('ESpecificCauseLte_MAC_ObjectDoesNotExist',1007), ('ESpecificCauseLte_MAC_ErrorInObjectCreation',1008), ('ESpecificCauseLte_MAC_BearerConfigurationError',1009), ('ESpecificCauseLte_MAC_UeConfigurationError',1010), ('ESpecificCauseLte_MAC_NoConfigurationMessage',1011), ('ESpecificCauseLte_MAC_ErrorInObjectDeletion',1012), ('ESpecificCauseLte_MAC_TooHighBbUsageRatio',1013), ('ESpecificCauseLte_MAC_GBRCongestionOnPDCCHDL',1014), ('ESpecificCauseLte_MAC_GBRCongestionOnPDCCHUL',1015), ('ESpecificCauseLte_MAC_GBRCongestionOnPDCCH',1016), ('ESpecificCauseLte_MAC_GBRCongestionOnPUSCH',1017), ('ESpecificCauseLte_MAC_GBRCongestionOnPDSCH',1018), ('ESpecificCauseLte_MAC_GBRCongestionSolvingCompleted',1019), ('ESpecificCauseLte_MAC_GBRCongestionSolvingPartlyCompleted',1020), ('ESpecificCauseLte_MAC_GBRCongestionSolvingIntentionallyIgnored',1021), ('ESpecificCauseLte_MAC_GBRCongestionSolvingUnintentionallyNotHandled',1022), ('ESpecificCauseLte_MAC_LackOfUlResources',1023), ('ESpecificCauseLte_MAC_MaximumNumberOfUesExceeded',1024), ('ESpecificCauseLte_MAC_CrntiNotFree',1025), ('ESpecificCauseLte_MAC_SCellDoesNotExist',1026), ('ESpecificCauseLte_MAC_SCellReconfigrationFailed',1027), ('ESpecificCauseLte_UEC_Unspecified',2000), ('ESpecificCauseLte_UEC_CellSetup',2001), ('ESpecificCauseLte_UEC_NoCellcUecRegistrationRespReceived',2002), ('ESpecificCauseLte_UEC_NetworkConfiguration',2010), ('ESpecificCauseLte_UEC_ReleaseUe_S1Reset',2020), ('ESpecificCauseLte_UEC_ReleaseUe_SctpLinkError',2021), ('ESpecificCauseLte_UEC_ReleaseUe_GtpuError',2022), ('ESpecificCauseLte_UEC_UnknownCellId',2023), ('ESpecificCauseLte_UEC_ResourceInconsistency',2024), ('ESpecificCauseLte_CELLC_Unspecified',3000), ('ESpecificCauseLte_CELLC_CellIdAlreadyKnown',3001), ('ESpecificCauseLte_CELLC_MacSysInfoActivationFailed',3002), ('ESpecificCauseLte_CELLC_OMParameterOutOfRange',3003), ('ESpecificCauseLte_CELLC_StateChangeToDisableNotSupported',3004), ('ESpecificCauseLte_CELLC_MaxNumOfSupportedCellsReached',3005), ('ESpecificCauseLte_CELLC_InvalidParameterValue',3006), ('ESpecificCauseLte_CELLC_MacSysInfoConfigurationFailed',3007), ('ESpecificCauseLte_CELLC_MessageReceivedInWrongState',3008), ('ESpecificCauseLte_CELLC_SrsConfigurationParameterConsistencyCheckFailure',3009), ('ESpecificCauseLte_CELLC_PhyUlResourceInfoFailure',3010), ('ESpecificCauseLte_CELLC_MacBcchModIndFailed',3011), ('ESpecificCauseLte_CELLC_MacMeasurementInitiationFailed',3012), ('ESpecificCauseLte_CELLC_OaMParameterForCarrierAggregationForSubfeatureAOutOfRange',3013), ('ESpecificCauseLte_CELLC_OaMParameterPrachConfigIndexNotSupported',3014), ('ESpecificCauseLte_CELLC_RrmNoFreeResources',3100), ('ESpecificCauseLte_CELLC_RrmAmbrOutsideRange',3101), ('ESpecificCauseLte_CELLC_RrmUeIdNotKnown',3102), ('ESpecificCauseLte_CELLC_RrmWrongCallReason',3103), ('ESpecificCauseLte_CELLC_Rrm_InvalidOperationalState',3104), ('ESpecificCauseLte_CELLC_Rrm_MandatoryParameterMissing',3105), ('ESpecificCauseLte_CELLC_Rrm_UeIdAlreadyKnown',3106), ('ESpecificCauseLte_CELLC_Rrm_MaxNumberOfDrbsPerUeReached',3107), ('ESpecificCauseLte_CELLC_Rrm_InvalidDrxCycleLengthCqiPerNpRelation',3108), ('ESpecificCauseLte_CELLC_RrmUeHasPreemptedBearer',3109), ('ESpecificCauseLte_CELLC_SCellNotFound',3110), ('ESpecificCauseLte_CELLC_NoHarqResourcesLeftForSCellConfiguration',3111), ('ESpecificCauseLte_CELLC_Generic_UnexpectedInternalSwError',3200), ('ESpecificCauseLte_CELLC_Generic_CellIdUnknown',3201), ('ESpecificCauseLte_ENBC_Unspecified',4000), ('ESpecificCauseLte_ENBC_UEID_TEID_AllocationBlocked',4001), ('ESpecificCauseLte_ENBC_TEID_AllocationBlocked',4002), ('ESpecificCauseLte_ENBC_UnknownCellID',4003), ('ESpecificCauseLte_ENBC_UnknownLinkID',4006), ('ESpecificCauseLte_ENBC_UnknownTAI',4007), ('ESpecificCauseLte_ENBC_LinkDeactivationOngoing',4008), ('ESpecificCauseLte_ENBC_MmeCodeMismatch',4009), ('ESpecificCauseLte_ENBC_PlmnIdMismatch',4010), ('ESpecificCauseLte_ENBC_TUP_RegistrationFailed',4016), ('ESpecificCauseLte_ENBC_MmeOverloaded',4017), ('ESpecificCauseLte_ENBC_InvalidMmeGroupID',4018), ('ESpecificCauseLte_RROM_Unspecified',5000), ('ESpecificCauseLte_RROM_InternalError',5001), ('ESpecificCauseLte_RROM_OutOfMemory',5002), ('ESpecificCauseLte_RROM_UnexpectedMessage',5003), ('ESpecificCauseLte_RROM_MandatoryParameterMissing',5004), ('ESpecificCauseLte_RROM_ParameterOutOfRange',5005), ('ESpecificCauseLte_RROM_InvalidMessageLength',5006), ('ESpecificCauseLte_RROM_Registration',5100), ('ESpecificCauseLte_RROM_IndicationTypeEmpty',5101), ('ESpecificCauseLte_RROM_HwConfigurationData',5110), ('ESpecificCauseLte_RROM_HwMapping',5111), ('ESpecificCauseLte_RROM_InternalAddressDistributionFailed',5120), ('ESpecificCauseLte_RROM_PHYStartRefSyncS',5220), ('ESpecificCauseLte_RROM_CELLCCellStateChange',5221), ('ESpecificCauseLte_RROM_UnknownLcrId',5222), ('ESpecificCauseLte_RROM_CellSetupFailure',5250), ('ESpecificCauseLte_RROM_CellDeletionFailure',5251), ('ESpecificCauseLte_RROM_RegistrationFailure',5252), ('ESpecificCauseLte_RROM_NotInTestDedicatedState',5300), ('ESpecificCauseLte_RROM_OvenOscillatorNotWarmedUp',5301), ('ESpecificCauseLte_RROM_Start3GPPTestModelFailure',5303), ('ESpecificCauseLte_RROM_Stop3GPPTestModelFailure',5304), ('ESpecificCauseLte_RROM_Conflicting3GPPTestModelRunning',5305), ('ESpecificCauseLte_RROM_No3GPPTestModelRunning',5306), ('ESpecificCauseLte_RROM_3GPPTestModelParameterMismatch',5307), ('ESpecificCauseLte_RROM_CellOperationalStateDisabled',5310), ('ESpecificCauseLte_RROM_X2LinkBlacklisted',5320), ('ESpecificCauseLte_RROM_AdjCellConfigurationInconsistency',5321), ('ESpecificCauseLte_RROM_AntennaCarrierCalibrationSetupFailureAtBTSOM',5330), ('ESpecificCauseLte_RROM_TrswConfigurationData',5340), ('ESpecificCauseLte_RROM_MobilitySettingsChangeData',5341), ('ESpecificCauseLte_SMC_Unspecified',6000), ('ESpecificCauseLte_SMC_UnexpectedMessage',6001), ('ESpecificCauseLte_SMC_InvalidBoardId',6002), ('ESpecificCauseLte_SMC_InvalidMessageLength',6003), ('ESpecificCauseLte_SMC_InternalAddressDistributionFailed',6100), ('ESpecificCauseLte_SMC_TupNetworkConfigFailed',6104), ('ESpecificCauseLte_PHY_Unspecified',7000), ('ESpecificCauseLte_PHY_UnknownCellId',7001), ('ESpecificCauseLte_PHY_CellIdAlreadyInUse',7002), ('ESpecificCauseLte_PHY_InvalidParam',7003), ('ESpecificCauseLte_PHY_NotEnoughResources',7004), ('ESpecificCauseLte_PHY_OutOfMemory',7005), ('ESpecificCauseLte_PHY_InternalAddrReqNotReceived',7006), ('ESpecificCauseLte_PHY_LteTimerNotRunning',7007), ('ESpecificCauseLte_PHY_AifFailure',7008), ('ESpecificCauseLte_PHY_UnexpectedMessage',7009), ('ESpecificCauseLte_PHY_PrachNotInitialized',7100), ('ESpecificCauseLte_PHY_PrachAlreadyInUse',7101), ('ESpecificCauseLte_PHY_TestmodelUnsupportedCellConfig',7202), ('ESpecificCauseLte_PHY_TestloopUnsupportedCellConfig',7203), ('ESpecificCauseLte_PHY_DeploymentNotSupported',7300), ('ESpecificCauseLte_PHY_DlPhyChanAlreadyInUse',7400), ('ESpecificCauseLte_PHY_DeadlineMissed',7500), ('ESpecificCauseLte_Unspecified',8001), ('ESpecificCauseLte_SWError',8002), ('ESpecificCauseLte_InvalidParameter',8003), ('ESpecificCauseLte_ParameterOutOfRange',8004), ('ESpecificCauseLte_OutOfMemory',8005), ('ESpecificCauseLte_ResourceUnavailable',8006), ('ESpecificCauseLte_NotEnoughResources',8007), ('ESpecificCauseLte_AlreadyActivatedAllocated',8008), ('ESpecificCauseLte_MessageReceivedInWrongState',8009), ('ESpecificCauseLte_InvalidMessageLength',8010), ('ESpecificCauseLte_AbnormalRelease',8011), ('ESpecificCauseLte_S1APIdErrorInIncomingRequestBeforeL3ConnSetup',8012)]

class SMessageResult(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('status',EStatusLte), ('cause',ECauseLte), ('specificCause',ESpecificCauseLte)]
class SPlmnId(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('mncLength',TMncLength), ('mnc',TMnc), ('mcc',TMcc)]
class SGummei(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('PlmnIdentity',SPlmnId), ('mmeGroupId',TMmeGroupId), ('mmeCode',TMmeCode)]
class SSTMsi(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('mTMsi',TMTMsi), ('mmeCode',TMmeCode)]
class STransportLayerAddress(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('addressLength',TNumberOfItems), ('address',prophy.array(u8,bound='addressLength'))]
class SGcadAddress(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('eqid',TEqId), ('ccid',TCcId)]
class SResultCounters(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numberOfReceivedBits',TCounterLte), ('numberOfDefectiveBits',TCounterLte), ('numberOfReceivedTransmissionBlocks',TCounterLte), ('numberOfUnreceivedTransmissionBlocks',TCounterLte)]
class SUlCtrlChannelMeasCounters(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('detectedCounter',TCounterCtrlLte), ('missedCounter',TCounterCtrlLte), ('falseCounter',TCounterCtrlLte), ('idlePeriodCounter',TCounterCtrlLte)]
class SUlCtrlChannelMeasCountersMissedPrach(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('noPaCounter',TCounterCtrlLte), ('wrongPaCounter',TCounterCtrlLte), ('wrongTimingCounter',TCounterCtrlLte)]
class SUlCtrlChannelPrachParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('prachConfIndex',TPrachConfIndex), ('preambleIndex',prophy.u32), ('acceptedTimingError',prophy.u32), ('constantOffset',prophy.u32), ('delayPatternSingleStepDuration',prophy.u32)]
class SUlCtrlChannelPucchAckParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('pucchResourceIndexAn',TPucchResourceIndex), ('pucchResourceIndexSecond',TPucchResourceIndex), ('pucchResourceIndexThird',TPucchResourceIndex), ('pucchResourceIndexFourth',TPucchResourceIndex)]
class SUlCtrlChannelPucchCqiParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('pucchResourceIndexCqi',TResourceIndexCqi), ('pucchResourceIndexSecond',TResourceIndexCqi), ('pucchResourceIndexThird',TResourceIndexCqi), ('pucchResourceIndexFourth',TResourceIndexCqi)]
class SUlCtrlChannelPuschHarqAckParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('referenceChannelNumber',EReferenceChannelNumber), ('resourceBlockOffset',TResourceBlock)]
class SUlTestModelsDigitalOutputParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('digitalOutputType',EDigitalOutputType), ('bitRate',EDigitalOutputBitRate), ('bBSelector',EDigitalOutputBBSelector)]
class SPucchConfiguration(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('deltaPucchShift',TDeltaPucchShift), ('pucchNAnCs',TPucchNAnCs), ('nCqiRb',TNCqiRb), ('n1PucchAn',TN1PucchAn)]
class SPuschControlOffsets(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('puschAckOffI',TPuschControlOffsetIndex), ('puschRiOffI',TPuschControlOffsetIndex), ('puschCqiOffI',TPuschControlOffsetIndex)]
class SCalibrationSets(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('calRxTxFlag',prophy.u32), ('calFrameOffset',prophy.u32), ('halfFrameIndication',prophy.u32), ('antennaBitMap',prophy.u32)]
class SS1SignallingConnectivityInfoOfAdjEnb(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tmpName',TNumberOfItems), ('s1LinkId',prophy.array(TL3LinkId,bound='tmpName'))]
class SCandUPlaneIpAddresses(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('transportNetworkId',TTransportNetworkId), ('cPlaneIpAddress',STransportLayerAddress), ('uPlaneIpAddress',STransportLayerAddress)]
class SSectorBfWeightforAntenna(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('bfWeigthImag',prophy.i16), ('bfWeightReal',prophy.i16)]
class SPdschResources(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numPrbs',TNumPrbs), ('prbMap0',prophy.bytes(size=MAX_NUM_PRBS_DIV32)), ('prbMap1',prophy.bytes(size=MAX_NUM_PRBS_DIV32))]
class SDlBfTbFormat(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('bfWeight',prophy.bytes(size=4)), ('stBFWeight',TStBFWeightPointer), ('nSCID',prophy.u16), ('cbiValidity',prophy.u16), ('numMuPrbs',TNumPrbs), ('muPrbMapSlot0',prophy.bytes(size=MAX_NUM_PRBS_DIV32)), ('muPrbMapSlot1',prophy.bytes(size=MAX_NUM_PRBS_DIV32))]
class SDlTbFormat(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('modulation',EModulation), ('redundancyVersion',TRedundancyVersion), ('spatialMode',ESpatialMode), ('numOfLayers',TNumOfLayers), ('codebookIndex',TCodebookIndex), ('codeWordIndex',TCodeWordIndex), ('nIr',TNIr)]
class STxAntennaMapping(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('txAntIndex',prophy.u32), ('subCellId',prophy.u32)]
class SRxAntennaMapping(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('rxAntIndex',prophy.u32), ('subCellId',prophy.u32)]
class SMeasReportValue(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('status',EStatusLte), ('measurementValue',TMeasurementValue)]
class SRaPreambleList(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('RAPreamble',TRaPreamble)]
class SRaPreambleResList(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('RAPreamble',TRaPreamble), ('crnti',TCrnti), ('status',EStatusLte)]
class SL2DeploymentInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('l2NodeType',EL2DeployableNode), ('nodeAddr',TAaSysComNid)]
class SL2PoolInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('poolId',TPoolId), ('numOfDeploymentInfo',TNumberOfItems), ('deploymentInfo',prophy.array(SL2DeploymentInfo,bound='numOfDeploymentInfo'))]
