import prophy 
from externals import *
from globals import *


MAX_COVARIANCE_MATRIX_ELEMENT = 16
MAX_NUM_SUBCELL_PER_SUBPOOL = 6
MAX_NUM_SUBPOOLS = 2
PHY_INVALID_VALUE_U8 = 0xFF
MAX_NUM_SCELLS = 1
MAX_NUM_OF_SRS_RECEIVE_REQ_TDD = 67
MAX_NUM_OF_MAC_TO_PHY_EVENTS = 8
MAX_PUCCH_SR_UES_PER_TTI_TDD = 100
MAX_PUCCH_CQI_UES_PER_TTI_TDD = 50
MAX_NUM_OF_PUCCH_RECEIVE_REQ_TDD = 230
MAX_ACKNACK_UES_PER_TTI_TDD = 80
MAX_SRS_UE_LIMIT = 384
MAX_SR_CQI_UE_LIMIT = 200
COMMON_POOL_SR_CQI_SIZE_LOW = 84
COMMON_POOL_SR_CQI_SIZE = 120
RESET_RI_TABLE = 0xFF
PHY_INVALID_VALUE = 0xFFFF
MAX_UES_IN_PUSCH_RESPU = 8
FIRST_PRB_NOT_VALID = 250
MAX_NUM_SRS_CELL_MEAS_COUNT = 100
MAX_ACKNACK_UES_PER_TTI_LOW = 25
MAX_ACKNACK_UES_PER_TTI = 25
MAX_PUCCH_SR_UES_PER_TTI_LOW = 42
MAX_PUCCH_SR_UES_PER_TTI = 60
MAX_PUCCH_CQI_UES_PER_TTI_LOW = 42
MAX_PUCCH_CQI_UES_PER_TTI = 60
MAX_PUSCH_UES_PER_TTI_20MHZ = 32
MAX_PUSCH_UES_PER_TTI_15MHZ = 32
MAX_PUSCH_UES_PER_TTI_10MHZ = 32
MAX_PUSCH_UES_PER_TTI_5MHZ = 16
FREQUENCY_OFFSET_NOT_VALID = 0x80000000
ELAPSED_TIME_NOT_VALID = 0
MAX_ELAPSED_TIME_IN_SUBFRAMES = 65000
MAX_NUM_PUCCH_CELL_MEAS_COUNT = 44
MAX_NUM_OF_BUNDLED_DL_SUBFRAMES = 9
NUM_OF_RESOURCE_CONFIGURATIONS = 10
MAX_TOTAL_CYCLES = 50000
MAX_PROCESSING_LOAD = 5000
PUSCH_CQI_BIT_TABLE_SIZE = 3
NUM_OF_TOTAL_RX_POWERS = 8
NUM_OF_RX_SCALING_VALUES = 8
NUM_OF_RX_ANTENNAS = 2
MAX_UL_TEST_MODEL_USERS = 2
NUM_OF_PUCH_PRB_COUNT_20MHZ = 100
NUM_OF_PUCH_PRB_COUNT_10MHZ = 50
NUM_OF_PUCH_PRB_COUNT_1_4MHZ = 6
MAX_NUM_OF_SRS_MEASUREMENTS_PER_SUBFRAME_TDD = 192
MAX_NUM_OF_SRS_MEASUREMENTS_PER_SUBFRAME = 240
MAX_NUM_OF_SRS_MEASUREMENTS_PER_UE = 24
MAX_NUM_OF_SRS_RECEIVE_REQ = 120
MAX_NUM_OF_PUSCH_RECEIVE_REQ = 20
MAX_NUM_OF_PUCCH_RECEIVE_REQ_LOW = 109
MAX_NUM_OF_PUCCH_RECEIVE_REQ = 160
MAX_NUM_OF_PRACH_PREAMBLES = 64
MAX_RECEIVE_REQ_MSG_SIZE = 4096
THIS_IS_VARIABLE_SIZE_ARRAY = 1
NUM_OF_BEAMS = 4
MAX_ST_BF_WEIGHT_START_PRB = 96
MIN_ST_BF_WEIGHT_START_PRB = 0
MAX_ST_BF_WEIGHT_BAND_WIDTH = 96
MIN_ST_BF_WEIGHT_BAND_WIDTH = 4
MAX_NUM_CTRL_SYMBOLS = 4
MAX_NUM_OF_BITS_IN_PBCH_DIV8 = 8
MAX_NUM_OF_BITS_IN_PDCCH_DIV8 = 8
MAX_NUM_OF_PHICH_INFO = 24
MAX_NUM_OF_DCI_INFO = 88
VARIABLE_SIZE_ARRAY = 1
MAX_UE_BLER_TRIGGER_SUBFRM_INTERVAL = 9
MAX_UE_BLER_TRIGGER = 64
SRS_COMBINE_ANTENNA_NUMBER = 8
SRS_MAX_PRB = 100
MAX_NUM_OF_L1DEPLOYABLE_NODE = 16
MAX_NUM_OF_DEPLOYMENT_INFO = 30

TNumPrbsU8 = prophy.u8
TTbPointer = prophy.u32
TUnitNid = prophy.u32
TNumberOfItemsU8 = prophy.u8
TTbSizeU8 = prophy.u8
TNumOfCce = prophy.u8
TCceStartIndex = prophy.u8
TPhyMsgPointer = prophy.u32
TPhichGroupIndex = prophy.u8
THarqAckIndicatorAndPhichIndex = prophy.u8
TNumOfTtis = prophy.u32
TFreqShift1TxIn2Tx = prophy.u32
TPbIndex = prophy.u32
TDlInterferenceLevel = prophy.u32
TPwrReduction = prophy.u32
TStepDuration = prophy.u32
TShutdownStepAmnt = prophy.u32
TTxPowerI16 = prophy.i16
TPrsConfigurationIndex = prophy.u32
TPrsNumDlFrames = prophy.u32
TPrsMutingInfoPatternLength = prophy.u32
TUpdatePeriod = prophy.u32
TUeIdI16 = prophy.i16
TSrsCyclicShift = prophy.u32
TSrsCyclicShiftU8 = prophy.u8
TDlHarqAckBits = prophy.u32
TDlHarqAckBitsU8 = prophy.u8
TFrequencyError = prophy.i32
TCqiBits = prophy.u32
TCqiSize = prophy.u32
TCqiSizeU8 = prophy.u8
TInterferencePower = prophy.r32
TNoiseVariance = prophy.r32
TPrachIndex = prophy.u32
TPrachCyclicShift = prophy.u32
TPrachPreambleFormat = prophy.u32
TPrachPreambleTiming = prophy.u32
TPrachRootSeqIndex = prophy.u32
TPrbNumber = prophy.u32
TPreambleFra = prophy.u32
TPrbNumberU8 = prophy.u8
TPucchResourceIndexAn = prophy.u32
TPucchResourceIndexCqi = prophy.u32
TPucchResourceIndexSr = prophy.u32
TProcessingLoad = prophy.u32
TUlRefSigDeltaSeqShift = prophy.u32
TUlRefSigParamNdmrs = prophy.u32
TRiData = prophy.u32
TRiDataU8 = prophy.u8
TRiSize = prophy.u32
TRiSizeU8 = prophy.u8
TRssi = prophy.r32
TSignalPower = prophy.r32
TSinr = prophy.u32
TTimeOffsetEst = prophy.i32
TTimeOffsetEstWeight = prophy.u32
TTimeEstPhi = prophy.i32
TTotalPower = prophy.r32
TFrequencyOffset = prophy.u32
TSubCarrierIndex = prophy.u32
TElapsedTime = prophy.u16
TDlHarqProcessInfoPacked = prophy.u8
TNumOfCodeBlocks = prophy.u8
TEBundlingModeU8 = prophy.u8
TERiQualityResultU8 = prophy.u8
TECqiQualityResultU8 = prophy.u8
TECqiRepTypeU8 = prophy.u8
TECrcResultU8 = prophy.u8
TESrResultU8 = prophy.u8
TEDlHarqAckResultU8 = prophy.u8
TEDlHarqAckTypeU8 = prophy.u8
TEPucchFormatU8 = prophy.u8
TEUlSyncQualityResultU8 = prophy.u8
TESrsQualityResultU8 = prophy.u8
TTransCombU8 = prophy.u8
TPayloadOffsetU8 = prophy.u8
TEMacToPhyEventU8 = prophy.u8
TEMacToPhyEventTypeU8 = prophy.u8
TPucchResourceIndex16 = prophy.u16
TCoMpSinrThreshold = prophy.i32
TSubCellIdU8 = prophy.u8
TMimoLayer = prophy.u16

class EPhyDeployableNode(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EPhyDeployableNode_Basic1',0), ('EPhyDeployableNode_Basic2',1), ('EPhyDeployableNode_Basic3',2), ('EPhyDeployableNode_Basic4',3), ('EPhyDeployableNode_Extended1',10), ('EPhyDeployableNode_Extended2',11), ('EPhyDeployableNode_Extended3',12), ('EPhyDeployableNode_Extended4',13), ('EPhyDeployableNode_Extended5',14), ('EPhyDeployableNode_Extended6',15), ('EPhyDeployableNode_Extended7',16), ('EPhyDeployableNode_Extended8',17), ('EPhyDeployableNode_Tdd8Pipe1',20), ('EPhyDeployableNode_Tdd8Pipe2',21), ('EPhyDeployableNode_Tdd8Pipe3',22), ('EPhyDeployableNode_Tdd8Pipe4',23), ('EPhyDeployableNode_Tdd8Pipe5',24), ('EPhyDeployableNode_Tdd8Pipe6',25), ('EPhyDeployableNode_Tdd8Pipe7',26), ('EPhyDeployableNode_Tdd8Pipe8',27), ('EPhyDeployableNode_Tdd8Pipe9',28), ('EPhyDeployableNode_Tdd8Pipe10',29), ('EPhyDeployableNode_Tdd8Pipe11',30), ('EPhyDeployableNode_Tdd8Pipe12',31), ('EPhyDeployableNode_TddSuperCell1',40), ('EPhyDeployableNode_TddSuperCell2',41), ('EPhyDeployableNode_TddSuperCell3',42), ('EPhyDeployableNode_TddSuperCell4',43), ('EPhyDeployableNode_TddSuperCell5',44), ('EPhyDeployableNode_TddSuperCell6',45), ('EPhyDeployableNode_TddSuperCell7',46), ('EPhyDeployableNode_TddSuperCell8',47), ('EPhyDeployableNode_TddSuperCell9',48), ('EPhyDeployableNode_TddSuperCell10',49), ('EPhyDeployableNode_TddSuperCell11',50), ('EPhyDeployableNode_TddSuperCell12',51), ('EPhyDeployableNode_TddSuperCell13',52), ('EPhyDeployableNode_TddSuperCell14',53), ('EPhyDeployableNode_TddSuperCell15',54), ('EPhyDeployableNode_TddSuperCell16',55), ('EPhyDeployableNode_Internal',56)]
class ECrcResult(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ECrcResult_Fail',0), ('ECrcResult_Pass',1), ('ECrcResult_NotAttempted',2), ('ECrcResult_TransmissionUnreliable',3), ('ECrcResult_InvalidParam',100), ('ECrcResult_NotEnoughResources',101), ('ECrcResult_DeadlineMissed',102)]
class EInterferenceSM(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EInterferenceSM_SingleTx',0), ('EInterferenceSM_TxDiversity',1), ('EInterferenceSM_SingleStreamBF',2)]
class EBundlingMode(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EBundlingMode_NoBundling',0), ('EBundlingMode_NormalTti',1), ('EBundlingMode_FinalTti',2)]
class EPhichDur(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EPhichDur_Normal',0), ('EPhichDur_Extended',1)]
class EResourceConfiguration(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EResourceConfiguration_1x5MHz',0), ('EResourceConfiguration_2x5MHz',1), ('EResourceConfiguration_1x10MHz',2), ('EResourceConfiguration_2x10MHz',3), ('EResourceConfiguration_1x15MHz',4), ('EResourceConfiguration_1x20MHz',5), ('EResourceConfiguration_5_1x5MHz_1x10MHz',6), ('EResourceConfiguration_10_1x5MHz_1x10MHz',7), ('EResourceConfiguration_3MHz',8), ('EResourceConfiguration_1_4MHz',9)]
class EMacToPhyEvent(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EMacToPhyEvent_HoMsg3Fails',0), ('EMacToPhyEvent_NotDefined',1)]
class EUlSyncQualityResult(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EUlSyncQualityResult_NotAttempted',0), ('EUlSyncQualityResult_OutOfSyncQuality',1), ('EUlSyncQualityResult_InSyncQuality',2)]
class ECqiQualityResult(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ECqiQualityResult_NotAttempted',0), ('ECqiQualityResult_Dtx',1), ('ECqiQualityResult_Tx',2), ('ECqiQualityResult_CrcFailed',3), ('ECqiQualityResult_InvalidParam',100), ('ECqiQualityResult_NotEnoughResources',101), ('ECqiQualityResult_DeadlineMissed',102)]
class EDlHarqAckResult(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EDlHarqAckResult_NotAttempted',0), ('EDlHarqAckResult_Dtx',1), ('EDlHarqAckResult_Tx',2), ('EDlHarqAckResult_Nack_Dtx',3), ('EDlHarqAckResult_InvalidParam',100), ('EDlHarqAckResult_NotEnoughResources',101), ('EDlHarqAckResult_DeadlineMissed',102)]
class ESrResult(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ESrResult_NotDetected',0), ('ESrResult_Detected',1), ('ESrResult_InvalidParam',100), ('ESrResult_NotEnoughResources',101), ('ESrResult_DeadlineMissed',102)]
class ETimeChInfoValid(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETimeChInfoValid_Invalid',0), ('ETimeChInfoValid_10',1), ('ETimeChInfoValid_20',2), ('ETimeChInfoValid_50',3), ('ETimeChInfoValid_100',4), ('ETimeChInfoValid_200',5), ('ETimeChInfoValid_500',6), ('ETimeChInfoValid_1000',7), ('ETimeChInfoValid_1500',8), ('ETimeChInfoValid_2000',9), ('ETimeChInfoValid_Infinite',10)]
class EMacToPhyEventType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EMacToPhyEventType_Pusch',0), ('EMacToPhyEventType_Prach',1), ('EMacToPhyEventType_Pucch',2)]
class EDlTestMode(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EDlTestMode_Normal',0), ('EDlTestMode_Trial',1)]
class ERunMode(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERunMode_Normal',0), ('ERunMode_RfLoopback',1), ('ERunMode_NumberOf',2)]
class ECpLength(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ECpLength_Normal',0), ('ECpLength_Extended',1)]
class ERiQualityResult(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERiQualityResult_NotAttempted',0), ('ERiQualityResult_Dtx',1), ('ERiQualityResult_Tx',2)]
class ETransmissionScheme(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETransmissionScheme_Localized',0), ('ETransmissionScheme_Distributed',1)]
class ESyncSigTxMode(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ESyncSigTxMode_SingleTx',0), ('ESyncSigTxMode_TxDiversity',1)]
class EDlHarqAckType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EDlHarqAckType_None',0), ('EDlHarqAckType_1bit',1), ('EDlHarqAckType_2bit',2), ('EDlHarqAckType_Multicell',3), ('EDlHarqAckType_Multicell_W1',4), ('EDlHarqAckType_Multicell_W2',5), ('EDlHarqAckType_Multicell_W3',6), ('EDlHarqAckType_Multicell_W4',7)]
class EEnable1TxIn2Tx(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EEnable1TxIn2Tx_Off',0), ('EEnable1TxIn2Tx_On',1)]
class ESrsQualityResult(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ESrsQualityResult_NotAttempted',0), ('ESrsQualityResult_Dtx',1), ('ESrsQualityResult_Tx',2), ('ESrsQualityResult_InvalidParam',100), ('ESrsQualityResult_NotEnoughResources',101), ('ESrsQualityResult_DeadlineMissed',102)]
class EPhyDeployableUnit(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EPhyDeployableUnit_RxResourceManager',0), ('EPhyDeployableUnit_RxChannelizer',1), ('EPhyDeployableUnit_RxPuschReceiver',2), ('EPhyDeployableUnit_RxPrachReceiver',3), ('EPhyDeployableUnit_RxUlMacInterface',4), ('EPhyDeployableUnit_RxDlMacInterface',5), ('EPhyDeployableUnit_RxDecoderMaster',6), ('EPhyDeployableUnit_RxDecoderSlave',7), ('EPhyDeployableUnit_RxPucchReceiver',8), ('EPhyDeployableUnit_RxPrachSlave',9), ('EPhyDeployableUnit_RxSrsReceiver',10), ('EPhyDeployableUnit_RxTestSw',11), ('EPhyDeployableUnit_RxTswMacInterface',12), ('EPhyDeployableUnit_RxPuschReceiverSlave',13), ('EPhyDeployableUnit_RxSrsReceiverSlave',14), ('EPhyDeployableUnit_RxDecoder',15), ('EPhyDeployableUnit_RxPucchReceiverSlave',16), ('EPhyDeployableUnit_RxPrachChannelizer',17), ('EPhyDeployableUnit_RxCalibrationReceiver',18), ('EPhyDeployableUnit_RxPuschReceiverDecoder',19), ('EPhyDeployableUnit_RxChannelizerSecond',20), ('EPhyDeployableUnit_TxChannelProcessing',100), ('EPhyDeployableUnit_TxStreamProcessing',101)]
class EPhichRes(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EPhichRes_1_6',0), ('EPhichRes_1_2',1), ('EPhichRes_1',2), ('EPhichRes_2',3)]
class ECqiRepType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ECqiRepType_0',0), ('ECqiRepType_1',1), ('ECqiRepType_2',2), ('ECqiRepType_3',3), ('ECqiRepType_4',4), ('ECqiRepType_5',5), ('ECqiRepType_6',6), ('ECqiRepType_1a',11), ('ECqiRepType_2a',21), ('ECqiRepType_2b',22), ('ECqiRepType_2c',23), ('ECqiRepType_ambiguous',100)]
class EPucchFormat(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EPucchFormat_1',0), ('EPucchFormat_1a',1), ('EPucchFormat_1b',2), ('EPucchFormat_2',3), ('EPucchFormat_2a',4), ('EPucchFormat_2b',5), ('EPucchFormat_1b_CS',6), ('EPucchFormat_3',7)]

class SDeploymentInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('unitAddr',TAaSysComNid), ('explicitPadding',prophy.u16), ('unitType',EPhyDeployableUnit)]
class SPhyDeployableNode(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('nodeAddr',TAaSysComNid), ('explicitPadding',prophy.u16), ('nodeType',EPhyDeployableNode)]
class SCalibrationParameters(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('calibrationEnabled',TBoolean), ('calibrationPeriod',prophy.u32), ('rxCalibrationStartOffset',prophy.u32), ('rxCalibrationEndOffset',prophy.u32), ('txCalibrationStartOffset',prophy.u32), ('txCalibrationEndOffset',prophy.u32), ('calibrationAntennaCarrier',prophy.u32), ('calibrationSets',prophy.bytes(size=8))]
class SStBfWeightElement(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('weight',prophy.bytes(size=SRS_COMBINE_ANTENNA_NUMBER)), ('frameNumber',TFrameNumber)]
class SStBfWeightNode(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('stBfWeightElem',prophy.bytes(size=SRS_MAX_PRB))]
class STargetUe(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrntiU16), ('stBFWeightUeOffset',prophy.u16)]
class SAntCablingMappingConfig(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('rruPort1AntId',prophy.u8), ('rruPort2AntId',prophy.u8), ('rruPort3AntId',prophy.u8), ('rruPort4AntId',prophy.u8), ('rruPort5AntId',prophy.u8), ('rruPort6AntId',prophy.u8), ('rruPort7AntId',prophy.u8), ('rruPort8AntId',prophy.u8)]
class SDciInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('txPower',TTxPowerI16), ('crnti',TCrntiU16), ('numOfCce',TNumOfCce), ('cceStartIndex',TCceStartIndex), ('tbSize',TTbSizeU8), ('dciFormat',TDciFormatType), ('data',prophy.bytes(size=MAX_NUM_OF_BITS_IN_PDCCH_DIV8))]
class SPhichInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('harqAckIndicatorAndPhichIndex',THarqAckIndicatorAndPhichIndex), ('groupIndex',TPhichGroupIndex), ('txPower',TTxPowerI16)]
class SPhichSendReqBuffer(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfPhichInfo',TNumberOfItems), ('phichInfo',prophy.bytes(size=VARIABLE_SIZE_ARRAY))]
class SPdcchSendReqBuffer(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('txPowerPcfich',TTxPowerI16), ('pdcchSymPowerCorr',prophy.bytes(size=MAX_NUM_CTRL_SYMBOLS)), ('cfiAndFlags',TCfiU8), ('numOfDci',TNumberOfItemsU8), ('dciInfo',prophy.bytes(size=VARIABLE_SIZE_ARRAY))]
class SDlComPdsch(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('crnti',TCrnti), ('cfi',TCfi), ('txPower',TTxPower), ('resources',SPdschResources), ('tbFormat',SDlTbFormat), ('tbSize',TTbSize), ('srioId',TUnitNid), ('tbPointer',TTbPointer), ('tbFlags',prophy.u32)]
class SPhyPrsInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('actOtdoa',TBoolean), ('prsConfigurationIndex',TPrsConfigurationIndex), ('prsBandwidth',ECarrierBandwidth), ('prsNumDlFrames',TPrsNumDlFrames), ('prsMutingInfoPatternLength',TPrsMutingInfoPatternLength), ('prsMutingInfo',prophy.u32), ('actPrsTxDiv',TBoolean), ('txPowerPrs',TTxPower)]
class STxAntennaInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('actSuperCell',TBoolean), ('numOfTxAntennasInCell',prophy.u32), ('txAntMap',prophy.bytes(size=MAX_NUM_OF_ANT_IN_CELL))]
class SCsiRsConfigInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfCsiRsAntennaPorts',prophy.u32), ('csiRsResourceConf',prophy.u32), ('csiRsSubfrConf',prophy.u32), ('txPowerCsiRs',TTxPower)]
class SDlBfCell(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dlSectorBeamformingMode',ESectorBeamformingMode), ('sectorBfWeightforAntenna',prophy.bytes(size=NUM_OF_ANTENNAGROUPS)), ('calibrationParameters',SCalibrationParameters), ('numOfBfAntennas',TNumAntennas), ('timeChInfoValid',ETimeChInfoValid), ('ulPhyInfoInterfaceAddress',TAaSysComSicad), ('csiRsConfigInfo',SCsiRsConfigInfo), ('antCablingMappingConfig',SAntCablingMappingConfig)]
class SDlBfPdsch(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dlBfTbFormat',SDlBfTbFormat)]
class SDlBfInterferenceWeight(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('imag',prophy.i16), ('real',prophy.i16)]
class SBfWeight(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('weightAntennaPair0',SDlBfInterferenceWeight), ('weightAntennaPair1',SDlBfInterferenceWeight), ('weightAntennaPair2',SDlBfInterferenceWeight), ('weightAntennaPair3',SDlBfInterferenceWeight)]
class SDlBfInterferenceParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dlInterferenceSpatialMode',EInterferenceSM), ('dlInterferenceUpdatePeriod',TUpdatePeriod), ('dlInterferenceBFWeightSet',prophy.bytes(size=NUM_OF_BEAMS))]
class SSubCellMeasurement(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('subCellId',TSubCellIdU8), ('numOfSubCellPreamble',TNumberOfItemsU8), ('explicitPadding',prophy.u16), ('interferencePower',TInterferencePower)]
class SFrequencyOffsetInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('elapsedTimePusch',TElapsedTime), ('elapsedTimePucchOrPrach',TElapsedTime), ('frequencyOffsetPusch',TFrequencyOffset), ('frequencyOffsetPucchOrPrach',TFrequencyOffset)]
class SFdChannelEst(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('real',prophy.r32), ('imag',prophy.r32)]
class SPrachParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('prachConfIndex',TPrachConfIndex), ('prachFreqOff',TPrachFreqOff), ('prachCs',TPrachCyclicShift), ('rootSeqIndex',TPrachRootSeqIndex), ('prachHsFlag',TBoolean)]
class SPrachPreamble(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('prachIndex',TPrachIndex), ('signalPower',TSignalPower), ('frequencyOffsetPrach',TFrequencyOffset), ('absoluteTimingAdvance',prophy.u16), ('timingAdvanceStrongestPath',prophy.u16)]
class SPuschResources(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('firstPrb',TPrbNumberU8), ('numPrbs',TNumPrbsU8), ('simultanousSrs',TBooleanU8), ('initialNumPrbs',TNumPrbsU8), ('initialSimultanousSrs',TBooleanU8), ('firstPrbIn2ndSlot',TPrbNumberU8), ('ueContextFlags',prophy.u8), ('explicitPadding2',prophy.u8)]
class SUlRefSigParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ulGrpHop',TBoolean), ('grpAssigPusch',TUlRefSigDeltaSeqShift), ('ulRsCs',TUlRefSigParamNdmrs)]
class SUlTbFormat(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('modulation',TEModulationU8), ('newDataIndicator',TNewDataIndicatorU8), ('harqProcessNumber',THarqProcessNumberU8), ('redundancyVersion',TRedundancyVersionU8)]
class SPuschPrbMeasurement(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('signalPower',TSignalPower), ('interferencePower',TInterferencePower)]
class SSCellInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('harqAckSize',prophy.u8), ('harqProcessesInfoPackedSCell',TDlHarqProcessInfoPacked), ('riCqiIndicator',prophy.u8), ('sCellAddrIndex',prophy.u8), ('ueIndexSCell',TUeIndex), ('explicitPadding',prophy.u16)]
class SPucchUeReceiveReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrntiU16), ('ueIndex',TUeIndex), ('harqProcessesInfoPacked',TDlHarqProcessInfoPacked), ('pucchFormat',TEPucchFormatU8), ('cqiSizeRi1',TCqiSizeU8), ('cqiSizeRi2',TCqiSizeU8), ('cqiSizeRi1Pti0',TCqiSizeU8), ('cqiSizeRi2Pti0',TCqiSizeU8), ('servingSubCellId',TSubCellIdU8), ('candidateSubCellId',TSubCellIdU8), ('cqiRepType',TECqiRepTypeU8), ('srHarqAckCombined',TBooleanU8), ('simulSrAndCqi',TBooleanU8), ('simultanousSrs',prophy.u8), ('resourceIndexAn',prophy.u32), ('resourceIndexAnScell',prophy.u32), ('resourceIndexSr',TPucchResourceIndex16), ('resourceIndexCqi',TPucchResourceIndex16), ('frequencyOffsetInfo',SFrequencyOffsetInfo), ('frequencyOffsetInfoCandiSubCell',SFrequencyOffsetInfo), ('sCellInfo',SSCellInfo)]
class SPucchUeReceiveRespD(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrntiU16), ('ueIndex',TUeIndex), ('pucchFormat',TEPucchFormatU8), ('harqAckResult',TEDlHarqAckResultU8), ('harqAckBits',TDlHarqAckBitsU8), ('harqProcessesInfoPacked',TDlHarqProcessInfoPacked)]
class SPucchUeReceiveRespU(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrntiU16), ('srResult',TESrResultU8), ('explicitPadding',prophy.u8)]
class SPucchUeReceiveCqiRespD(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrntiU16), ('ueIndex',TUeIndex), ('pucchFormat',TEPucchFormatU8), ('cqiSize',TCqiSizeU8), ('cqiRepType',TECqiRepTypeU8), ('cqiQualityResult',TECqiQualityResultU8), ('cqiBits',TCqiBits), ('ulSyncQualityResult',TEUlSyncQualityResultU8), ('explicitPadding',prophy.u8), ('explicitPadding1',prophy.u8), ('explicitPadding2',prophy.u8)]
class SPucchUeReceiveMeasResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrntiU16), ('ueIndex',TUeIndex), ('status',EStatusLte), ('specificCause',ESpecificCauseLte), ('pucchFormat',TEPucchFormatU8), ('cqiQualityResult',TECqiQualityResultU8), ('subCellId',TSubCellIdU8), ('explicitPadding2',prophy.u8), ('rssi',TRssi), ('interferencePower',TInterferencePower), ('frequencyOffsetPucch',TFrequencyOffset), ('phiReal',TTimeEstPhi), ('phiImag',TTimeEstPhi), ('fdChannelEstSlot0',prophy.bytes(size=NUM_OF_RX_ANTENNAS)), ('fdChannelEstSlot1',prophy.bytes(size=NUM_OF_RX_ANTENNAS))]
class SPucchPrbMeasurement(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('totalPower',TTotalPower), ('interferencePower',TInterferencePower)]
class SPucchProcessingLoad(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('srUeLoad',TProcessingLoad), ('cqiUeLoad',TProcessingLoad), ('srsPrbLoad',TProcessingLoad), ('srsUeOverheadLoad',TProcessingLoad)]
class STotalCapacity(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('resourceConfiguration',EResourceConfiguration), ('totalSrCqiCapacity',TProcessingLoad), ('totalSrsCapacity',TProcessingLoad), ('srUeLimit',TNumberOfItems), ('cqiUeLimit',TNumberOfItems), ('srsUeLimit',TNumberOfItems)]
class SCellCqi(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cqiSizeRi1',TCqiSizeU8), ('cqiSizeRi2',TCqiSizeU8), ('cqiSizeRi1Pti0',TCqiSizeU8), ('cqiSizeRi2Pti0',TCqiSizeU8), ('cqiRepType',TECqiRepTypeU8), ('riSize',TRiSizeU8), ('explicitPadding',prophy.u16)]
class SPuschUeReceiveReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrntiU16), ('ueIndex',TUeIndex), ('paramNdmrs',TUlRefSigParamNdmrs), ('harqAckType',TEDlHarqAckTypeU8), ('harqProcessesInfoPacked',TDlHarqProcessInfoPacked), ('cqiSizeRi1',TCqiSizeU8), ('cqiSizeRi2',TCqiSizeU8), ('cqiSizeRi1Pti0',TCqiSizeU8), ('cqiSizeRi2Pti0',TCqiSizeU8), ('servingSubCellId',TSubCellIdU8), ('candidateSubCellId',TSubCellIdU8), ('cqiRepType',TECqiRepTypeU8), ('riSize',TRiSizeU8), ('bundlingMode',TEBundlingModeU8), ('bundleIndex',prophy.u8), ('resources',SPuschResources), ('controlOffsets',SPuschControlOffsets), ('tbFormat',SUlTbFormat), ('tbSize',TTbSize), ('tbPointer',TTbPointer), ('frequencyOffsetInfo',SFrequencyOffsetInfo), ('frequencyOffsetInfoCandiSubCell',SFrequencyOffsetInfo), ('sCellInfo',SSCellInfo), ('sCellCqi',SCellCqi), ('pairedUeIndex',TUeIndex), ('mimoLayer',TMimoLayer)]
class SPuschUeReceiveRespD(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrntiU16), ('ueIndex',TUeIndex), ('harqAckType',TEDlHarqAckTypeU8), ('harqAckResult',TEDlHarqAckResultU8), ('harqAckBits',TDlHarqAckBitsU8), ('harqProcessesInfoPacked',TDlHarqProcessInfoPacked)]
class SPuschUeReceiveCqiRespD(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrntiU16), ('ueIndex',TUeIndex), ('status',EStatusLte), ('specificCause',ESpecificCauseLte), ('cqiSize',TCqiSizeU8), ('cqiRepType',TECqiRepTypeU8), ('cqiQualityResult',TECqiQualityResultU8), ('explicitPadding',prophy.u8), ('cqiBits',prophy.bytes(size=PUSCH_CQI_BIT_TABLE_SIZE)), ('riSize',TRiSizeU8), ('riData',TRiDataU8), ('riQualityResult',TERiQualityResultU8), ('explicitPadding2',prophy.u8)]
class SPuschUeReceiveRespU(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrntiU16), ('harqProcessNumber',THarqProcessNumberU8), ('crcResult',TECrcResultU8), ('ueIndex',TUeIndex), ('explicitPadding',prophy.u16)]
class SPuschUeResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrntiU16), ('ueIndex',TUeIndex), ('harqProcessNumber',THarqProcessNumberU8), ('crcResult',TECrcResultU8), ('tbSize',TTbSize), ('tbPointer',TTbPointer), ('ueContextFlags',prophy.u8), ('txCount',prophy.u8), ('explicitPadding',prophy.u16)]
class SPuschUeReceiveMeasResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrntiU16), ('ueIndex',TUeIndex), ('status',EStatusLte), ('specificCause',ESpecificCauseLte), ('rssi',TRssi), ('interferencePower',TInterferencePower), ('frequencyOffsetPusch',TFrequencyOffset), ('phiReal',TTimeEstPhi), ('phiImag',TTimeEstPhi), ('postCombSinr',prophy.i16), ('ulCompUsage',prophy.u8), ('ulReliabilty',TBooleanU8), ('subCellId',TSubCellIdU8), ('explicitPadding1',prophy.u8), ('explicitPadding2',prophy.u16)]
class SSrsMeasurementReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('startPosition',TPrbNumberU8)]
class SSrsUeReceiveReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrntiU16), ('ueIndex',TUeIndex), ('cyclicShift',TSrsCyclicShiftU8), ('srsBandWidth',TNumPrbsU8), ('startPosition',TNumPrbsU8), ('transComb',TTransCombU8), ('bfMeasurement',prophy.u8), ('explicitPadding',prophy.u8), ('stBFWeightUeOffset',prophy.u16)]
class SSrsUeReceiveRespU(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrntiU16), ('ueIndex',TUeIndex), ('srsQualityResult',TESrsQualityResultU8), ('srsBandWidth',TNumPrbsU8), ('startPosition',TNumPrbsU8), ('payloadOffset',TPayloadOffsetU8), ('subCellId',TSubCellIdU8), ('explicitPadding1',prophy.u8), ('explicitPadding2',prophy.u16)]
class SSrsUeReceiveRespD(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrntiU16), ('ueIndex',TUeIndex), ('status',EStatusLte), ('specificCause',ESpecificCauseLte), ('phiReal',TTimeEstPhi), ('phiImag',TTimeEstPhi), ('timeOffsetEstWeight',TTimeOffsetEstWeight), ('subCellId',TSubCellIdU8), ('explicitPadding1',prophy.u8), ('explicitPadding2',prophy.u16)]
class SSrsPrbMeasurement(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('interferencePower',TInterferencePower)]
class STestModelUlUserParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('resources',SPuschResources), ('modulation',EModulation)]
class SPhyDataBuffer(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('srioId',prophy.u16), ('bSize',prophy.u16), ('bAddress',prophy.u32)]
class SPuschReceiveReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cqiRespDBuffer',SPhyDataBuffer), ('measRespBuffer',SPhyDataBuffer), ('measRespBuffer2',SPhyDataBuffer), ('cellMeasRespBuffer',SPhyDataBuffer), ('rfLoopFlag',TBoolean), ('numOfDelayedUe',TNumberOfItems), ('tmpName',TNumberOfItems), ('delayedUe',prophy.array(TCrntiU16,bound='tmpName')), ('numOfSCellAddressingInfo',TNumberOfItems), ('numOfUePuschReq',TNumberOfItems), ('uePuschReq',prophy.bytes(size=THIS_IS_VARIABLE_SIZE_ARRAY))]
class SPuschReceiveMeasResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfUePuschResp',TNumberOfItems), ('uePuschResp',prophy.bytes(size=THIS_IS_VARIABLE_SIZE_ARRAY))]
class SPuschReceiveCqiRespD(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('uePuschResp',prophy.bytes(size=THIS_IS_VARIABLE_SIZE_ARRAY))]
class SPuschCellMeasResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('totalRxPower',prophy.bytes(size=NUM_OF_TOTAL_RX_POWERS)), ('numOfSubCell',TNumberOfItemsU8), ('subCellId',prophy.bytes(size=MAX_NUM_SUBCELL_PER_SUBPOOL)), ('numberOfLayers',TNumberOfItemsU8), ('numOfPuschPrbMeasurement',TNumberOfItems), ('puschPrbMeasurement',prophy.bytes(size=THIS_IS_VARIABLE_SIZE_ARRAY))]
class SPucchReceiveReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cqiRespDBuffer',SPhyDataBuffer), ('measRespBuffer',SPhyDataBuffer), ('measRespBuffer2',SPhyDataBuffer), ('cellMeasRespBuffer',SPhyDataBuffer), ('pucchRes',TNumPrbs), ('numOfSCellAddressingInfo',TNumberOfItems), ('numOfUePucchReq',TNumberOfItems), ('uePucchReq',prophy.bytes(size=THIS_IS_VARIABLE_SIZE_ARRAY))]
class SPucchReceiveCqiRespD(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfUeResp',TNumberOfItems), ('ueResp',prophy.bytes(size=THIS_IS_VARIABLE_SIZE_ARRAY))]
class SPucchReceiveMeasResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfUeResp',TNumberOfItems), ('ueResp',prophy.bytes(size=THIS_IS_VARIABLE_SIZE_ARRAY))]
class SPucchCellMeasResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfSubCell',TNumberOfItemsU8), ('subCellId',prophy.bytes(size=MAX_NUM_SUBCELL_PER_SUBPOOL)), ('explicitPadding',prophy.u8), ('numOfPucchPrbMeasurement',TNumberOfItems), ('pucchPrbMeasurement',prophy.bytes(size=THIS_IS_VARIABLE_SIZE_ARRAY))]
class SSrsReceiveReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('respUBuffer',SPhyDataBuffer), ('respDBuffer',SPhyDataBuffer), ('cellMeasRespBuffer',SPhyDataBuffer), ('numOfUeReq',TNumberOfItems), ('ueReq',prophy.bytes(size=THIS_IS_VARIABLE_SIZE_ARRAY))]
class SSrsReceiveRespU(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfSrsMeas',TNumberOfItems), ('numOfUeResp',TNumberOfItems), ('ueResp',prophy.bytes(size=THIS_IS_VARIABLE_SIZE_ARRAY))]
class SSrsReceiveRespD(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfUeResp',TNumberOfItems), ('ueResp',prophy.bytes(size=THIS_IS_VARIABLE_SIZE_ARRAY))]
class SSrsCellMeasResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfSubCell',TNumberOfItemsU8), ('subCellId',prophy.bytes(size=MAX_NUM_SUBCELL_PER_SUBPOOL)), ('explicitPadding',prophy.u8), ('numOfSrsPrbMeasurement',TNumberOfItems), ('srsPrbMeasurement',prophy.bytes(size=THIS_IS_VARIABLE_SIZE_ARRAY))]
class SPhyDataHeader(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('buffer',SPhyDataBuffer)]
class SSCellAddresses(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelIdScell',TCellId), ('respDAddress',TAaSysComSicad), ('cqiRespDAddress',TAaSysComSicad)]
class SSCellAddressingInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sCellAddresses',prophy.bytes(size=MAX_NUM_SCELLS))]
class SPhyDataTypes(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('enum1',EBundlingMode), ('enum2',ECqiQualityResult), ('enum3',ECqiRepType), ('enum4',ECrcResult), ('enum5',EDlHarqAckResult), ('enum6',EDlHarqAckType), ('enum7',EModulation), ('enum8',EPucchFormat), ('enum9',ESrResult), ('enum10',ERiQualityResult), ('type1',TRiSize), ('type2',TRiData), ('type3',TNumPrbs), ('type4',TPrbNumber), ('type5',TBoolean), ('type6',TCqiSize), ('type7',TPrbNumber), ('type8',TNumPrbs), ('type9',TNewDataIndicator), ('type10',TSrsCyclicShift), ('type11',TSubCarrierIndex), ('type12',TRedundancyVersion), ('type13',TDlHarqAckBits), ('type14',THarqProcessNumber), ('type15',ESrsQualityResult), ('type16',SSCellAddressingInfo)]
class SMacToPhyEvent(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrntiU16), ('event',TEMacToPhyEventU8), ('type',TEMacToPhyEventTypeU8)]
class SUlCoMPInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ulCoMpSinrThreshold',TCoMpSinrThreshold)]
class SNeighborCellInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('lCelId',TLocalCellResId), ('ulPhyNeighborCellAddr',TAaSysComSicad), ('numOfRxPowerScaling',TNumberOfItems), ('tmpName',TNumberOfItems), ('RxPowerScaling',prophy.array(TRxPowerScaling,bound='tmpName'))]
class SUlAddrGroupInSubPool(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('puschReceiverAddress',TAaSysComSicad), ('pucchReceiverAddress',TAaSysComSicad), ('srsReceiverAddress',TAaSysComSicad)]
class SRxAntennaInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('actSuperCell',TBoolean), ('numOfRxAntennasInCell',prophy.u32), ('rxAntMap',prophy.bytes(size=MAX_NUM_OF_ANT_IN_CELL))]
class SUlBfCell(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('calibrationParameters',SCalibrationParameters), ('antCablingMappingConfig',SAntCablingMappingConfig)]
class SSrsUeBfCovMatrixMeasResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('Crnti',TCrntiU16), ('ueIndex',TUeIndex), ('bfCovMatrix',prophy.bytes(size=MAX_COVARIANCE_MATRIX_ELEMENT)), ('stBFWeight',TStBFWeightPointer)]
class SSrsBfCovMatrixMeasResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfUeResp',TNumberOfItems), ('ueResp',prophy.bytes(size=THIS_IS_VARIABLE_SIZE_ARRAY))]
class PHY_BfAddressReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCellId',TCellId), ('txCaliBufNid',TUnitNid), ('txCalibrationBufferAddress',prophy.u32)]
class PHY_BfAddressResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCellId',TCellId), ('status',EStatusLte), ('shortTermBeamformingBufNid',TUnitNid)]
class PHY_UeBlerTriggerReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('startFrameNumber',TFrameNumber), ('startSubFrameNumber',TSubFrameNumber), ('numOfSubFrame',TNumberOfItems), ('tmpName',TNumberOfItems), ('targetUe',prophy.array(STargetUe,bound='tmpName'))]
class PHY_UlInternalAddressReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('transactionId',TTransactionID), ('tmpName',TNumberOfItems), ('deploymentInfo',prophy.array(SDeploymentInfo,bound='tmpName'))]
class PHY_UlInternalAddressResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('transactionId',TTransactionID)]
class PHY_DlInternalAddressReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('transactionId',TTransactionID), ('tmpName',TNumberOfItems), ('deploymentInfo',prophy.array(SDeploymentInfo,bound='tmpName'))]
class PHY_DlInternalAddressResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('transactionId',TTransactionID)]
class PHY_AddressConfigReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('transactionId',TTransactionID), ('tmpName',TNumberOfItems), ('DeployableNode',prophy.array(SPhyDeployableNode,bound='tmpName'))]
class PHY_AddressConfigResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('transactionId',TTransactionID)]
class PHY_DlCellSetupReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('lCelId',TLocalCellResId), ('phyCellId',TPhyCellId), ('numOfTxPorts',TNumAntennas), ('dlChBw',ECarrierBandwidth), ('cycPrefixDl',ECpLength), ('dlMimoMode',EDlMimoMode), ('syncSigTxMode',ESyncSigTxMode), ('enable1TxIn2Tx',EEnable1TxIn2Tx), ('freqShift1TxIn2Tx',TFreqShift1TxIn2Tx), ('pbIndexPdsch',TPbIndex), ('txPowerRs',TTxPower), ('txPowerSs',TTxPower), ('txPowerScaling',TTxPowerScaling), ('pMax',TMaxTxPower), ('pbIndexPbch',TPbIndex), ('phyPrsInfo',SPhyPrsInfo), ('tddUplinkDownlinkConf',TTddUplinkDownlinkConf), ('tddSpecialSubframeConf',TTddSpecialSubframeConf), ('txAntennaInfo',STxAntennaInfo), ('tmpName',TNumberOfItems), ('dlBfCell',prophy.array(SDlBfCell,bound='tmpName'))]
class PHY_DlCellSetupResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('dlPhyDataAddr',TAaSysComSicad), ('dlPhyTestAddr',TAaSysComSicad)]
class PHY_DlCellDeleteReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId)]
class PHY_DlCellDeleteResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class PHY_DlPhysicalChannelSetupReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('phichRes',EPhichRes), ('phichDur',EPhichDur)]
class PHY_DlPhysicalChannelSetupResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class PHY_DlPhysicalChannelDeleteReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId)]
class PHY_DlPhysicalChannelDeleteResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class PHY_StartRefSyncSReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId)]
class PHY_StartRefSyncSResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class PHY_StopRefSyncSReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId)]
class PHY_StopRefSyncSResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class PHY_DlPhyDataAddressReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('dlErrorIndAddress',TAaSysComSicad)]
class PHY_DlPhyDataAddressResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('status',EStatusLte), ('PbchSendReqAddress',TAaSysComSicad), ('pdcchCw0SendReqAddress',TAaSysComSicad), ('pdcchCw1SendReqAddress',TAaSysComSicad), ('PhichSendReqAddress',TAaSysComSicad), ('pdschCw0SendReqAddress',TAaSysComSicad), ('pdschCw1SendReqAddress',TAaSysComSicad), ('requestCtrlMsgBufferCw0',TPhyMsgPointer), ('requestCtrlMsgBufferCw1',TPhyMsgPointer), ('qmRxFlowId',prophy.u32), ('srioType9Cos',prophy.u32), ('srioType9StreamId',prophy.u32), ('pdschEventQueueId',prophy.u32)]
class PHY_PbchSendReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('txPower',TTxPower), ('tbSize',TTbSize), ('data',prophy.bytes(size=MAX_NUM_OF_BITS_IN_PBCH_DIV8))]
class PHY_PdcchSendReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('requestCtrlMsgBuffer',TPhyMsgPointer), ('requestMsg',SPdcchSendReqBuffer)]
class PHY_PdschSendReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dlComPdsch',SDlComPdsch), ('tmpName',TNumberOfItems), ('dlBfPdsch',prophy.array(SDlBfPdsch,bound='tmpName'))]
class PHY_PhichSendReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('requestCtrlMsgBuffer',TPhyMsgPointer), ('requestMsg',SPhichSendReqBuffer)]
class PHY_DlErrorInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('frameNumber',TFrameNumber), ('subframeNumber',TSubFrameNumber), ('numDroppedPdschSendReq',TNumberOfItems), ('droppedPdschDataSize',TTbSize)]
class PHY_Start3GppDlTestModelReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('testModelId',ETestModelId), ('antennaMap',TAntennaPort)]
class PHY_Start3GppDlTestModelResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class PHY_Stop3GppDlTestModelReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId)]
class PHY_Stop3GppDlTestModelResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class PHY_DlStartRfLoopTestReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('txPowerLoop',TTxPower), ('antennaMap',TAntennaPort)]
class PHY_DlStartRfLoopTestResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class PHY_DlInterferenceGenerationReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('dlInterferenceEnable',TBoolean), ('dlInterferenceLevel',TDlInterferenceLevel), ('dlInterferenceTxPower',TTxPower), ('dlInterferenceModulation',EModulation), ('tmpName',TNumberOfItems), ('dlBfInterferenceParams',prophy.array(SDlBfInterferenceParams,bound='tmpName'))]
class PHY_DlInterferenceGenerationResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class PHY_DlCellShutdownReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('pwrReductionStepSize',TPwrReduction), ('stepDuration',TStepDuration), ('shutdownStepAmount',TShutdownStepAmnt)]
class PHY_DlCellShutdownResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class PHY_DlCellReconfigurationReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('txPowerRs',TTxPower), ('txPowerSs',TTxPower), ('phyPrsInfo',SPhyPrsInfo)]
class PHY_DlCellReconfigurationResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class PHY_UlCellSetupReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('lCelId',TLocalCellResId), ('phyCellId',TPhyCellId), ('carrierBandwidth',ECarrierBandwidth), ('cyclicPrefixLength',ECpLength), ('rxPowerScaling',prophy.bytes(size=NUM_OF_RX_SCALING_VALUES)), ('pucchParameters',SPucchConfiguration), ('ulRefSigParameters',SUlRefSigParams), ('hsTrainScenario',EHsTrainScenario), ('actUlMuMimo',TBoolean), ('blankedPucch',TNCqiRb), ('tddUplinkDownlinkConf',TTddUplinkDownlinkConf), ('tddSpecialSubframeConf',TTddSpecialSubframeConf), ('runMode',ERunMode), ('ulCombinationMode',EUlCombinationMode), ('numOfRxDivAntennas',TNumAntennas), ('rxAntennaInfo',SRxAntennaInfo), ('actReduceWimaxInterference',TBoolean), ('ulCoMPInfo',SUlCoMPInfo), ('tmpName',TNumberOfItems), ('ulBfCell',prophy.array(SUlBfCell,bound='tmpName'))]
class PHY_UlCellSetupResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('ulPhyDataAddr',TAaSysComSicad)]
class PHY_UlCellDeleteReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId)]
class PHY_UlCellDeleteResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class PHY_PrachSetupReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('prachParameters',SPrachParams)]
class PHY_PrachSetupResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class PHY_PrachDeleteReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId)]
class PHY_PrachDeleteResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class PHY_UlPhyDataAddressReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('prachReceiveIndAddress',TAaSysComSicad), ('puschReceiveRespDAddress',TAaSysComSicad), ('puschReceiveCqiRespDAddress',TAaSysComSicad), ('puschReceiveMeasRespAddress1',TAaSysComSicad), ('puschReceiveMeasRespAddress2',TAaSysComSicad), ('numOfUeGroups',TNumberOfItems), ('puschReceiveRespUAddress',prophy.bytes(size=MAX_NUM_UEGROUP_PER_BB_POOL_RL70)), ('puschReceiveRespUAddress2',TAaSysComSicad), ('pucchReceiveRespDAddress',TAaSysComSicad), ('pucchReceiveCqiRespDAddress',TAaSysComSicad), ('pucchReceiveMeasRespAddress1',TAaSysComSicad), ('pucchReceiveMeasRespAddress2',TAaSysComSicad), ('pucchReceiveRespUAddress',TAaSysComSicad), ('srsReceiveRespDAddress',TAaSysComSicad), ('srsReceiveRespUAddress',TAaSysComSicad), ('puschCellMeasRespAddress',TAaSysComSicad), ('pucchCellMeasRespAddress',TAaSysComSicad), ('srsCellMeasRespAddress',TAaSysComSicad), ('srsBfCovMatrixMeasRespAddress',TAaSysComSicad), ('ulResourceUpdateAddress',TAaSysComSicad)]
class PHY_UlPhyDataAddressResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('status',EStatusLte), ('puschReceiverAddress',TAaSysComSicad), ('pucchReceiverAddress',TAaSysComSicad), ('srsReceiverAddress',TAaSysComSicad), ('stWeightVectorAddr',prophy.u32), ('numOfSubPools',prophy.u32), ('ulAddrGroupInSubpool',prophy.bytes(size=MAX_NUM_SUBPOOLS))]
class PHY_UlResourceInfoReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('transactionId',TTransactionID)]
class PHY_UlResourceInfoResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('transactionId',TTransactionID), ('pucchProcessingLoad',SPucchProcessingLoad), ('tmpName',TNumberOfItems), ('totalCapacity',prophy.array(STotalCapacity,bound='tmpName'))]
class PHY_UlResourceUpdateReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('maxPuschUesTti',TNumberOfItems)]
class PHY_UlResourceUpdateResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('status',EStatusLte)]
class PHY_PuschReceiveReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('header',SPhyDataHeader), ('message',SPuschReceiveReq)]
class PHY_PuschReceiveRespD(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('tmpName',TNumberOfItems), ('uePuschResp',prophy.array(SPuschUeReceiveRespD,bound='tmpName'))]
class PHY_PuschReceiveCqiRespD(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('header',SPhyDataHeader), ('message',SPuschReceiveCqiRespD)]
class PHY_PuschReceiveRespU(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('lastMsgInTti',prophy.u16), ('numOfRespUsInTti',prophy.u16), ('tmpName',TNumberOfItems), ('uePuschResp',prophy.array(SPuschUeResp,bound='tmpName'))]
class PHY_PuschReceiveGroupedRespU(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('tmpName',TNumberOfItems), ('uePuschResp',prophy.array(SPuschUeReceiveRespU,bound='tmpName'))]
class PHY_PuschReceiveMeasResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('header',SPhyDataHeader), ('message',SPuschReceiveMeasResp)]
class PHY_PuschCellMeasResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('header',SPhyDataHeader), ('message',SPuschCellMeasResp)]
class PHY_PucchReceiveReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('header',SPhyDataHeader), ('message',SPucchReceiveReq)]
class PHY_PucchReceiveRespD(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('tmpName',TNumberOfItems), ('ueResp',prophy.array(SPucchUeReceiveRespD,bound='tmpName'))]
class PHY_PucchReceiveCqiRespD(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('header',SPhyDataHeader), ('message',SPucchReceiveCqiRespD)]
class PHY_PucchReceiveRespU(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('tmpName',TNumberOfItems), ('ueResp',prophy.array(SPucchUeReceiveRespU,bound='tmpName'))]
class PHY_PucchReceiveMeasResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('header',SPhyDataHeader), ('message',SPucchReceiveMeasResp)]
class PHY_PucchCellMeasResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('header',SPhyDataHeader), ('message',SPucchCellMeasResp)]
class PHY_SrsReceiveReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('header',SPhyDataHeader), ('message',SSrsReceiveReq)]
class PHY_SrsReceiveRespD(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('header',SPhyDataHeader), ('message',SSrsReceiveRespD)]
class PHY_SrsReceiveRespU(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('header',SPhyDataHeader), ('message',SSrsReceiveRespU)]
class PHY_SrsCellMeasResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('header',SPhyDataHeader), ('message',SSrsCellMeasResp)]
class PHY_PrachReceiveInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('preambleFra',TPreambleFra), ('interferencePower',TInterferencePower), ('numOfSubCell',TNumberOfItemsU8), ('explicitPadding1',prophy.u8), ('explicitPadding2',prophy.u16), ('subCellMeasurement',prophy.bytes(size=MAX_NUM_SUBCELL_PER_SUBPOOL)), ('tmpName',TNumberOfItems), ('preamble',prophy.array(SPrachPreamble,bound='tmpName'))]
class PHY_PuschReceiveRejectedResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('specificCause',ESpecificCauseLte)]
class PHY_PucchReceiveRejectedResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('specificCause',ESpecificCauseLte)]
class PHY_SrsReceiveRejectedResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('specificCause',ESpecificCauseLte)]
class PHY_StartTestModelUlReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('numberOfUsers',TNumberOfItems), ('testModelUser',prophy.bytes(size=MAX_UL_TEST_MODEL_USERS))]
class PHY_StartTestModelUlResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class PHY_StopTestModelUlReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId)]
class PHY_StopTestModelUlResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class PHY_EventDetectedInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('frameNumber',TFrameNumber), ('subFrameNumber',TSubFrameNumber), ('numOfEvents',TNumberOfItemsU8), ('event',prophy.bytes(size=MAX_NUM_OF_MAC_TO_PHY_EVENTS))]
class PHY_UlCompNeighborCellAttachReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('neighborCellInfo',SNeighborCellInfo)]
class PHY_UlCompNeighborCellAttachResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('neighborLnCelId',TCellId)]
class PHY_UlCompNeighborCellDetachReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('neighborLnCelId',TCellId)]
class PHY_UlCompNeighborCellDetachResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('neighborLnCelId',TCellId)]
class PHY_UlCompParamUpdateReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('ulCoMPInfo',SUlCoMPInfo)]
class PHY_UlCompParamUpdateResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId)]
class PHY_SrsBfCovMatrixMeasResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('Header',SPhyDataHeader), ('Message',SSrsBfCovMatrixMeasResp)]
