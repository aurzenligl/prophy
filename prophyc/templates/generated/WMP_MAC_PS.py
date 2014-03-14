import prophy 
from externals import *
from OAM_MERGED import *
from globals import *


MAX_NUM_OF_RESOURCE_GROUPS = 4
MAX_NUM_OF_NCELLABS = 1
MAX_MSG_TYPE_TAG = 17
MAC_T_PDCCH_UL_DL_PRIO_MAX = 99
MAC_T_PDCCH_UL_DL_PRIO_MIN = 0

TPdcchUlDlPrio = prophy.u32
TUlsSidVol = prophy.u32
TDlsGbrRlc = prophy.u32
TDlsGbrMac = prophy.u32
TUlsGbrRlc = prophy.u32
TUlsGbrMac = prophy.u32
TDrxMaxLongCycle = prophy.u32
TUlsMinRbPerUe = prophy.u32
TUlsMinTbs = prophy.u32
TReCqiLimit = prophy.u8
TMeasGapOffset = prophy.u32
THarqMaxTrUl = prophy.u32
TDedicRaPreExpT = prophy.u32
TICqiPmi = prophy.u32
TIRi = prophy.u32
TCqiPerSbCycK = prophy.u32
TCellResourceGroupId = prophy.u32
TSCellResourceGroupId = prophy.u32
TSCellServCellIndex = prophy.u32

class ETransmMode(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETransmMode_NotDefined',0), ('ETransmMode_SingleAntennaPort_Port0',1), ('ETransmMode_TransmitDiversity',2), ('ETransmMode_OpenLoopSpatialMultiplexing',3), ('ETransmMode_ClosedLoopSpatialMultiplexing',4), ('ETransmMode_MultiUserMIMO',5), ('ETransmMode_ClosedLoopRank1Precoding',6), ('ETransmMode_SingleAntennaPort_Port5',7), ('ETransmMode_DualBeamforming_Port7_8',8), ('ETransmMode_TM9',9)]
class ECellType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ECellType_Normal',0), ('ECellType_Micro',1), ('ECellType_Macro',2)]
class EDeploymentInformation(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EDeploymentInformation_Undefined',0), ('EDeploymentInformation_2Pipe',2), ('EDeploymentInformation_4Pipe',4), ('EDeploymentInformation_8Pipe',8)]
class ECqiAperMode(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ECqiAperMode_m12',0), ('ECqiAperMode_m20',1), ('ECqiAperMode_m22',2), ('ECqiAperMode_m30',3), ('ECqiAperMode_m31',4)]
class ECqiPerMode(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ECqiPerMode_Wideband',0), ('ECqiPerMode_Wideband_And_Subband',1), ('ECqiPerMode_WidebandSubmode1',2), ('ECqiPerMode_WidebandSubmode2',3)]
class ETmSettingWithBf(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETmSettingWithBf_fixedTm3WithBf',0), ('ETmSettingWithBf_followDlMimoMode',1)]
class EDrxConfigType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EDrxConfigType_NotDefined',0), ('EDrxConfigType_Activation',1), ('EDrxConfigType_Deactivation',2), ('EDrxConfigType_Reconfiguration',3), ('EDrxConfigType_ConfigCompleted',4)]
class ECqiPerEnable(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ECqiPerEnable_Disabled',0), ('ECqiPerEnable_Enabled',1)]
class ECqiPerSbPeriodicityFactorR10(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ECqiPerSbPeriodicityFactorR10_n2',0), ('ECqiPerSbPeriodicityFactorR10_n4',1)]
class ECqiPerSimulAck(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ECqiPerSimulAck_Disabled',0), ('ECqiPerSimulAck_Enabled',1)]
class EMeasGapOffset(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EMeasGapOffset_None',0), ('EMeasGapOffset_measGapPattern0',1), ('EMeasGapOffset_measGapPattern1',2)]
class EDelayTarget(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EDelayTarget_NotDefined',0), ('EDelayTarget_50ms',50), ('EDelayTarget_60ms',60), ('EDelayTarget_70ms',70), ('EDelayTarget_80ms',80), ('EDelayTarget_90ms',90), ('EDelayTarget_100ms',100), ('EDelayTarget_110ms',110), ('EDelayTarget_120ms',120), ('EDelayTarget_130ms',130), ('EDelayTarget_140ms',140), ('EDelayTarget_150ms',150), ('EDelayTarget_200ms',200), ('EDelayTarget_250ms',250), ('EDelayTarget_300ms',300), ('EDelayTarget_350ms',350), ('EDelayTarget_400ms',400), ('EDelayTarget_450ms',450), ('EDelayTarget_500ms',500), ('EDelayTarget_550ms',550), ('EDelayTarget_600ms',600), ('EDelayTarget_650ms',650), ('EDelayTarget_700ms',700), ('EDelayTarget_750ms',750), ('EDelayTarget_800ms',800), ('EDelayTarget_850ms',850), ('EDelayTarget_900ms',900), ('EDelayTarget_950ms',950), ('EDelayTarget_1000ms',1000)]
class EMaxNumOfLayers(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EMaxNumOfLayers_NotDefined',0), ('EMaxNumOfLayers_2',2), ('EMaxNumOfLayers_4',4), ('EMaxNumOfLayers_8',8)]

class SExtendedDrxParameters(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('applyOutOfSyncState',EOaMApplyOutOfSyncState), ('stInactFactor',TOaMStInactFactor)]
class SRadioLinkFailureParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('rlpDetMaxTimeDl',TOaMRlpDetMaxTimeDl), ('rlpDetMaxNoDl',TOaMRlpDetMaxNoDl), ('rlpDetEndNoDl',TOaMRlpDetEndNoDl), ('rlpDetMaxNUl',TOaMRlpDetMaxNUl), ('rlpDetEndNUl',TOaMRlpDetEndNUl)]
class SRateCappingParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('rcEnableDl',TOaMRcEnableDl), ('rcAmbrMgnDl',SOaMRcAmbrMgnDl), ('rcAvCstDl',TOaMRcAvCstDl), ('rcEnableUl',TOaMRcEnableUl), ('rcAmbrMgnUl',SOaMRcAmbrMgnUl), ('rcAvCstUl',TOaMRcAvCstUl)]
class SUlpcIawConfig(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ulpcCEBalanceIAw',TOaMUlpcCEBalanceIAw), ('ulpcMinWaitForPc',TOaMUlpcMinWaitForPc), ('ulpcMinQualIAw',TOaMUlpcMinQualIAw), ('ulpcRefPwrIAw',TOaMUlpcRefPwrIAw), ('ulpcRssiMaxIAw',SOaMUlpcRssiMaxIAw)]
class SUlPCCellParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ulpcRarespTpc',TOaMUlpcRarespTpc), ('dFpucchF1',EOaMDFpucchF1), ('dFpucchF1b',EOaMDFpucchF1b), ('dFpucchF2',EOaMDFpucchF2), ('dFpucchF2a',EOaMDFpucchF2a), ('dFpucchF2b',EOaMDFpucchF2b), ('ulpcRssiMin',TOaMUlpcRssiMin), ('ulpcRssiMax',TOaMUlpcRssiMax), ('ulpcSinrMin',TOaMUlpcSinrMin), ('ulpcSinrMax',TOaMUlpcSinrMax), ('ulpcWfPucchcell',TOaMUlpcWfPucchcell), ('ulpcWfPucchUe',TOaMUlpcWfPucchUe), ('ulpcWfPuschcell',TOaMUlpcWfPuschcell), ('ulpcWfPuschUe',TOaMUlpcWfPuschUe), ('ulpcWfSrscell',TOaMUlpcWfSrscell), ('ulpcWfSrsUe',TOaMUlpcWfSrsUe), ('ulpcCumpucchmin',TOaMUlpcCumpucchmin), ('ulpcCumpucchmax',TOaMUlpcCumpucchmax), ('ulpcCumpuschmin',TOaMUlpcCumpuschmin), ('ulpcCumpuschmax',TOaMUlpcCumpuschmax), ('ulpcReadPeriod',SOaMUlpcReadPeriod), ('ulpcSchavgtcont',TOaMUlpcSchavgtcont), ('ulpcSchavgtdisc',TOaMUlpcSchavgtdisc), ('ulpcCchavgtcont',TOaMUlpcCchavgtcont), ('ulpcCchavgtdisc',TOaMUlpcCchavgtdisc), ('actUlpcMethod',EOaMActUlpcMethod), ('p0NominalPusch',TOaMP0NomPusch), ('p0NomPucch',TOaMP0NomPucch), ('ulpcIniPrePwr',EOaMUlpcIniPrePwr), ('deltaPreambleMsg3',prophy.i32), ('ulpcAlpha',EOaMUlpcAlpha), ('ulpcPucchConfig',SOaMUlpcPucchConfig), ('ulpcPuschConfig',SOaMUlpcPuschConfig), ('ulpcIawConfig',SUlpcIawConfig)]
class STtiBundlingParameters(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ttiBundlingBlerThreshold',SOaMTtiBundlingBlerThreshold), ('ttiBundlingSinrThreshold',SOaMTtiBundlingSinrThreshold), ('ttiBundlingBlerTarget',SOaMTtiBundlingBlerTarget), ('ttiBundlingCStepUp',TOaMTtiBundlingCStepUp), ('ttiBundlingDeltaCini',TOaMTtiBundlingDeltaCini), ('ttiBundlingDeltaCmin',TOaMTtiBundlingDeltaCmin), ('ttiBundlingDeltaCmax',TOaMTtiBundlingDeltaCmax)]
class SPuschHoppingInformation(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('hopBwPusch',TOaMLnbtsHopBwPusch), ('hopModePusch',EOaMHopModePusch), ('hopTypePusch',prophy.u32), ('TPuschHoppingEnable',TBoolean), ('puschHopOffset',TOaMPuschHopOffset)]
class SUlMuMimoParameters(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('actUlMuMimo',TBoolean), ('ulMuMimoSinrThreshold',prophy.i32), ('ulMuMimoOrthThreshold',prophy.u32)]
class SCommonCellParamsWmpTdd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('maxNumUeDlDwPTS',TOaMMaxNumUeDlDwPTS), ('nSrsDtx',TOaMNSrsDtx), ('nSrsRec',TOaMNSrsRec), ('dlsSchedType',EOaMDlsSchedType), ('ulsSrelFilterCst',TOaMUlsSrelFilterCst), ('dlsNgap',EOaMDlsNgap), ('dlsDciCch',TBoolean), ('puschHoppingInformation',SPuschHoppingInformation), ('dlsFdAlg',EOaMDlsFdAlg), ('ulMuMimoParameters',SUlMuMimoParameters)]
class SCommonCellParamsWmp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('iniPrbsUl',TOaMIniPrbsUl), ('maxNumPrbSr',TOaMMaxNumPrbSr), ('dlsTputAvgT',TOaMDlsTputAvgT), ('ulsTputAvgT',TOaMUlsTputAvgT), ('maxNumUeDl',TOaMMaxNumUeDl), ('maxNumUeUl',TOaMMaxNumUeUl), ('psd0',TTxPower), ('psdMimo',TTxPower), ('dl64QamEnable',TOaMDl64QamEnable), ('enableDl16Qam',TOaMEnableDl16Qam), ('dlsUsePartPrb',EOaMDlsUsePartPrb), ('ilMinDatvolUl',TOaMIlMinDatvolUl), ('ilReacTimerUl',TOaMIlReacTimerUl), ('enablePhichCtrlUl',TOaMEnablePhichCtrlUl), ('taOffsetSchedMgn',TOaMTaOffScheMarg), ('taCmdMaxRetry',TOaMTaCmdMaxRetry), ('taTimerMargin',TOaMTaTimerMargin), ('nCqiDtx',TOaMNCqiDtx), ('nCqiRec',TOaMNCqiRec), ('redBwEnDl',TOaMRedBwEnDl), ('redBwMaxRbDl',SOaMRedBwMaxRbDl), ('redBwRpaEnUl',TOaMRedBwRpaEnUl), ('radioLinkFailureParams',SRadioLinkFailureParams), ('rateCappingParams',SRateCappingParams), ('ulPCCellParams',SUlPCCellParams), ('dlsFdPfSchAvgC',TOaMDlsFdPfSchAvgC), ('qciWeightAlignDl',TOaMQciWeightAlignDl), ('ulsFdPrbAssignAlg',EOaMUlsFdPrbAssignAlg), ('qciWeightAlignUl',TOaMQciWeightAlignUl), ('actModulationSchemeUL',EOaMActModulationSchemeUL), ('ulsSchedMethod',EOaMUlsSchedMethod), ('ulsInterferenceCst',TOaMUlsInterferenceCst), ('ulsNumSchedAreaUl',TOaMUlsNumSchedAreaUl), ('ulsTxPowDenConst',TOaMUlsTxPowDenConst), ('extendedDrxParameters',SExtendedDrxParameters), ('primaryPLMNId',SPlmnId), ('ttiBundlingParameters',STtiBundlingParameters), ('actCsiDroppingSolution',EOaMActCsiDroppingSolution), ('ulsPuschMask',SArrayOfOaMUlsPuschMask), ('redBwRbUlConfig',SOaMRedBwRbUlConfig), ('commonCellParamsWmpTdd',SCommonCellParamsWmpTdd)]
class SMcsParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('raLargeMcsUl',TOaMRaLargeMcsUl), ('raLargeVolUl',TOaMRaLargeVolUl), ('raSmallMcsUl',TOaMRaSmallMcsUl), ('raSmallVolUl',EOaMRaSmallVolUl), ('maxCrSibDl',TOaMMaxCrSibDl), ('maxCrPgDl',TOaMMaxCrPgDl), ('maxCrRaDl',TOaMMaxCrRaDl), ('maxCrRa4Dl',TOaMMaxCrRa4Dl), ('iniMcsDl',TOaMIniMcsDl), ('iniMcsUl',TOaMIniMcsUl)]
class SPdcchParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('pdcchAggSib',TOaMPdcchAggSib), ('pdcchAggRaresp',TOaMPdcchAggRaresp), ('pdcchAggPaging',TOaMPdcchAggPaging), ('pdcchAggPreamb',TOaMPdcchAggPreamb), ('pdcchAggMsg4',TOaMPdcchAggMsg4), ('enableAmcPdcch',TOaMEnableAmcPdcch), ('pdcchAggDefUe',EOaMPdcchAggDefUe), ('pdcchCqiAvg',TOaMPdcchCqiAvg), ('pdcchCqiShift',SOaMPdcchCqiShift), ('pdcchOlComp',TOaMPdcchOlComp), ('pdcchClComp',TOaMPdcchClComp), ('pdcchCqiHist',TOaMPdcchCqiHist), ('enableLowAgg',TOaMEnableLowAgg), ('pdcchLowAggTh',TOaMPdcchLowAggTh), ('pdcchAlpha',TOaMPdcchAlpha), ('pdcchUlDlBal',TOaMPdcchUlDlBal), ('pdcchUlDlPrio',prophy.bytes(size=MAX_MSG_TYPE_TAG)), ('enablePcPdcch',TOaMEnablePcPdcch), ('pdcchPcBoost',TOaMPdcchPcBoost), ('pdcchPcRed',TOaMPdcchPcRed), ('pdcchPcReloc',TOaMPdcchPcReloc), ('actLdPdcch',TBoolean), ('actPdcchLoadGen',TOaMActPdcchLoadGen), ('pdcchLoadLevel',SOaMPdcchLoadLevel), ('pdcchLoadPsdOffset',SOaMPdcchLoadPsdOffset)]
class SSchedulingWeightParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('prioHarqDl',TOaMPrioHarqDl), ('prioSrbDl',TOaMPrioSrbDl), ('prioHarqUl',TOaMPrioHarqUl), ('prioSrUl',TOaMPrioSrUl), ('prioSrbUl',TOaMPrioSrbUl)]
class SLinkAdaptConfParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dlamcEnable',TOaMDlamcEnable), ('dlOlqcEnable',TOaMDlOlqcEnable), ('dlOlqcDeltaCqiIni',TOaMDlOlqcDeltaCqiIni), ('dlOlqcDeltaCqiMax',TOaMDlOlqcDeltaCqiMax), ('dlOlqcDeltaCqiMin',TOaMDlOlqcDeltaCqiMin), ('dlOlqcDeltaCqiStepUp',TOaMDlOlqcDeltaCqiStepUp), ('dlTargetBler',SOaMDlTargetBler), ('dlamcCqiDef',TOaMDlamcCqiDef), ('dlamcTHistCqi',TOaMDlamcTHistCqi), ('cqiCompSmRi1Ol',TOaMCqiCompSmRi1Ol), ('cqiCompTdRi2Ol',TOaMCqiCompTdRi2Ol), ('cqiCompSmRi1Cl',TOaMCqiCompSmRi1Cl), ('cqiCompTdRi2Cl',TOaMCqiCompTdRi2Cl), ('ulTargetBler',TOaMUlTargetBler), ('ulamcUpdowngrF',TOaMUlamcUpdowngrF), ('ulamcDeltaCmax',TOaMUlamcDeltaCmax), ('ulamcDeltaCmin',TOaMUlamcDeltaCmin), ('ulamcDeltaCini',TOaMUlamcDeltaCini), ('ulamcCStepUp',TOaMUlamcCStepUp), ('ulamcAllTbEn',TOaMUlamcAllTbEn), ('ulamcHistMcsT',TOaMUlamcHistMcsT), ('ulamcInactT',TOaMUlamcInactT), ('ulamcSwitchPer',TOaMUlamcSwitchPer), ('ulatbPhrAvgF',TOaMUlatbPhrAvgF), ('ulatbEventPer',TOaMUlatbEventPer), ('actUlLnkAdp',EOaMActUlLnkAdp), ('eUlLaAtbPeriod',SOaMEUlLaAtbPeriod), ('eUlLaPrbIncDecFactor',SOaMEUlLaPrbIncDecFactor), ('eUlLaBlerAveWin',SOaMEUlLaBlerAveWin), ('eUlLaDeltaMcs',SOaMEUlLaDeltaMcs), ('eUlLaLowPrbThr',SOaMEUlLaLowPrbThr), ('eUlLaLowMcsThr',SOaMEUlLaLowMcsThr), ('actOlLaPdcch',TOaMActOlLaPdcch), ('pdcchHarqTargetBler',SOaMPdcchHarqTargetBler), ('fUlLAAtbTrigThr',SOaMFUlLAAtbTrigThr)]
class SMimoCtrlParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('mimoOlCqiComp',TOaMMimoOlCqiComp), ('mimoOlCqiAvg',TOaMMimoOlCqiAvg), ('mimoOlRiAvg',TOaMMimoOlRiAvg), ('mimoClCqiComp',TOaMMimoClCqiComp), ('mimoClCqiAvg',TOaMMimoClCqiAvg), ('mimoClRiAvg',TOaMMimoClRiAvg), ('mimoClConfig',SOaMMimoClConfig), ('mimoOlConfig',SOaMMimoOlConfig)]
class SConvVoiceParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('actConvVoice',TOaMActConvVoice), ('actDlsVoicePacketAgg',TOaMActDlsVoicePacketAgg), ('actDlsOldtc',TOaMActDlsOldtc), ('dlsOldtcTarget',SOaMDlsOldtcTarget), ('dlsOldtcStepUp',TOaMDlsOldtcStepUp), ('ulsMaxPacketAgg',TOaMUlsMaxPacketAgg), ('ulsVoipOverhead',TOaMUlsVoipOverhead)]
class SGbrCongestionParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('gbrCongHandling',EOaMGbrCongHandling), ('maxGbrTrafficLimit',TOaMMaxGbrTrafficLimit), ('addGbrTrafficRrHo',TOaMAddGbrTrafficRrHo), ('addGbrTrafficTcHo',TOaMAddGbrTrafficTcHo)]
class SPRSInfoParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('actOtdoa',TOaMActOtdoa), ('prsConfigurationIndex',SOaMPrsConfigurationIndex), ('prsNumDlFrames',SOaMPrsNumDlFrames)]
class SSRSTriggerParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ulsNumConsecutivePhr',TOaMUlsNumConsecutivePhr), ('srsConfiguration',SOaMSrsConfiguration)]
class SBeamformingCtrlParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sectorBeamformingMode',EOaMDlSectorBeamformingMode), ('sectorBfWeightforAntenna',prophy.bytes(size=NUM_OF_ANTENNAGROUPS)), ('bfCqiThUp',prophy.u32), ('bfCqiThDown',prophy.u32), ('bfRankThUp',prophy.u32), ('bfRankThDown',prophy.u32), ('timeChInfoValid',EOaMTimeChInfoValid), ('actBfFallback',TBoolean), ('mimoBfdlCqiComp',prophy.u32), ('mimoBfCqiAvg',prophy.u32), ('mimoBfdlRiAvg',prophy.u32), ('deploymentInformation',EDeploymentInformation), ('mimoBfslCqiThU',prophy.u32), ('mimoBfslCqiThD',prophy.u32), ('sectorBeamAggrGain',prophy.u32)]
class STransmModeParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('actTmSwitch',TOaMActTmSwitch), ('prohibitTimerTmSwitch',EOaMProhibitTimerTmSwitch), ('tm7to3CqiTh',SOaMTm7to3CqiTh), ('tm3to7CqiTh',SOaMTm3to7CqiTh), ('tm8to3CqiTh',SOaMTm8to3CqiTh), ('tm3to8CqiTh',SOaMTm3to8CqiTh)]
class SEicicAbsPattern(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('absPatternLow',prophy.u32), ('absPatternHigh',prophy.u8), ('absShift',prophy.u16)]
class SEicicParameters(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellType',ECellType), ('reCqiLimit',TReCqiLimit), ('reCqiThreshold',TReCqiLimit), ('cellAbsPattern',SEicicAbsPattern), ('numberOfNcellAbsPattern',u8), ('nCellAbsPattern',prophy.array(SEicicAbsPattern,bound='numberOfNcellAbsPattern'))]
class SMuMimoParameters(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('actTm8MuMimo',TBoolean), ('tm8MuMimoCqiThd',TOaMTm8MuMimoCqiThd), ('tm8MuMimoCorrThd',TOaMTm8MuMimoCorrThd)]
class SUplinkPcCommonR10(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('deltaFPucchF3r10',EOaMDeltaFPucchF3r10), ('deltaFPucchF1bCSr10',EOaMDeltaFPucchF1bCSr10)]
class SDlCarrierAggrParamsPCell(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCellIdScell',TOaMLnCelId), ('uplinkPcCommonR10',SUplinkPcCommonR10)]
class SDlCarrierAggrParamsSCell(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCellIdPcell',TOaMLnCelId), ('sCellDeactivationTimerEnb',EOaMSCellDeactivationTimereNB), ('disableSCellPDCCHOlLa',TOaMDisableSCellPDCCHOlLa)]
class SDlCarrierAggrParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('caSchedFairFact',TOaMCaSchedFairFact), ('sCellActivationCyclePeriod',EOaMSCellActivationCyclePeriod), ('sCellActivationMethod',EOaMSCellActivationMethod), ('sCellpCellHARQFdbkUsage',EOaMSCellpCellHARQFdbkUsage), ('dlCarrierAggrParamsPCell',SDlCarrierAggrParamsPCell), ('dlCarrierAggrParamsSCell',SDlCarrierAggrParamsSCell)]
class SCsiRsConfiguration(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfCsiRsAntennaPorts',EOaMNumOfCsiRsAntennaPorts), ('csiRsResourceConf',EOaMCsiRsResourceConf), ('csiRsSubfrConf',TOaMCsiRsSubfrConf), ('csiRsPwrOffset',TOaMCsiRsPwrOffset), ('actCsiRsSubFNonTM9Sch',TOaMActCsiRsSubFNonTM9Sch)]
class SSuperCellParSet(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('subCellSwitchUlSinrHys',TOaMSubCellSwitchUlSinrHys), ('subCellUlSinrAvgT',TOaMSubCellUlSinrAvgT), ('candSubCellUlSinrOffset',prophy.u32), ('remCandSubCellUlSinrHys',prophy.u32), ('repCandSubCellUlSinrHys',prophy.u32)]
class SSuperCellParameters(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('actSuperCell',TOaMActSuperCell), ('superCellParSet',SSuperCellParSet)]
class SWmpCellContainer(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfCellsPerBBPool',prophy.u32), ('commonCellParamsWmp',SCommonCellParamsWmp), ('mcsParams',SMcsParams), ('pdcchParams',SPdcchParams), ('schedulingWeightParams',SSchedulingWeightParams), ('linkAdaptConfParams',SLinkAdaptConfParams), ('mimoCtrlParams',SMimoCtrlParams), ('convVoiceParams',SConvVoiceParams), ('enaDrxRepGra',TOaMEnaDrxRepGra), ('enaDrxWactUl',TOaMEnaDrxWactUl), ('enaDrxWactDl',TOaMEnaDrxWactDl), ('enaDrxWcqiDl',TOaMEnaDrxWcqiDl), ('actDrx',TOaMActDrx), ('drxMaxLongCycle',TDrxMaxLongCycle), ('dlRsBoost',EOaMDlRsBoost), ('dlPcfichBoost',TOaMDlPcfichBoost), ('dlPhichBoost',TOaMDlPhichBoost), ('dlsSciCch',TBoolean), ('ulsMinTbs',TUlsMinTbs), ('ulsMinRbPerUe',TUlsMinRbPerUe), ('actEnhAcAndGbrServices',TBoolean), ('gbrCongestionParams',SGbrCongestionParams), ('prsInfoParams',SPRSInfoParams), ('actDLCAggr',TBoolean), ('actFastMimoSwitch',TOaMActFastMimoSwitch), ('cellResourceSharingMode',EOaMCellResourceSharingMode), ('crgSkipThreshold',EOaMCrgSkipThreshold), ('sharePerResourceGroup',prophy.bytes(size=MAX_NUM_OF_RESOURCE_GROUPS)), ('sdlEnable',TBoolean), ('srsTriggerParams',SSRSTriggerParams), ('bfCtrlParams',SBeamformingCtrlParams), ('transmModeParams',STransmModeParams), ('eIcicParams',SEicicParameters), ('muMimoParameters',SMuMimoParameters), ('dlCarrierAggrParams',SDlCarrierAggrParams), ('csiRsConfiguration',SCsiRsConfiguration), ('superCellParameters',SSuperCellParameters), ('scellTmSettingWithBf',ETmSettingWithBf)]
class SCqiParamsWmp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cqiAperPollT',TOaMCqiAperPollT), ('cqiAperEnable',TOaMCqiAperEnable)]
class SWmpUserContainer(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cqiParamsWmp',SCqiParamsWmp), ('harqMaxTrDl',TOaMHarqMaxTrDl), ('harqMaxTrUl',THarqMaxTrUl), ('tm8SupportFlag',TBoolean), ('ttiBmMeasActivate',TBoolean), ('measGapStopRequired',TBoolean), ('gapPattern',EMeasGapOffset), ('measGapOffset',TMeasGapOffset), ('ueInactivityTimer',TOaMInactivityTimer), ('tInactiveUtraAnr',prophy.u32), ('dedicRaPreExpT',TDedicRaPreExpT), ('oldCrntiInTheSameCell',TCrnti), ('intentionalContentionbasedRaEnabled',TBoolean), ('cellResourceGroupId',TCellResourceGroupId), ('padding',prophy.u32), ('maxNumOfLayers',EMaxNumOfLayers), ('reserved1',prophy.u32), ('reserved2',prophy.u32), ('reserved3',prophy.u32)]
class SWmpSrbInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dlSchedulingPriority',TSchedulingWeight)]
class SWmpRbInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dlSchedulingPriority',TSchedulingWeight), ('schedulWeight',TSchedulingWeight), ('qci',prophy.u32), ('dlsBucketSizeDuration',EOaMLnbtsQciTab5SchedulBSD), ('dlsGbrRlc',TDlsGbrRlc), ('dlsGbrMac',TDlsGbrMac), ('dlsDelayTarget',EDelayTarget), ('ulsBucketSizeDuration',EOaMLnbtsQciTab5SchedulBSD), ('ulsGbrRlc',TUlsGbrRlc), ('ulsGbrMac',TUlsGbrMac), ('ulsDelayTarget',EDelayTarget), ('ulsSidVol',TUlsSidVol), ('congestionWeight',prophy.u32), ('ulSchedulingPriority',TSchedulingWeight), ('reserved1',prophy.u32), ('reserved2',prophy.u32)]
class SCqiParamsScellWmp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cqiAperPollT',TOaMCqiAperPollT), ('cqiAperEnable',TOaMCqiAperEnable)]
class STmSwitchScell(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sCellServCellIndex',TSCellServCellIndex), ('newTransmMode',ETransmMode)]
class SWmpUlResCtrlParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cqiParamsWmp',SCqiParamsWmp), ('newTransmMode',ETransmMode), ('cqiParamsScellWmp',SCqiParamsScellWmp), ('tmSwitchScell',STmSwitchScell)]
class SSib8Info(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sib8TimePosition',prophy.u32), ('sib8TimeLength',prophy.u32), ('longCodeState1XRTTPosition',prophy.u32), ('sib8SizeWithTime',TL3MsgSize), ('sib8DataWithTime',prophy.array(u8,bound='sib8SizeWithTime'))]
class SSystemInfoContainerWmp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sib8SyncTimePresent',TBoolean), ('sib8info',SSib8Info)]
class SUlPCUeParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('p0UePusch',TOaMP0UePusch), ('p0UePucch',TOaMP0UePucch), ('deltaTfEnabled',TOaMDeltaTfEnabled), ('ulpcAccuEnable',TOaMUlpcAccuEnable), ('srsPwrOffset',SOaMSrsPwrOffset)]
class SCqiParamsScell(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCellIdScell',TOaMLnCelId), ('cqiAperMode',ECqiAperMode), ('cqiPerEnable',ECqiPerEnable), ('iCqiPmi',TICqiPmi), ('resourceIndexCqiR10',TResourceIndexCqi), ('cqiPerMode',ECqiPerMode), ('riEnable',TBoolean), ('iRi',TIRi), ('cqiPerSimulAck',ECqiPerSimulAck), ('cqiPerSbCycK',TCqiPerSbCycK), ('cqiPerSbPeriodicityFactorR10',ECqiPerSbPeriodicityFactorR10)]
class SCaWmpSCellContainer(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('harqMaxTrDlSCell',TOaMHarqMaxTrDl), ('sCellResourceGroupId',TSCellResourceGroupId), ('cqiParamsScellWmp',SCqiParamsScellWmp)]
