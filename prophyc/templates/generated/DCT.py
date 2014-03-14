import prophy 
from externals import *
from globals import *


MAX_NUMBER_OF_DETECTED_PREAMBLES = 64
DCT_G1M2_GROUP_SIZE = 1
MAX_NUMBER_OF_S_CELLS = 4
NUMBER_OF_DTCH = 8
NUMBER_OF_DCCH = 2
NUMBER_OF_TRANSPORT_BLOCKS = 2
MAX_U8_RANGE = 255
MAX_PDU_DATA_LENGTH = 9422
MAX_PDU_PER_REPORT = 75376
DCT_DL_LEV_OFDM_GROUP_SIZE = 3
NUMBER_OF_CQI_VALUES = 16
MAX_UL_RBG = 16
MAX_PDU_SIZE = 75376
MAX_UL_PDU = 32
MAX_DL_PDU_MIMO = 32
MAX_DL_PDU = 16
MAX_DL_DCI_PER_REPORT = 16
MAX_UL_DCI_PER_REPORT = 32
MAX_NUMBER_OF_PHICH_GRP = 50
MAX_NUMBER_OF_DCI = 32
MAX_NUMBER_OF_DETECTED_PREAMBLES__VARIABLE_SIZE = MAX_NUMBER_OF_DETECTED_PREAMBLES
MAX_NUM_RB_PER_USER__VARIABLE_SIZE = MAX_NUM_RB_PER_USER
MAX_DL_DCI_PER_REPORT__VARIABLE_SIZE = MAX_DL_DCI_PER_REPORT
MAX_DL_PDU_MIMO__VARIABLE_SIZE = MAX_DL_PDU_MIMO
MAX_DL_PDU__VARIABLE_SIZE = MAX_DL_PDU
MAX_PDU_DATA_LENGTH__VARIABLE_SIZE = MAX_PDU_DATA_LENGTH
MAX_UL_DCI_PER_REPORT__VARIABLE_SIZE = MAX_UL_DCI_PER_REPORT
MAX_UL_PDU__VARIABLE_SIZE = MAX_UL_PDU
MAX_NUMBER_OF_S_CELLS_VARIABLE_SIZE = MAX_NUMBER_OF_S_CELLS

TBitThroughput = prophy.u32
TResAllocType = prophy.u32
TMcsDct = prophy.u8
TRelativePower = prophy.u32
TTpcCmd = prophy.u8
TDlAckResult = prophy.u8
TFrequency = prophy.u32
TLinearTxPower = prophy.u32
TLinearRxPower = prophy.u32


class SDctG1M2Group(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('rxPowerBranch0',TLinearRxPower), ('rxPowerBranch1',TLinearRxPower)]
class SUlRbgGroup(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dctG1M3',TLinearRxPower), ('dctG1M5',TLinearRxPower)]
class SDctUlLevL1Cell(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sfn',TSfn), ('cellId',TCellId), ('dctG1M2Group',SDctG1M2Group), ('dctG1M4',TLinearRxPower), ('dctG1M6',TLinearRxPower), ('dctG1M7',TLinearRxPower), ('numberOfUlRbg',u8), ('ulRbgGroup',prophy.array(SUlRbgGroup,bound='numberOfUlRbg'))]
class SUlRbgGroup2(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dctG1M10',TRelativePower)]
class SUlSyncStatus(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ulSyncStatus',prophy.u8), ('ulResourceStatus',prophy.u8)]
class SDctUlLevL1UeResult(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('dctG1M9',TRelativePower), ('numberOfUlRbg',u8), ('ulRbgGroup',prophy.array(SUlRbgGroup2,bound='numberOfUlRbg')), ('dctG2M10',TFrequency), ('dctG1M18',TRelativePower), ('dctG1M19',SUlSyncStatus)]
class SDctUlLevL1Ue(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sfn',TSfn), ('numberOfUsers',prophy.u32), ('tmpName',TNumberOfItems), ('dctUlLevL1UeResults',prophy.array(SDctUlLevL1UeResult,bound='tmpName'))]
class SDciMappingInformationGroup(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dctG1M14',prophy.u8)]
class SDciTxPowerGroup(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dctG1M15',TLinearTxPower)]
class SPhichGroupTxPowerGroup(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dctG1M16Power',TLinearTxPower), ('dctG1M16NumberOfResouceElements',prophy.u32)]
class SDctDlLevOfdmGroup(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dctG1M17',TLinearTxPower)]
class SDctDlLevL1Cell(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sfn',TSfn), ('subFrameCounter',TSubFrameNumber), ('cellId',TCellId), ('dctG1M13',TLinearTxPower), ('tmpName',TNumberOfItems), ('dciMappingInformationGroup',prophy.array(SDciMappingInformationGroup,bound='tmpName')), ('tmpName',TNumberOfItems), ('dciTxPowerGroup',prophy.array(SDciTxPowerGroup,bound='tmpName')), ('tmpName',TNumberOfItems), ('phichGroupTxPowerGroup',prophy.array(SPhichGroupTxPowerGroup,bound='tmpName')), ('dctDlLevOfdmGroup',prophy.bytes(size=DCT_DL_LEV_OFDM_GROUP_SIZE))]
class SDctUlsch0Result(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('dctG2M2',prophy.u32), ('dctG2M7',prophy.u32), ('dctG2M8',prophy.u32), ('dctG2M9',prophy.u32), ('dctG2M11',prophy.u8), ('dctG2M12',prophy.u8), ('dctG2M13',prophy.i32)]
class SDctUlsch0(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sfn',TSfn), ('numberOfUsers',prophy.u32), ('tmpName',TNumberOfItems), ('SDctUlsch0Results',prophy.array(SDctUlsch0Result,bound='tmpName'))]
class SDctG2M4(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('accumulatedData',prophy.u32), ('numberOfSubframes',prophy.u16)]
class SDctUlsch1Result(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('dctG2M3',prophy.u32), ('dctG2M5',prophy.u32), ('dctG2M6',prophy.u32), ('dctG2M4',SDctG2M4)]
class SDctUlsch1(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sfn',TSfn), ('numberOfUsers',prophy.u32), ('tmpName',TNumberOfItems), ('SDctUlsch1Results',prophy.array(SDctUlsch1Result,bound='tmpName'))]
class SDctUlschData0Result(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dciFormat',TDciFormatType), ('dctG3M4',prophy.u8), ('dctG3M5',prophy.u8), ('dctG3M6',prophy.u8), ('dctG3M7',prophy.u8), ('dctG3M8',TMcsDct), ('dctG3M9',prophy.u8), ('dctG3M11',prophy.u8), ('dctG3M12',TTpcCmd), ('dctG3M13',prophy.u8), ('dctG3M14',prophy.u8), ('dctG3M41',prophy.u8), ('crnti',TCrnti), ('ueId',TUeId), ('dctG3M10',prophy.u32), ('dctG3M25',prophy.i32), ('dctG3M26',prophy.i32), ('dctG3M27',prophy.i32), ('dctG3M28',prophy.i32), ('dctG3M29',prophy.u32), ('dctG3M30',prophy.i32), ('dctG3M311',prophy.u32), ('dctG3M312',prophy.u32), ('dctG3M313',prophy.u32), ('dctG3M314',prophy.u32), ('dctG3M32',TBitThroughput), ('dctG3M33',prophy.i8), ('dctG3M34',prophy.u8), ('dctG3M35',prophy.u8), ('dctG3M36',prophy.u32), ('dctG3M37',prophy.u8), ('dctG3M38',prophy.i32), ('dctG3M39',prophy.u32), ('dctG3M40',prophy.i32)]
class SDctUlschData0(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('sfn',TSfn), ('subFrameCounter',TSubFrameNumber), ('numberOfDciElements',u32), ('SDctUlschData0Results',prophy.array(SDctUlschData0Result,bound='numberOfDciElements'))]
class SDcchGroup2(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dctG3M15',prophy.u32)]
class SDtchGroup2(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dctG3M16',prophy.u32)]
class SDctUlschData1Result(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrnti), ('ueId',TUeId), ('numberOfDcch',u8), ('dcchGroup',prophy.array(SDcchGroup2,bound='numberOfDcch')), ('numberOfDtch',u8), ('dtchGroup',prophy.array(SDtchGroup2,bound='numberOfDtch')), ('dctG3M17',prophy.u32), ('dctG3M18',prophy.u32), ('dctG3M19',prophy.u32), ('dctG3M20',prophy.u32), ('dctG3M21',prophy.u8), ('dctG3M22',prophy.u8)]
class SDctUlschData1(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('sfn',TSfn), ('subFrameCounter',TSubFrameNumber), ('tmpName',TNumberOfItems), ('dctUlschData1Results',prophy.array(SDctUlschData1Result,bound='tmpName'))]
class SDctUlschData2Result(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('crnti',TCrnti), ('ueId',TUeId), ('dctG3M23',prophy.u8), ('dctG3M24',TRelativePower)]
class SDctUlschData2(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('sfn',TSfn), ('subFrameCounter',TSubFrameNumber), ('numberOfDctUlschData2Results',u32), ('SDctUlschData2Results',prophy.array(SDctUlschData2Result,bound='numberOfDctUlschData2Results'))]
class SDctG5M7Group(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numberOfCqiReports',prophy.u32)]
class SDctDlSch0Results(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('dctG5M2',prophy.u32), ('dctG5M4',prophy.u32), ('dctG5M5',prophy.u32), ('dctG5M7Group',prophy.bytes(size=NUMBER_OF_CQI_VALUES)), ('dctG5M8',prophy.u32), ('dctG5M9',prophy.u8), ('dctG5M10',prophy.u32)]
class SDctDlsch0(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sfn',TSfn), ('numberOfUsers',prophy.u32), ('tmpName',TNumberOfItems), ('dctDlSch0Results',prophy.array(SDctDlSch0Results,bound='tmpName'))]
class SDctSCellInformationDlsch0(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('dctG5M21',prophy.u32), ('dctG5M41',prophy.u32), ('dctG5M51',prophy.u32), ('dctG5M7Group',prophy.bytes(size=NUMBER_OF_CQI_VALUES)), ('dctG5M81',prophy.u32)]
class SDctDlsch0Ca(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sfn',TSfn), ('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('dctG5M2',prophy.u32), ('dctG5M4',prophy.u32), ('dctG5M5',prophy.u32), ('dctG5M7Group',prophy.bytes(size=NUMBER_OF_CQI_VALUES)), ('dctG5M8',prophy.u32), ('dctG5M9',prophy.u8), ('dctG5M10',prophy.u32), ('tmpName',TNumberOfItems), ('dctSCellInformationDlsch0',prophy.array(SDctSCellInformationDlsch0,bound='tmpName'))]
class SDctDlsch1Result(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('dctG5M3',prophy.u32), ('dctG5M6',prophy.u32)]
class SDctDlsch1(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sfn',TSfn), ('numOfDctDlsch1Results',prophy.u32), ('tmpName',TNumberOfItems), ('dctDlsch1Results',prophy.array(SDctDlsch1Result,bound='tmpName'))]
class SDctSCellInformationDlsch1(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('dctG5M31',prophy.u32), ('dctG5M61',prophy.u32)]
class SDctDlsch1Ca(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sfn',TSfn), ('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('dctG5M3',prophy.u32), ('dctG5M6',prophy.u32), ('tmpName',TNumberOfItems), ('dctSCellInformationDlsch1',prophy.array(SDctSCellInformationDlsch1,bound='tmpName'))]
class STransportBlockInformationGroup(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('transportBlockNumber',prophy.u8), ('dctG6M10',TMcsDct), ('dctG6M11',prophy.u8), ('dctG6M13',prophy.u8), ('dctG6M12',prophy.u32), ('dctG6M14',prophy.u8), ('dctG6M36',prophy.u8)]
class SCodeWordBlockInformation(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('codewordIndex',prophy.u8), ('dctG6M30',prophy.i32), ('dctG6M31',prophy.i32), ('dctG6M32',prophy.u32)]
class SDctSyncRequestInformation(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('preambleIndex',prophy.u32), ('prachmaskIndex',prophy.u32)]
class SDctDlschData0Result(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('rnti',TCrnti), ('ueId',TUeId), ('dctG6M7',prophy.u32), ('dctG6M5',prophy.u32), ('dctG6M6',TResAllocType), ('dctG6M4',TDciFormatType), ('dctG6M8',prophy.u8), ('dctG6M9',TResAllocType), ('numberOfTranportBlocks',prophy.u8), ('tmpName',TNumberOfItems), ('transportBlockInformationGroup',prophy.array(STransportBlockInformationGroup,bound='tmpName')), ('codeWordBlockInformation',prophy.bytes(size=2)), ('dctG6M33',TBitThroughput), ('dctG6M34',prophy.i32), ('dctG6M35',prophy.u8), ('dctG6M20',TTpcCmd), ('dctG6M21',prophy.u8), ('dctG6M37',prophy.u8), ('dctG6M38',prophy.u16), ('dctG6M39',SDctSyncRequestInformation), ('dctG6M40',prophy.u8), ('dctG6M41',prophy.i32), ('dctG6M42',prophy.u32), ('dctG6M43',prophy.i32)]
class SDctDlschData0(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sfn',TSfn), ('subFrameCounter',TSubFrameNumber), ('cellId',TCellId), ('numberOfDciElements',u32), ('dctDlschData0Results',prophy.array(SDctDlschData0Result,bound='numberOfDciElements'))]
class SDctDlschData0ResultCa(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('rnti',TCrnti), ('ueId',TUeId), ('dctG6M7',prophy.u32), ('dctG6M5',prophy.u32), ('dctG6M6',TResAllocType), ('dctG6M4',TDciFormatType), ('dctG6M8',prophy.u8), ('dctG6M9',TResAllocType), ('numberOfTranportBlocks',prophy.u8), ('tmpName',TNumberOfItems), ('transportBlockInformationGroup',prophy.array(STransportBlockInformationGroup,bound='tmpName')), ('codeWordBlockInformation',prophy.bytes(size=2)), ('dctG6M33',TBitThroughput), ('dctG6M34',prophy.i32), ('dctG6M35',prophy.u8), ('dctG6M20',TTpcCmd), ('dctG6M21',prophy.u8), ('dctG6M37',prophy.u8), ('dctG6M38',prophy.u16), ('dctG6M44',prophy.u16), ('dctG6M39',SDctSyncRequestInformation), ('dctG6M40',prophy.u8), ('dctG6M41',prophy.i32), ('dctG6M42',prophy.u32), ('dctG6M43',prophy.i32), ('dctG6M45',prophy.u8), ('paddingdctG6M45',prophy.u16)]
class SDctDlschData0Ca(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sfn',TSfn), ('subFrameCounter',TSubFrameNumber), ('cellId',TCellId), ('numberOfDciElements',u32), ('dctDlschData0ResultsCa',prophy.array(SDctDlschData0ResultCa,bound='numberOfDciElements'))]
class SDcchGroup(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dctG6M22',prophy.u32)]
class SDtchGroup(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dctG6M23',prophy.u32)]
class SDctDlschData1Result(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('transportBlockNumber',prophy.u8), ('rnti',TCrnti), ('ueId',TUeId), ('dctG6M28',prophy.u8), ('tmpName',TNumberOfItems), ('dcchGroup',prophy.array(SDcchGroup,bound='tmpName')), ('tmpName',TNumberOfItems), ('dtchGroup',prophy.array(SDtchGroup,bound='tmpName')), ('dctG6m24',prophy.u32), ('dctG6m25',prophy.u32), ('dctG6m26',prophy.u32), ('dctG6m27',prophy.u32)]
class SDctDlschData1(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('sfn',TSfn), ('subFrameCounter',TSubFrameNumber), ('numberOfPdus',u32), ('dctDlschData1Result',prophy.array(SDctDlschData1Result,bound='numberOfPdus'))]
class SAckNackResult(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dctG6M29',TDlAckResult), ('crnti',TCrnti), ('ueId',TUeId)]
class SDctDlschData2(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('sfn',TSfn), ('subFrameCounter',TSubFrameNumber), ('numberOfAckNack',u8), ('ackNackResults',prophy.array(SAckNackResult,bound='numberOfAckNack'))]
class SDctDlschData3Result(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('rnti',TCrnti), ('dctG6m26',prophy.u32), ('dctG6m27',prophy.u32), ('dctG6M28',prophy.u8)]
class SDctDlschData3(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('sfn',TSfn), ('subFrameCounter',TSubFrameNumber), ('sequenceNumber',prophy.u8), ('numberOfPdus',u32), ('dctDlschData3Result',prophy.array(SDctDlschData3Result,bound='numberOfPdus'))]
class SDctMacPduDump(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueId',TUeId), ('sfn',TSfn), ('subFrameCounter',TSubFrameNumber), ('cellId',TCellId), ('nbrOfRetransmission',prophy.u8), ('sequenceNumber',prophy.u8), ('pcellscellinfo',prophy.u16), ('pduSize',prophy.u32), ('pduDataLength',u32), ('dctG7M1',prophy.array(u8,bound='pduDataLength'))]
class SDctUci(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sfn',TSfn), ('subFrameCounter',TSubFrameNumber), ('cellId',TCellId), ('ueId',TUeId), ('sequenceNumber',prophy.u32), ('dctG12M1',prophy.u8), ('dctG12M2',prophy.u8), ('dctG12M3',prophy.i8), ('dctG12M4',prophy.i8), ('dctG12M5',prophy.i8), ('dctG12M6',prophy.i8), ('dctG12M7',SUlSyncStatus)]
class SDctSCellStatus(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('dctG12M9',prophy.u8), ('dctG12M10',prophy.u8)]
class SDctUciInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('dctG12M3',prophy.i8), ('dctG12M4',prophy.i8), ('dctG12M5',prophy.i8), ('dctG12M6',prophy.i8)]
class SDctUciCa(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sfn',TSfn), ('subFrameCounter',TSubFrameNumber), ('cellId',TCellId), ('ueId',TUeId), ('sequenceNumber',prophy.u32), ('dctG12M1',prophy.u8), ('dctG12M2',prophy.u8), ('dctG12M7',SUlSyncStatus), ('dctG12M8',prophy.u8), ('paddingdctG12M81',prophy.u8), ('paddingdctG12M82',prophy.u16), ('tmpName',TNumberOfItems), ('dctSCellStatus',prophy.array(SDctSCellStatus,bound='tmpName')), ('tmpName',TNumberOfItems), ('dctUciInfo',prophy.array(SDctUciInfo,bound='tmpName'))]
class SDctRaResults(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dctG14M1',prophy.u8), ('dctG14M2',prophy.u16), ('dctG14M3',prophy.u16), ('dctG14M4',prophy.u32)]
class SDctRa(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('sfn',TSfn), ('subFrameCounter',TSubFrameNumber), ('sequenceNumber',prophy.u8), ('tmpName',TNumberOfItems), ('dctRaResults',prophy.array(SDctRaResults,bound='tmpName'))]
class SDctDlRlcAmPduResult(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('isSrbId',TBoolean), ('rbIdentifier',TRadioBearerId), ('dctG9M1',prophy.u32), ('dctG9M2',prophy.u32), ('dctG9M3',TPercentage)]
class SDlRbsAmResult(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('numberOfRadioBearers',u8), ('dctDlRlcAmPduResults',prophy.array(SDctDlRlcAmPduResult,bound='numberOfRadioBearers'))]
class SDctDlRlcAmPdu(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numberOfUsers',prophy.u32), ('tmpName',TNumberOfItems), ('rbsResults',prophy.array(SDlRbsAmResult,bound='tmpName'))]
class SDctUlRlcAmPduResult(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('isSrbId',TBoolean), ('rbIdentifier',TRadioBearerId), ('dctG9M4',prophy.u32)]
class SUlRbsAmResult(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('numberOfRadioBearers',u8), ('dctUlRlcAmPduResults',prophy.array(SDctUlRlcAmPduResult,bound='numberOfRadioBearers'))]
class SDctUlRlcAmPdu(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numberOfUsers',u32), ('rbsResults',prophy.array(SUlRbsAmResult,bound='numberOfUsers'))]
class SDctDlRlcUmPduResult(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('isSrbId',TBoolean), ('rbIdentifier',TRadioBearerId), ('dctG9M5',prophy.u32)]
class SDlRbsUmResult(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('numberOfRadioBearers',prophy.u8), ('numberOfRadioBearers',u8), ('dctDlRlcUmPduResults',prophy.array(SDctDlRlcUmPduResult,bound='numberOfRadioBearers'))]
class SDctDlRlcUmPdu(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numberOfUsers',prophy.u32), ('tmpName',TNumberOfItems), ('rbsResults',prophy.array(SDlRbsUmResult,bound='tmpName'))]
class SDctUlRlcUmPduResult(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('isSrbId',TBoolean), ('rbIdentifier',TRadioBearerId), ('dctG9M6',prophy.u32)]
class SUlRbsUmResult(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('numberOfRadioBearers',prophy.u8), ('numberOfRadioBearers',u8), ('dctUlRlcUmPduResults',prophy.array(SDctUlRlcUmPduResult,bound='numberOfRadioBearers'))]
class SDctUlRlcUmPdu(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numberOfUsers',u32), ('rbsResults',prophy.array(SUlRbsUmResult,bound='numberOfUsers'))]
class SDctUlPdcpPduResult(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('isSrbId',TBoolean), ('rbId',TRadioBearerId), ('dctG10M1N',prophy.u32), ('dctG10M1A',prophy.u32)]
class SDctUlPdcpPdu(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('tmpName',TNumberOfItems), ('dctUlPdcpPduResults',prophy.array(SDctUlPdcpPduResult,bound='tmpName'))]
class SDctDlRlcSduResult(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('isSrbId',TBoolean), ('rbIdentifier',TRadioBearerId), ('dctG15M1',prophy.u32), ('dctG15M2',prophy.u32)]
class SDctDlRlcSdu(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('numOfDctDlRlcSduResults',u32), ('dctDlRlcSduResults',prophy.array(SDctDlRlcSduResult,bound='numOfDctDlRlcSduResults'))]
class SDctDlPdcpSduResult(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('isSrbId',TBoolean), ('rbIdentifier',TRadioBearerId), ('dctG11M1',prophy.u32), ('dctG11M2',prophy.u32), ('dctG11M3',prophy.u32), ('dctG11M4',prophy.u32), ('dctG11M5',prophy.u32), ('dctG11M6',prophy.u32), ('dctG11M7',prophy.u32), ('dctG11M8',prophy.u32)]
class SDctDlPdcpSdu(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('tmpName',TNumberOfItems), ('dctDlPdcpSduResults',prophy.array(SDctDlPdcpSduResult,bound='tmpName'))]
class SDctDlPdcpSduResultHdbde(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('isSrbId',TBoolean), ('rbIdentifier',TRadioBearerId), ('dctG11M1',prophy.u32), ('dctG11M2',prophy.u32), ('dctG11M3',prophy.u32), ('dctG11M4',prophy.u32), ('dctG11M5',prophy.u32), ('dctG11M6',prophy.u32), ('dctG11M7',prophy.u32), ('dctG11M8',prophy.u32), ('dctG11M9',prophy.u32), ('dctG11M10',prophy.u32), ('dctG11M11',prophy.u32)]
class SDctDlPdcpSduHdbde(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('tmpName',TNumberOfItems), ('dctDlPdcpSduResultsHdbde',prophy.array(SDctDlPdcpSduResultHdbde,bound='tmpName'))]
class SDctStartParameters(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('startSfn',TSfn)]
