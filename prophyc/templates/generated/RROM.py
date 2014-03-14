import prophy 
from externals import *
from globals import *
from ASN import *
from ASN import *
from ASN import *
from ASN import *
from OAM_MERGED import *
from DCM_MAC_PS import *
from WMP_MAC_PS import *


MAX_NUM_OF_MAPPED_BB_UNIT = 2
MAX_ALLOWED_GU_GROUP_IDS = 256
MAX_NUM_OF_RX_ANTENNAS_IN_CELL = 12
MAX_NUM_OF_TX_ANTENNAS_IN_CELL = 12
MAX_NUM_OF_SUPPORTED_TRACING_FUNCTIONALITIES = 2

TCpId = prophy.u32
TMoc = prophy.u32
TRromRadParamTaTimerInfinity = prophy.u32
TRromRadParamEarfcnOffset = prophy.u32
TRromRadParamEarfcnOffsetSign = prophy.u32
TRromRadDebugLogEnabledGlobal = TBoolean
TRromRadDebugLogEnabledRrom = TBoolean
TRromRadDebugLogEnabledCommon = TBoolean
TRromRadCellStateBufferTimer = prophy.u32
TRromRadBacktracingErrorsEnable = TBoolean
TRromRadBacktraceMaxEventsPerTimePeriod = prophy.u32
TRromRadBacktracingErrorsTimePeriod = prophy.u32
TRromRadParamAutoNeighRemovalTimerPeriod = prophy.u32
TRromRadS1L3AvailabilityTimer = prophy.u32
TRromRadCellSetupPhaseCompleteTimer = prophy.u32
TRromRadParamBlockRfMessages = TBoolean
TRromRadTracingConnExtCellMaxRetries = prophy.u32
TRromRadTracingConnSubscriberMaxRetries = prophy.u32
TRromRadTracingConnOmsMaxRetries = prophy.u32
TRromRadTracingConnReleaseTimer = prophy.u32
TRromRadParamEicicLnCellId01 = prophy.u32
TRromRadParamEicicLnCellId02 = prophy.u32
TRromRadParamEicicLnCellId03 = prophy.u32
TRromRadParamEicicLnCellId04 = prophy.u32
TRromRadParamEicicLnCellId05 = prophy.u32
TRromRadParamEicicLnCellId06 = prophy.u32
TRromRadParamEicicCellType = prophy.u32
TRromRadParamEicicReCqiLimit01 = prophy.u32
TRromRadParamEicicReCqiLimit02 = prophy.u32
TRromRadParamEicicReCqiThreshold01 = prophy.u32
TRromRadParamEicicReCqiThreshold02 = prophy.u32
TRromRadParamEicicAbsPatternLow = prophy.u32
TRromRadParamEicicAbsPatternHigh = prophy.u32
TRromRadParamEicicCQI2PerNp = prophy.u32
TRromRadParamEicicAbsShift = prophy.u32
TRromRadParamRfmMinOutputPwrFdd = prophy.u32
TRromRadParamRfmMinOutputPwrTdd = prophy.u32
TRromRadParamAntennaCarrierTimerFdd = prophy.u32
TRromRadParamAntennaCarrierTimerTdd = prophy.u32
TRromRadHwConfigReqMappedTimer = prophy.u32
TRromRadParamActRIMforUTRAN = TBoolean
TRromRadDummy01 = TBoolean
TRromRadDummy02 = TBoolean
TRromRadDummy03 = TBoolean
TRromRadDummy04 = TBoolean
TRromRadDummy05 = TBoolean
TRromRadDummy06 = prophy.u32
TRromRadDummy07 = prophy.u32
TRromRadDummy08 = prophy.u32
TRromRadDummy09 = prophy.u32
TRromRadDummy10 = prophy.u32

class EIndicationType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EIndicationType_NotDefined',0), ('EIndicationType_CellState',1), ('EIndicationType_HwMapping',2), ('EIndicationType_ThroughputMeasurementReport',4), ('EIndicationType_UlCtrlChannelMeasReport',8), ('EIndicationType_NetworkPlanUpdate',16), ('EIndicationType_PlanActivationComplete',32), ('EIndicationType_HwMappingChange',64), ('EIndicationType_NetworkPlanStorage',128), ('EIndicationType_AllIndications',255)]
class EConnectivity(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EConnectivity_NotConnected',0), ('EConnectivity_Connected',1)]
class ENeighborCellConfig(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ENeighborCellConfig_Complete',0), ('ENeighborCellConfig_Delta',1)]
class ERfLoopTestPhase(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERfLoopTestPhase_Startup',0), ('ERfLoopTestPhase_Measurement',1)]
class EFileType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EFileType_NetworkPlanFile',0), ('EFileType_VendorSpecificDataFile',1), ('EFileType_ActualSCF',2), ('EFileType_FullNetworkPlanFile',3)]
class EConfigurationPhase(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EConfigurationPhase_UnmappedLCRs',0), ('EConfigurationPhase_MappedLCRs',1), ('EConfigurationPhase_Calibration',2)]
class ECellSetupResult(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ECellSetupResult_CellNotAvailable',0), ('ECellSetupResult_CellAvailable',1)]
class EHstConfiguration(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EHstConfiguration_NotApplied',0), ('EHstConfiguration_HstScenario1',1), ('EHstConfiguration_HstScenario3',2), ('EHstConfiguration_HstPucchScenario1',3), ('EHstConfiguration_HstPucchScenario3',4)]
class EX2SetupResult(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EX2SetupResult_SetupSuccessful',0), ('EX2SetupResult_SetupFailed',1)]
class EBbUnitType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EBbUnitType_FspC',0), ('EBbUnitType_FspD',1), ('EBbUnitType_FspE',2), ('EBbUnitType_FspH',3), ('EBbUnitType_FspI',4), ('EBbUnitType_FspJ',5), ('EBbUnitType_FWxx',6), ('EBbUnitType_FspP',7), ('EBbUnitType_FspQ',8), ('EBbUnitType_FspM',9)]
class EDspType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EDspType_Faraday',0), ('EDspType_Nyquist',1), ('EDspType_TurboNyquist',2), ('EDspType_Kepler2DSPCorePac',3)]

class SCMcuUnit(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('unitStatus',EAvailability)]
class SControlUnit(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('controlUnitId',TBoardId), ('cMcuUnit',SCMcuUnit)]
class SBbMcuUnit(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('unitStatus',EAvailability)]
class SBbProcUnit(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('unitStatus',EAvailability), ('dspType',EDspType)]
class SBaseBandUnit(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('bbUnitId',TBoardId), ('bbUnitType',EBbUnitType), ('deploymentInfo',EDeploymentInfo), ('bbMcuUnit',SBbMcuUnit), ('numOfBbProcessors',TNumberOfItems), ('bbProcUnits',prophy.array(SBbProcUnit,bound='numOfBbProcessors')), ('localCellGroupId',TLocalCellGroupId)]
class SLcrInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('localCellGroupId',TLocalCellGroupId), ('numOfBbUnits',TNumberOfItems), ('bbUnits',prophy.array(TBoardId,bound='numOfBbUnits')), ('initialLcrState',EState), ('numOfTxAntennas',TNumberOfItems), ('tmpName',TNumberOfItems), ('txAntennaMap',prophy.array(STxAntennaMapping,bound='tmpName')), ('numOfRxAntennas',TNumberOfItems), ('tmpName',TNumberOfItems), ('rxAntennaMap',prophy.array(SRxAntennaMapping,bound='tmpName')), ('numOfRxPowerScaling',TNumberOfItems), ('rxPowerScaling',prophy.array(TRxPowerScaling,bound='numOfRxPowerScaling')), ('txPowerScaling',TTxPowerScaling), ('calibrationParametersId',prophy.u32), ('calibrationSetupAddress',TAaSysComSicad), ('sectorId',prophy.u8)]
class SUnmappedLCRs(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfFcmUnits',TNumberOfItems), ('controlUnits',prophy.array(SControlUnit,bound='numOfFcmUnits')), ('numOfBbUnits',TNumberOfItems), ('basebandUnits',prophy.array(SBaseBandUnit,bound='numOfBbUnits')), ('numOfValidLcrs',TNumberOfItems), ('localCellResources',prophy.array(SLcrInfo,bound='numOfValidLcrs')), ('testDedicatedState',TBoolean)]
class SLteRxTxResource(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('completeSicad',TBoolean), ('unitAddress',TBoardId), ('cpuId',TCpuId), ('cpId',TCpId), ('carrierResourceId',TCarrierResourceId), ('radioResourceType',ERadioResourceType), ('availability',EAvailability), ('connectivity',EConnectivity), ('numOfLcrIds',TNumberOfItems), ('associatedLcrIds',prophy.array(TLocalCellResId,bound='numOfLcrIds'))]
class SLteCarrierResources(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfTxResources',TNumberOfItems), ('txResource',prophy.array(SLteRxTxResource,bound='numOfTxResources')), ('numOfRxResources',TNumberOfItems), ('rxResource',prophy.array(SLteRxTxResource,bound='numOfRxResources'))]
class SLcrMap(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lcrId',TLocalCellResId), ('numOfBbUnitIds',TNumberOfItems), ('bbUnitIds',prophy.array(TBoardId,bound='numOfBbUnitIds'))]
class SHwMapping(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfLcrMapItems',TNumberOfItems), ('lcrMap',prophy.array(SLcrMap,bound='numOfLcrMapItems'))]
class SMappedLCRs(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('carrierResources',SLteCarrierResources), ('hwMapping',SHwMapping)]
class SLteCarrierResourcesChange(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfTxResources',TNumberOfItems), ('txResource',prophy.array(SLteRxTxResource,bound='numOfTxResources')), ('numOfRxResources',TNumberOfItems), ('rxResource',prophy.array(SLteRxTxResource,bound='numOfRxResources'))]
class SHwMappingChange(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfLcrMapItems',TNumberOfItems), ('lcrMap',prophy.array(SLcrMap,bound='numOfLcrMapItems'))]
class SMappedLCRsChange(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('carrierResourcesChange',SLteCarrierResourcesChange), ('hwMappingChange',SHwMappingChange)]
class SLcrCalibrationParametersId(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lcrId',TLocalCellResId), ('calibrationParametersId',prophy.u32)]
class SAdjGlobalENBID(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('pLMNIdentity',SPlmnId), ('lnBtsId',TOaMLnBtsId)]
class SAdjECGI(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('pLMNIdentity',SPlmnId), ('eutraCelId',TOaMEutraCelId)]
class SAdjServedCellInformation(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('phyCellId',TOaMLncelPhyCellId), ('cellId',SAdjECGI), ('lnadjlTac',TOaMLnadjlTac), ('broadcastPLMNs',SX2apBroadcastPLMNsItem), ('eUTRAModeInfo',UX2apEUTRAModeInfo)]
class SAdjServedCells(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('n',u16), ('elem',prophy.array(SAdjServedCellInformation,bound='n'))]
class SAdjServedCellToModifyInformation(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('oldEcgi',SAdjECGI), ('phyCellId',TOaMLncelPhyCellId), ('cellId',SAdjECGI), ('lnadjlTac',TOaMLnadjlTac), ('broadcastPLMNs',SX2apBroadcastPLMNsItem), ('eUTRAModeInfo',UX2apEUTRAModeInfo)]
class SAdjServedCellsToModify(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('n',u16), ('elem',prophy.array(SAdjServedCellToModifyInformation,bound='n'))]
class SAdjServedCellsToDelete(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('n',u16), ('elem',prophy.array(SAdjECGI,bound='n'))]
class SAdjGUGroupID(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('pLMNIdentity',SPlmnId), ('mmeGroupId',TOaMMmeGroupId)]
class SAdjGUGroupIDList(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('n',u8), ('elem',prophy.array(SAdjGUGroupID,bound='n'))]
class SBaseBandUnitStatus(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('bbUnitId',TBoardId), ('availability',EAvailability)]
class SUnmappedFspStatus(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfBbUnits',TNumberOfItems), ('basebandUnits',prophy.array(SBaseBandUnitStatus,bound='numOfBbUnits'))]
class SAdjCellConfigInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('enbId',SAdjGlobalENBID), ('servedCells',SAdjServedCells), ('gUGroupIDList',SAdjGUGroupIDList)]
class SAdjCellConfigDelta(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('servedCellsToAdd',SAdjServedCells), ('servedCellsToModify',SAdjServedCellsToModify), ('servedCellsToDelete',SAdjServedCellsToDelete), ('gUGroupIdToAddList',SAdjGUGroupIDList), ('gUGroupIdToDeleteList',SAdjGUGroupIDList)]
class SAllowedGUGroupID(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('plmnId',SPlmnId), ('mmeGroupId',TMmeGroupId)]
class STrackingAreaIdentity(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('plmnId',SPlmnId), ('tac',TOaMLncelTac)]
class SAdjGlobalEnbIdAndTai(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('neighborEnbId',SAdjGlobalENBID), ('neighborEnbSupportedTai',STrackingAreaIdentity)]
class SPciEarfcn(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('pci',TOaMPci), ('earfcnDL',TOaMEarfcnDL)]
class RROM_NetworkPlanReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('fileType',EFileType), ('lengthOfFileName',TNumberOfItems), ('fileName',prophy.array(u8,bound='lengthOfFileName'))]
class RROM_NetworkPlanResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('status',EStatusLte), ('resetRequest',EResetRequestType), ('lengthOfRejectedObjectsFileName',TNumberOfItems), ('rejectedObjectsFile',prophy.array(u8,bound='lengthOfRejectedObjectsFileName')), ('lengthOfCauseDescription',TNumberOfItems), ('cause',prophy.array(u8,bound='lengthOfCauseDescription'))]
class RROM_NetworkPlanValidateReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('fileType',EFileType), ('lengthOfNetworkPlanFileName',TNumberOfItems), ('networkPlanFile',prophy.array(u8,bound='lengthOfNetworkPlanFileName'))]
class RROM_NetworkPlanValidateResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('status',EStatusLte), ('lengthOfCauseDescription',TNumberOfItems), ('cause',prophy.array(u8,bound='lengthOfCauseDescription'))]
class RROM_HwConfigurationReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('configurationPhase',EConfigurationPhase), ('unmappedLCRs',SUnmappedLCRs), ('mappedLCRs',SMappedLCRs)]
class RROM_HwConfigurationResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('result',SMessageResult)]
class RROM_HwMappingInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('hwMapping',SHwMapping), ('gtpuDataPathSupervision',STransportLayerAddress)]
class RROM_HwConfigurationChangeReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('configurationPhase',EConfigurationPhase), ('unmappedLCRs',SUnmappedFspStatus), ('mappedLCRs',SMappedLCRsChange), ('tmpName',TNumberOfItems), ('calibrationParametersIds',prophy.array(SLcrCalibrationParametersId,bound='tmpName'))]
class RROM_HwConfigurationChangeResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('result',SMessageResult)]
class RROM_HwMappingChangeInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('hwMapping',SHwMappingChange), ('gtpuDataPathSupervision',STransportLayerAddress)]
class RROM_RegisterReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('clientAddress',TAaSysComSicad), ('indicationType',EIndicationType)]
class RROM_RegisterResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('result',SMessageResult)]
class RROM_CellStateInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('cellSetupResult',ECellSetupResult)]
class RROM_CellStateChangeReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('cellOperationalState',ECellOperationalState)]
class RROM_CellStateChangeResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('result',SMessageResult)]
class RROM_AdjacentCellConfigReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('enbcTransactionId',TTransactionID), ('neighborCellConfig',ENeighborCellConfig), ('neighborCellConfigInfo',SAdjCellConfigInfo), ('neighborCellConfigDelta',SAdjCellConfigDelta), ('ipAddress',STransportLayerAddress)]
class RROM_AdjacentCellConfigResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('enbcTransactionId',TTransactionID), ('messageResult',SMessageResult), ('mocId',TMoc)]
class RROM_NetworkPlanUploadResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('result',SMessageResult), ('lengthOfNetworkPlanFileName',TNumberOfItems), ('deltaNetworkPlanFile',prophy.array(u8,bound='lengthOfNetworkPlanFileName'))]
class RROM_NetworkPlanUpdateInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lengthOfNetworkPlanFileName',TNumberOfItems), ('deltaNetworkPlanFile',prophy.array(u8,bound='lengthOfNetworkPlanFileName'))]
class RROM_PlanActivationCompleteInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('status',EStatusLte), ('lengthOfAdditionalInfoDescription',TNumberOfItems), ('additionalInfo',prophy.array(u8,bound='lengthOfAdditionalInfoDescription'))]
class RROM_MMEConfigReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('enbcTransactionId',TTransactionID), ('linkId',TL3LinkId), ('lnMmeId',TOaMLnMmeId), ('lengthOfMmeName',TNumberOfItems), ('mMEName',prophy.array(u8,bound='lengthOfMmeName')), ('lengthOfServedPLMNs',TNumberOfItems), ('servedPLMNs',prophy.array(SPlmnId,bound='lengthOfServedPLMNs')), ('relativeMMECapacity',TRelativeMMECapacity), ('tmpName',TNumberOfItems), ('allowedGUGroupIds',prophy.array(SAllowedGUGroupID,bound='tmpName')), ('secondaryIpAddress',STransportLayerAddress)]
class RROM_MMEConfigResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('enbcTransactionId',TTransactionID), ('messageResult',SMessageResult), ('linkId',TL3LinkId), ('lnMmeId',TOaMLnMmeId)]
class RROM_StartDlTestModelReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('testModelId',ETestModelId), ('localCellResId',TLocalCellResId), ('earfcnDL',TOaMEarfcnDL), ('phyCellId',TPhyCellId)]
class RROM_StartDlTestModelResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('result',SMessageResult)]
class RROM_StopDlTestModelReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId)]
class RROM_StopDlTestModelResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('result',SMessageResult)]
class RROM_StartUlTestModelReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('referenceChannelNumber',EReferenceChannelNumber), ('harqUsed',TBoolean), ('localCellResId',TLocalCellResId), ('reportingTimeInterval',TReportingTimeInterval), ('earfcnUL',TOaMEarfcnUL), ('resourceBlockOffset',TResourceBlock), ('digitalOutputEnabled',TBoolean), ('ulTestModelDigitalOutputParams',SUlTestModelsDigitalOutputParams), ('hstConfig',EHstConfiguration), ('resourceIndexCqi',TResourceIndexCqi), ('dlInterferenceEnable',TBoolean)]
class RROM_StartUlTestModelResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('result',SMessageResult)]
class RROM_StopUlTestModelReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId)]
class RROM_StopUlTestModelResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('result',SMessageResult)]
class RROM_ThroughputMeasurementReportInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('resultStatus',EStatusLte), ('throughputResult',TThroughputResult), ('resultCounters',SResultCounters)]
class RROM_StartUlCtrlChannelMeasReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('measType',EUlCtrlChannelMeasType), ('reportingTimeInterval',TReportingTimeInterval), ('receptionSubframe',TSubframes), ('expectionSubframe',TSubframes), ('prachParams',SUlCtrlChannelPrachParams), ('pucchAckParams',SUlCtrlChannelPucchAckParams), ('pucchCqiParams',SUlCtrlChannelPucchCqiParams), ('puschHarqAckParams',SUlCtrlChannelPuschHarqAckParams), ('earfcnUL',TOaMEarfcnUL), ('rootSeqIndex',TOaMRootSeqIndex), ('prachCS',TOaMPrachCS), ('prachHsFlag',TOaMPrachHsFlag), ('phyCellId',TPhyCellId)]
class RROM_StartUlCtrlChannelMeasResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('result',SMessageResult)]
class RROM_StopUlCtrlChannelMeasReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId)]
class RROM_StopUlCtrlChannelMeasResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('result',SMessageResult)]
class RROM_UlCtrlChannelMeasReportInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('resultStatus',EStatusLte), ('measType',EUlCtrlChannelMeasType), ('ulCtrlChannelResultCounters',SUlCtrlChannelMeasCounters), ('ulCtrlChannelMeasCountersMissedPrach',SUlCtrlChannelMeasCountersMissedPrach)]
class RROM_StartRfLoopTestReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('phase',ERfLoopTestPhase), ('txResource',prophy.bytes(size=MAX_NUM_OF_TX_RESOURCES)), ('rxResource',prophy.bytes(size=MAX_NUM_OF_RX_RESOURCES)), ('reportingTimeInterval',TReportingTimeInterval), ('txPowerScaling',TTxPowerScaling), ('maxTxPower',TMaxTxPower), ('txPowerLoop',TPowerLoop)]
class RROM_StartRfLoopTestResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('phase',ERfLoopTestPhase), ('result',SMessageResult)]
class RROM_StopRfLoopTestReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId)]
class RROM_StopRfLoopTestResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('result',SMessageResult)]
class RROM_NetworkPlanStorageInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lengthOfNetworkPlanFileName',TNumberOfItems), ('networkPlanFile',prophy.array(u8,bound='lengthOfNetworkPlanFileName'))]
class RROM_ShutdownReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId)]
class RROM_ShutdownResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('result',SMessageResult)]
class RROM_TraceControlAvailInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('rromMgmtSicad',TAaSysComSicad), ('tmpName',TNumberOfItems), ('supportedTracingFunctionalites',prophy.array(ESupportedTracingFunctionalities,bound='tmpName'))]
class RROM_AntennaCarrierCalibrationSetupReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('calibrationEnabled',TBoolean), ('calibrationPeriod',prophy.u32), ('rxCalibrationStartOffset',prophy.u32), ('rxCalibrationEndOffset',prophy.u32), ('txCalibrationStartOffset',prophy.u32), ('txCalibrationEndOffset',prophy.u32), ('calibrationAntennaCarrier',prophy.u32), ('calibrationSets',prophy.bytes(size=8))]
class RROM_AntennaCarrierCalibrationSetupResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('result',SMessageResult)]
class RROM_ConfigParamsChangeReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('numOfRxPowerScaling',TNumberOfItems), ('rxPowerScaling',prophy.array(TRxPowerScaling,bound='numOfRxPowerScaling')), ('txPowerScaling',TTxPowerScaling), ('calibrationParametersId',prophy.u32), ('calibrationSetupAddress',TAaSysComSicad)]
class RROM_ConfigParamsChangeResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('localCellResId',TLocalCellResId), ('result',SMessageResult)]
class RROM_TrswConfigurationReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tmpName',TNumberOfItems), ('candUPlaneAddresses',prophy.array(SCandUPlaneIpAddresses,bound='tmpName')), ('transportNetworkIdMainOperator',TTransportNetworkId), ('dscp',TDscp), ('omsIpAddress',STransportLayerAddress), ('actIpv6',TBoolean), ('localIpAddress',STransportLayerAddress)]
class RROM_TrswConfigurationResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('result',SMessageResult)]
class RROM_TrswConfigurationChangeReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tmpName',TNumberOfItems), ('candUPlaneAddresses',prophy.array(SCandUPlaneIpAddresses,bound='tmpName')), ('omsIpAddress',STransportLayerAddress)]
class RROM_TrswConfigurationChangeResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('result',SMessageResult)]
class RROM_MobilitySettingsChangeReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TOaMEutraCelId), ('neighbourECGI',SAdjECGI), ('cellIndOffNeighDelta',TOaMCellIndOffNeighDelta)]
class RROM_MobilitySettingsChangeResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TOaMEutraCelId), ('result',SMessageResult)]
