import prophy 


SIZE_OF_TH_UE_LARGE_DATA = 3
SIZE_OF_SPG = 3
SIZE_OF_NUM_DL_UE_LARGE_DATA = 4
SIZE_OF_SIUL_TABLE_DCM = 32
SIZE_OF_SIDL_TABLE_DCM = 32
SIZE_OF_TH_PUCCH_TPC_TABLE_DCM = 4
SIZE_OF_B_CA_TPC_TABLE_DCM = 4
SIZE_OF_PERIODIC_GRANT_THRESHOLD = 3
SIZE_OF_PERIODIC_GRANT_INDEX_REF_TABLE_DCM = 4
SIZE_OF_DELAY_PACKED_INDEX_REF_TABLE_DCM = 4
SIZE_OF_DELAY_PACKED_THRESHOLD = 3
SIZE_OF_CQI_TIMER_TABLE_DCM = 4
SIZE_OF_NUMBER_OF_UE_TABLE_DCM = 3
SIZE_OF_TA_RESTRICT_TABLE_DCM = 4
SIZE_OF_TA_PARAMS_TABLE_DCM = 2
MAX_NUM_OF_UE_CATEGORY_DCM = 8
SIZE_OF_SI_REPETITION_TABLE_DCM = 15
SIZE_OF_SI_BITMAP_DCM = 2
SIZE_OF_TPC_RNTI_TABLE_DCM = 100
SIZE_OF_RB_INFO_DBCH_TABLE_DCM = 16
SIZE_OF_UL_PERSISTENT_RB_NUM_TABLE_DCM = 4
SIZE_OF_DL_PERSISTENT_RB_NUM_TABLE_DCM = 8
SIZE_OF_P0_PRACH_INFO_TABLE_DCM = 8
SIZE_OF_SIUL_SPECIFIC_PARAMS_TABLE_DCM = 32
SIZE_OF_SIDL_SPECIFIC_PARAMS_TABLE_DCM = 32
SIZE_OF_UL_PERSISTENT_MCS_INDEX_TABLE_DCM = 4
SIZE_OF_PERSISTENT_MCS_INDEX_TABLE_DCM = 8
SIZE_OF_DRX_PARAMS_DCM = 2
SIZE_OF_PERSISTENT_BUNDLING_TABLE_DCM = 4
SIZE_OF_RV_INFO_TABLE_DCM = 16
MAX_NUM_OF_LCG_DCM = 4
SIZE_OF_PERSISTENT_TF_UL_TABLE_DCM = 4
SIZE_OF_PERSISTENT_TFR_INIT_UL_TABLE_DCM = 3
SIZE_OF_PERSISTENT_ULTFR_TABLE_DCM = 3
SIZE_OF_P0_PUCCH_REF_TABLE_DCM = 8
SIZE_OF_P0_PUSCH_REF_TABLE_DCM = 8
SIZE_OF_RBG_OFFSET_INFO_TABLE_DCM = 16
SIZE_OF_PSRS_OFFSET_REF_TABLE_DCM = 8
MAX_NUM_OF_LCP_DCM = 16
SIZE_OF_PERSISTENT_DL_TABLE_DCM = 8
SIZE_OF_PERSISTENT_TF_TABLE_DCM = 7
SIZE_OF_PERSISTENT_DLTFR_TABLE_DCM = 7
SIZE_OF_DCI_FORMAT_TABLE_DCM = 10
DCM_Y_PERIODIC_GRANT_MAX = 60
DCM_Y_PERIODIC_GRANT_MIN = 0
DCM_Y_DELAY_PACKED_MAX = 15
DCM_Y_DELAY_PACKED_MIN = 0
DCM_TRESHOLD_PL_RESTRICT_MAX = 63
DCM_TRESHOLD_PL_RESTRICT_MIN = 0
DCM_INDEX_MIN_RESTRICT_MIN = 0
DCM_TRESHOLD_TA_RESTRICT_MAX = 382
DCM_TRESHOLD_TA_RESTRICT_MIN = 1
DCM_INDEX_MIN_RESTRICT_MAX = ((SIZE_OF_PSRS_OFFSET_REF_TABLE_DCM)-1)

u32 = prophy.u32
u16 = prophy.u16
TBoolean = prophy.u32
TMaxNumEmergencyCallsDcm = prophy.u16
TPrioCoeffDcm = prophy.u16
TPathlossThDcm = prophy.u16
TCrThDcm = prophy.u16
TTxPowerAbsoluteDcm = prophy.u16
TNumOfRbsDcm = prophy.u16
TRbIndexDcm = prophy.u16
TTxControlPowerDcm = prophy.u16
TCqiDefaultDlDcm = prophy.u16
TOffsetPhichDcm = prophy.u16
TTxPowerAdjStepSizeDcm = prophy.u16
TTargetBlerDcm = prophy.u16
TPdcchFormatThDcm = prophy.u16
TNumOfOfdmaSymbolsDcm = prophy.u16
TTimerDcm = prophy.u16
TStopPeriodicTaThDcm = prophy.u16
TDataSizeDcm = prophy.u16
TPowerAdjStepCqiDcm = prophy.u16
TTfrDcm = prophy.u16
TPayloadSizeDcm = prophy.u32
TNumOfAckNackThDcm = prophy.u16
TWeightPersistentDlDcm = prophy.u16
TAverTimeRbUsageDcm = prophy.u16
TGuardRbDcm = prophy.u16
TCoeffTfrsDcm = prophy.u16
TPSrsOffsetRefDcm = prophy.u16
TSirSoundingRefDcm = prophy.u16
TTttSrsThDcm = prophy.u16
TTttSrsRenewalCycleDcm = prophy.u16
TRbgOffsetDcm = prophy.u16
TRbgOffsetThDcm = prophy.u16
TCoeffPathlossDcm = prophy.u16
TP0PuschRefDcm = prophy.u16
TTttP0PuxchThDcm = prophy.u16
TSirPucchDcm = prophy.u16
TP0PucchRefDcm = prophy.u16
TPersistentSirUlDcm = prophy.u16
TNumOfMaxTxThDcm = prophy.u16
TWeightPersistentUlDcm = prophy.u16
TRvInfoDcm = prophy.u16
TLcgDcm = prophy.u16
TMaxHarqReTxNumDcm = prophy.u16
TTargetDataRateIndexDcm = prophy.u16
TForgettingFactorConvDcm = prophy.u16
TCqiAdjStepDcm = prophy.u16
TCqiOffsetDcm = prophy.u16
TPowerOffsetCqiDcm = prophy.u16
TSirAdjStepDcm = prophy.u16
TSirOffsetDcm = prophy.u16
TPowerOffsetSirDcm = prophy.u16
TBooleanDcm = prophy.u16
TMaxNumHarqRetransmissionsUlSchDcm = prophy.u16
TP0UePuschDcm = prophy.u16
TP0UePucchDcm = prophy.u16
TSizeOfRaMsg3Dcm = prophy.u16
TTxPowerOfSyncReqDcm = prophy.u16
TOffsetPdcchMaxDcm = prophy.u16
TOffsetPdcchMinDcm = prophy.u16
TThCfiDcm = prophy.u16
TITpcRefDcm = prophy.u16
TInterferenceDcm = prophy.u16
TMaxNumPdcchDlUlDcm = prophy.u16
TSFNDcm = prophy.u16
TSubframeDcm = prophy.u16
TP0PrachDcm = prophy.u16
TThNumDcm = prophy.u16
TThCntDcm = prophy.u16
TThMsg3Dcm = prophy.u16
TNumOfSyncReqDcm = prophy.u16
TSyncInitialTimerDcm = prophy.u16
TSyncTimerDcm = prophy.u16
TMaxNumOfSyncReqDcm = prophy.u16
TPowerDcm = prophy.u16
TIndexDcm = prophy.u16
TSirDcm = prophy.u16
TNRachDcm = prophy.u16
TPhyCellIdDcm = prophy.u16
TThDcm = prophy.u16
TTxPowerDcm = prophy.u16
TImplicitReleaseAfterDcm = prophy.u16
TLteT1TimeThresholdDcm = prophy.u16
TRBmbmsDcm = prophy.u16
TMCSIndexDcm = prophy.u16
TFlagDcm = prophy.u16
TSidlDcm = prophy.u16
TSiulDcm = prophy.u16
TUeInactivityTimerDcm = prophy.u32
TPdcchFormatDcm = prophy.u16
TLcpDcm = prophy.u16
TTxPowerRelativeDcm = prophy.u16
TNumRbDcm = prophy.u16
TDeltaMsg2Dcm = prophy.u16
TSirCommonDcm = prophy.u16
TPowerRampingDcm = prophy.u16
TTpcPdcchStartOffsetDcm = prophy.u16
TNumSiDcm = prophy.u16
TMaxNumOfMsg3Dcm = prophy.u16
TPuschHoppingOffsetDcm = prophy.u16
TNumAvailableTxAntennaDcm = prophy.u16
TThTimeCqiRiDropDcm = prophy.u16
TDrbIdDcm = prophy.u16
TTresholdTARestrict = prophy.u16
TIndexMinRestrict = prophy.u16
TTresholdPLRestrict = prophy.u16
TMinTotalDLBufferSizeDcm = prophy.u16
TNumOfUELimitDCM = prophy.u16
TYDelayPackedDcm = prophy.u16
TYPeriodicGrantDcm = prophy.u16
TMinCostAMBRDcm = prophy.u16
TMaxTbsAMBRDcm = prophy.u16
TTargetDataRateMeasDcm = prophy.u32
TPeriodicGrantIdxStsDCM = prophy.u16
TNRBUlBufferMin = prophy.u16
TNTmpUlBuffer = prophy.u16
TCqiAvgForgetFactorCplaDcm = prophy.u16
TNDlCandidateMax = prophy.u16
TAlphaDlPDCCH = prophy.u16
TBetaDlPDCCHCommon = prophy.u16
TGammaDlPDCCH = prophy.u16
TNUlCandidateMax = prophy.u16
TAlphaUlPDCCH = prophy.u16
TBetaUlPDCCHCommon = prophy.u16
TGammaUlPDCCH = prophy.u16
TMinPuschSir = prophy.u16
TCellIdDcm = prophy.u16
TBCaPCell = prophy.u16
TBCaSCell = prophy.u16
TBCaTpc = prophy.u16
TThSCellCqiState = prophy.u16
TFlagACqiCellSelection = prophy.u16
TDlCsearch = prophy.u16
TDlCdataSize = prophy.u16
TThUELargeData = prophy.u16
TNDlPRBRemain = prophy.u16
TTProhibitRestartTA = prophy.u16
TTProhibitPaddingTA = prophy.u16
TThCQIOrdering = prophy.u16
TThTatRestartTA = prophy.u16
TThStopRestartTA = prophy.u16
TThPduSizePaddingTA = prophy.u16
TThTatPaddingTA = prophy.u16
TThSumRBOrdering = prophy.u16
TNDlUELargeData = prophy.u16

class EUmSnFieldLengthDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EUmSnFieldLengthDcm_5bits',0), ('EUmSnFieldLengthDcm_10bits',1)]
class EAperiodicCqiLifetimeDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EAperiodicCqiLifetimeDcm_NA',0), ('EAperiodicCqiLifetimeDcm_10',10), ('EAperiodicCqiLifetimeDcm_20',20), ('EAperiodicCqiLifetimeDcm_30',30), ('EAperiodicCqiLifetimeDcm_40',40), ('EAperiodicCqiLifetimeDcm_80',80), ('EAperiodicCqiLifetimeDcm_160',160), ('EAperiodicCqiLifetimeDcm_320',320), ('EAperiodicCqiLifetimeDcm_640',640)]
class ERlcConfigurationDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERlcConfigurationDcm_Am',0), ('ERlcConfigurationDcm_Um_BiDirection',1), ('ERlcConfigurationDcm_Um_UniDirection_Ul',2), ('ERlcConfigurationDcm_Um_UniDirection_Dl',3)]
class EUCoeffKsDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EUCoeffKsDcm_0',0), ('EUCoeffKsDcm_125',1)]
class EAverTimeInterferenceDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EAverTimeInterferenceDcm_NA',0), ('EAverTimeInterferenceDcm_100ms',100), ('EAverTimeInterferenceDcm_500ms',500), ('EAverTimeInterferenceDcm_1s',1000), ('EAverTimeInterferenceDcm_5s',5000), ('EAverTimeInterferenceDcm_10s',10000), ('EAverTimeInterferenceDcm_15s',15000), ('EAverTimeInterferenceDcm_20s',20000), ('EAverTimeInterferenceDcm_30s',30000), ('EAverTimeInterferenceDcm_1min',60000), ('EAverTimeInterferenceDcm_2min',120000), ('EAverTimeInterferenceDcm_3min',180000), ('EAverTimeInterferenceDcm_5min',300000), ('EAverTimeInterferenceDcm_10min',600000), ('EAverTimeInterferenceDcm_20min',1200000), ('EAverTimeInterferenceDcm_30min',1800000), ('EAverTimeInterferenceDcm_60min',3600000)]
class ECallTypeDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ECallTypeDcm_NonEmergency',0), ('ECallTypeDcm_Emergency',1), ('ECallTypeDcm_RadioPerfTesting',2)]
class EModulationSchemeMsg3Dcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EModulationSchemeMsg3Dcm_QPSK',0), ('EModulationSchemeMsg3Dcm_QPSK_16QAM',1)]
class EThSCellActivationDl1(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EThSCellActivationDl1_0byte',0), ('EThSCellActivationDl1_200byte',1), ('EThSCellActivationDl1_400byte',2), ('EThSCellActivationDl1_600byte',3), ('EThSCellActivationDl1_800byte',4), ('EThSCellActivationDl1_1000byte',5), ('EThSCellActivationDl1_1500byte',6), ('EThSCellActivationDl1_2kbyte',7), ('EThSCellActivationDl1_3kbyte',8), ('EThSCellActivationDl1_5kbyte',9), ('EThSCellActivationDl1_7kbyte',10), ('EThSCellActivationDl1_10kbyte',11), ('EThSCellActivationDl1_15kbyte',12), ('EThSCellActivationDl1_20kbyte',13), ('EThSCellActivationDl1_30kbyte',14), ('EThSCellActivationDl1_40kbyte',15), ('EThSCellActivationDl1_60kbyte',16), ('EThSCellActivationDl1_80kbyte',17), ('EThSCellActivationDl1_100kbyte',18), ('EThSCellActivationDl1_120kbyte',19), ('EThSCellActivationDl1_150kbyte',20), ('EThSCellActivationDl1_200kbyte',21), ('EThSCellActivationDl1_250kbyte',22), ('EThSCellActivationDl1_300kbyte',23), ('EThSCellActivationDl1_400kbyte',24), ('EThSCellActivationDl1_500kbyte',25), ('EThSCellActivationDl1_600kbyte',26), ('EThSCellActivationDl1_800kbyte',27), ('EThSCellActivationDl1_1Mbyte',28), ('EThSCellActivationDl1_2Mbyte',29), ('EThSCellActivationDl1_3Mbyte',30), ('EThSCellActivationDl1_infinity',31)]
class EUmBufferSizeDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EUmBufferSizeDcm_0_bytes',0), ('EUmBufferSizeDcm_100_bytes',100), ('EUmBufferSizeDcm_200_bytes',200), ('EUmBufferSizeDcm_300_bytes',300), ('EUmBufferSizeDcm_400_bytes',400), ('EUmBufferSizeDcm_500_bytes',500), ('EUmBufferSizeDcm_600_bytes',600), ('EUmBufferSizeDcm_700_bytes',700), ('EUmBufferSizeDcm_800_bytes',800), ('EUmBufferSizeDcm_900_bytes',900), ('EUmBufferSizeDcm_1_Kb',1000), ('EUmBufferSizeDcm_2_Kb',2000), ('EUmBufferSizeDcm_3_Kb',3000), ('EUmBufferSizeDcm_4_Kb',4000), ('EUmBufferSizeDcm_5_Kb',5000), ('EUmBufferSizeDcm_6_Kb',6000), ('EUmBufferSizeDcm_7_Kb',7000), ('EUmBufferSizeDcm_8_Kb',8000), ('EUmBufferSizeDcm_9_Kb',9000), ('EUmBufferSizeDcm_10_Kb',10000), ('EUmBufferSizeDcm_20_Kb',20000), ('EUmBufferSizeDcm_30_Kb',30000), ('EUmBufferSizeDcm_40_Kb',40000), ('EUmBufferSizeDcm_50_Kb',50000), ('EUmBufferSizeDcm_60_Kb',60000), ('EUmBufferSizeDcm_70_Kb',70000), ('EUmBufferSizeDcm_80_Kb',80000), ('EUmBufferSizeDcm_90_Kb',90000), ('EUmBufferSizeDcm_100_Kb',100000), ('EUmBufferSizeDcm_200_Kb',200000), ('EUmBufferSizeDcm_300_Kb',300000), ('EUmBufferSizeDcm_400_Kb',400000), ('EUmBufferSizeDcm_500_Kb',500000), ('EUmBufferSizeDcm_600_Kb',600000), ('EUmBufferSizeDcm_700_Kb',700000), ('EUmBufferSizeDcm_800_Kb',800000), ('EUmBufferSizeDcm_900_Kb',900000), ('EUmBufferSizeDcm_1000_Kb',1000000), ('EUmBufferSizeDcm_1100_Kb',1100000), ('EUmBufferSizeDcm_1200_Kb',1200000), ('EUmBufferSizeDcm_1300_Kb',1300000), ('EUmBufferSizeDcm_1400_Kb',1400000), ('EUmBufferSizeDcm_1500_Kb',1500000), ('EUmBufferSizeDcm_1600_Kb',1600000), ('EUmBufferSizeDcm_1700_Kb',1700000), ('EUmBufferSizeDcm_1800_Kb',1800000), ('EUmBufferSizeDcm_1900_Kb',1900000), ('EUmBufferSizeDcm_2000_Kb',2000000), ('EUmBufferSizeDcm_2100_Kb',2100000), ('EUmBufferSizeDcm_2200_Kb',2200000), ('EUmBufferSizeDcm_2300_Kb',2300000), ('EUmBufferSizeDcm_2400_Kb',2400000), ('EUmBufferSizeDcm_2500_Kb',2500000), ('EUmBufferSizeDcm_2600_Kb',2600000), ('EUmBufferSizeDcm_2700_Kb',2700000), ('EUmBufferSizeDcm_2800_Kb',2800000), ('EUmBufferSizeDcm_2900_Kb',2900000), ('EUmBufferSizeDcm_3000_Kb',3000000), ('EUmBufferSizeDcm_3100_Kb',3100000), ('EUmBufferSizeDcm_3200_Kb',3200000)]
class EPeriodicTaTimerThDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EPeriodicTaTimerThDcm_NA',0), ('EPeriodicTaTimerThDcm_100ms',100), ('EPeriodicTaTimerThDcm_200ms',200), ('EPeriodicTaTimerThDcm_300ms',300), ('EPeriodicTaTimerThDcm_400ms',400), ('EPeriodicTaTimerThDcm_500ms',500), ('EPeriodicTaTimerThDcm_600ms',600), ('EPeriodicTaTimerThDcm_700ms',700), ('EPeriodicTaTimerThDcm_800ms',800), ('EPeriodicTaTimerThDcm_900ms',900), ('EPeriodicTaTimerThDcm_1000ms',1000), ('EPeriodicTaTimerThDcm_1500ms',1500), ('EPeriodicTaTimerThDcm_2000ms',2000), ('EPeriodicTaTimerThDcm_2500ms',2500), ('EPeriodicTaTimerThDcm_3000ms',3000), ('EPeriodicTaTimerThDcm_3500ms',3500), ('EPeriodicTaTimerThDcm_4000ms',4000), ('EPeriodicTaTimerThDcm_4500ms',4500), ('EPeriodicTaTimerThDcm_5000ms',5000), ('EPeriodicTaTimerThDcm_6000ms',6000), ('EPeriodicTaTimerThDcm_7000ms',7000), ('EPeriodicTaTimerThDcm_8000ms',8000), ('EPeriodicTaTimerThDcm_10000ms',10000)]
class ETalkSpurtOffTimerDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETalkSpurtOffTimerDcm_NA',0), ('ETalkSpurtOffTimerDcm_20',20), ('ETalkSpurtOffTimerDcm_40',40), ('ETalkSpurtOffTimerDcm_60',60), ('ETalkSpurtOffTimerDcm_80',80), ('ETalkSpurtOffTimerDcm_100',100), ('ETalkSpurtOffTimerDcm_120',120), ('ETalkSpurtOffTimerDcm_140',140), ('ETalkSpurtOffTimerDcm_160',160), ('ETalkSpurtOffTimerDcm_200',200), ('ETalkSpurtOffTimerDcm_250',250), ('ETalkSpurtOffTimerDcm_300',300), ('ETalkSpurtOffTimerDcm_500',500), ('ETalkSpurtOffTimerDcm_1000',1000)]
class EBufferThresholdDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EBufferThresholdDcm_0kb',0), ('EBufferThresholdDcm_128kb',128), ('EBufferThresholdDcm_256kb',256), ('EBufferThresholdDcm_384kb',150), ('EBufferThresholdDcm_512kb',512), ('EBufferThresholdDcm_640kb',640), ('EBufferThresholdDcm_768kb',768), ('EBufferThresholdDcm_896kb',896), ('EBufferThresholdDcm_1024kb',1024), ('EBufferThresholdDcm_1152kb',1152), ('EBufferThresholdDcm_1280kb',1280), ('EBufferThresholdDcm_1792kb',1792), ('EBufferThresholdDcm_2305kb',2305), ('EBufferThresholdDcm_2816kb',2816), ('EBufferThresholdDcm_3328kb',3328), ('EBufferThresholdDcm_3840kb',3840), ('EBufferThresholdDcm_4352kb',4352), ('EBufferThresholdDcm_4864kb',4864), ('EBufferThresholdDcm_5376kb',5376), ('EBufferThresholdDcm_5888kb',5888), ('EBufferThresholdDcm_6400kb',6400), ('EBufferThresholdDcm_6912kb',6912), ('EBufferThresholdDcm_7424kb',7424), ('EBufferThresholdDcm_7936kb',7936), ('EBufferThresholdDcm_8448kb',8448), ('EBufferThresholdDcm_8960kb',8960), ('EBufferThresholdDcm_9472kb',9472), ('EBufferThresholdDcm_9984kb',9984), ('EBufferThresholdDcm_10496kb',10496), ('EBufferThresholdDcm_11008kb',11008), ('EBufferThresholdDcm_11520kb',11520), ('EBufferThresholdDcm_12032kb',12032), ('EBufferThresholdDcm_12544kb',12544), ('EBufferThresholdDcm_13056kb',13056), ('EBufferThresholdDcm_13568kb',13568), ('EBufferThresholdDcm_14080kb',14080), ('EBufferThresholdDcm_14592kb',14592), ('EBufferThresholdDcm_15104kb',15104), ('EBufferThresholdDcm_15616kb',15616), ('EBufferThresholdDcm_16128kb',16128), ('EBufferThresholdDcm_16640kb',16640), ('EBufferThresholdDcm_17152kb',17152), ('EBufferThresholdDcm_17664kb',17664), ('EBufferThresholdDcm_18176kb',18176), ('EBufferThresholdDcm_18688kb',18688), ('EBufferThresholdDcm_19200kb',19200)]
class EThPucchTpc(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EThPucchTpc_0',0), ('EThPucchTpc_10',1), ('EThPucchTpc_20',2), ('EThPucchTpc_30',3), ('EThPucchTpc_40',4), ('EThPucchTpc_50',5), ('EThPucchTpc_60',6), ('EThPucchTpc_80',7), ('EThPucchTpc_100',8), ('EThPucchTpc_120',9), ('EThPucchTpc_160',10), ('EThPucchTpc_200',11), ('EThPucchTpc_250',12), ('EThPucchTpc_300',13), ('EThPucchTpc_400',14), ('EThPucchTpc_500',15), ('EThPucchTpc_600',16), ('EThPucchTpc_800',17), ('EThPucchTpc_1000',18), ('EThPucchTpc_1500',19), ('EThPucchTpc_2000',20), ('EThPucchTpc_3000',21), ('EThPucchTpc_infinity',22)]
class EHoppingModeDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EHoppingModeDcm_noHopping',0), ('EHoppingModeDcm_interSubFrame',1), ('EHoppingModeDcm_intraAndInterSubFrame',2)]
class ESilentPeriodTimerDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ESilentPeriodTimerDcm_0ms',0), ('ESilentPeriodTimerDcm_20ms',20), ('ESilentPeriodTimerDcm_40ms',40), ('ESilentPeriodTimerDcm_60ms',60), ('ESilentPeriodTimerDcm_80ms',80), ('ESilentPeriodTimerDcm_120ms',120), ('ESilentPeriodTimerDcm_160ms',160), ('ESilentPeriodTimerDcm_200ms',200)]
class EModulationInfoDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EModulationInfoDcm_QPSK',0), ('EModulationInfoDcm_16QAM',1), ('EModulationInfoDcm_64QAM',2)]
class ENGapDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ENGapDcm_Gap1',0), ('ENGapDcm_Gap2',1)]
class ETimeAlignTimerDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETimeAlignTimerDcm_NA',0), ('ETimeAlignTimerDcm_500',500), ('ETimeAlignTimerDcm_750',750), ('ETimeAlignTimerDcm_1280',1280), ('ETimeAlignTimerDcm_1920',1920), ('ETimeAlignTimerDcm_2560',2560), ('ETimeAlignTimerDcm_5120',5120), ('ETimeAlignTimerDcm_10240',10240), ('ETimeAlignTimerDcm_infinity',2147483647)]
class EUlBundlingDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EUlBundlingDcm_NotDefined',0), ('EUlBundlingDcm_On',1), ('EUlBundlingDcm_Off',2)]
class EThUeInactivityTimeDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EThUeInactivityTimeDcm_0ms',0), ('EThUeInactivityTimeDcm_100ms',100), ('EThUeInactivityTimeDcm_200ms',200), ('EThUeInactivityTimeDcm_500ms',500), ('EThUeInactivityTimeDcm_1000ms',1000), ('EThUeInactivityTimeDcm_1500ms',1500), ('EThUeInactivityTimeDcm_2000ms',2000), ('EThUeInactivityTimeDcm_2500ms',2500), ('EThUeInactivityTimeDcm_3000ms',3000), ('EThUeInactivityTimeDcm_3500ms',3500), ('EThUeInactivityTimeDcm_4000ms',4000), ('EThUeInactivityTimeDcm_4500ms',4500), ('EThUeInactivityTimeDcm_5000ms',5000)]
class EAperiodicCqiTimerDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EAperiodicCqiTimerDcm_NA',0), ('EAperiodicCqiTimerDcm_10',10), ('EAperiodicCqiTimerDcm_20',20), ('EAperiodicCqiTimerDcm_30',30), ('EAperiodicCqiTimerDcm_40',40), ('EAperiodicCqiTimerDcm_60',60), ('EAperiodicCqiTimerDcm_80',80), ('EAperiodicCqiTimerDcm_100',100), ('EAperiodicCqiTimerDcm_Infinity',2147483647)]
class ETimerSCellCqiCheck(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETimerSCellCqiCheck_60ms',0), ('ETimerSCellCqiCheck_80ms',1), ('ETimerSCellCqiCheck_100ms',2), ('ETimerSCellCqiCheck_120ms',3), ('ETimerSCellCqiCheck_160ms',4), ('ETimerSCellCqiCheck_200ms',5), ('ETimerSCellCqiCheck_240ms',6), ('ETimerSCellCqiCheck_300ms',7), ('ETimerSCellCqiCheck_400ms',8), ('ETimerSCellCqiCheck_500ms',9), ('ETimerSCellCqiCheck_600ms',10), ('ETimerSCellCqiCheck_800ms',11), ('ETimerSCellCqiCheck_1s',12), ('ETimerSCellCqiCheck_infinity',2147483647)]
class EFDEstimationUsageDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EFDEstimationUsageDcm_FD_Estimation',0), ('EFDEstimationUsageDcm_FD_Low',1), ('EFDEstimationUsageDcm_FD_High',2)]
class ETimerDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETimerDcm_NA',0), ('ETimerDcm_100ms',100), ('ETimerDcm_200ms',200), ('ETimerDcm_400ms',400), ('ETimerDcm_800ms',800), ('ETimerDcm_1600ms',1600), ('ETimerDcm_3200ms',3200), ('ETimerDcm_6400ms',6400), ('ETimerDcm_12800ms',12800)]
class ECqiAverForgetFactorDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ECqiAverForgetFactorDcm_0',0), ('ECqiAverForgetFactorDcm_50',50), ('ECqiAverForgetFactorDcm_60',60), ('ECqiAverForgetFactorDcm_70',70), ('ECqiAverForgetFactorDcm_80',80), ('ECqiAverForgetFactorDcm_90',90), ('ECqiAverForgetFactorDcm_95',95), ('ECqiAverForgetFactorDcm_99',99)]
class EDCIFlagDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EDCIFlagDcm_NA',0), ('EDCIFlagDcm_1A',1), ('EDCIFlagDcm_1C',2)]
class ERMinDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERMinDcm_NA',0), ('ERMinDcm_0',2), ('ERMinDcm_1',4), ('ERMinDcm_2',6), ('ERMinDcm_3',8), ('ERMinDcm_4',10), ('ERMinDcm_5',20), ('ERMinDcm_6',40), ('ERMinDcm_7',80)]
class ETxPowerAdjPhichEnableDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETxPowerAdjPhichEnableDcm_DL',0), ('ETxPowerAdjPhichEnableDcm_UL',1), ('ETxPowerAdjPhichEnableDcm_OFF',2)]
class EThTimeCqiRiDropForSCell(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EThTimeCqiRiDropForSCell_0',0), ('EThTimeCqiRiDropForSCell_10',10), ('EThTimeCqiRiDropForSCell_20',20), ('EThTimeCqiRiDropForSCell_40',40), ('EThTimeCqiRiDropForSCell_80',80), ('EThTimeCqiRiDropForSCell_120',120), ('EThTimeCqiRiDropForSCell_160',160), ('EThTimeCqiRiDropForSCell_320',320), ('EThTimeCqiRiDropForSCell_infinity',2147483647)]
class EAverTimeSRSSDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EAverTimeSRSSDcm_NA',0), ('EAverTimeSRSSDcm_10ms',10), ('EAverTimeSRSSDcm_20ms',20), ('EAverTimeSRSSDcm_50ms',50), ('EAverTimeSRSSDcm_100ms',100), ('EAverTimeSRSSDcm_200ms',200), ('EAverTimeSRSSDcm_500ms',500), ('EAverTimeSRSSDcm_1000ms',1000)]
class ESchedPrioGroupIndexDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ESchedPrioGroupIndexDcm_High',0), ('ESchedPrioGroupIndexDcm_Middle',1), ('ESchedPrioGroupIndexDcm_Low',2)]
class ENumOfOfdmaSymbolsModeDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ENumOfOfdmaSymbolsModeDcm_Dynamic',0), ('ENumOfOfdmaSymbolsModeDcm_Static_1',1), ('ENumOfOfdmaSymbolsModeDcm_Static_2',2), ('ENumOfOfdmaSymbolsModeDcm_Static_3',3)]
class EActDeactRetxTimer(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EActDeactRetxTimer_0ms',0), ('EActDeactRetxTimer_50ms',1), ('EActDeactRetxTimer_100ms',2), ('EActDeactRetxTimer_150ms',3), ('EActDeactRetxTimer_200ms',4), ('EActDeactRetxTimer_250ms',5), ('EActDeactRetxTimer_300ms',6)]
class ETimingAlignTimerThDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETimingAlignTimerThDcm_NA',0), ('ETimingAlignTimerThDcm_sf500',500), ('ETimingAlignTimerThDcm_sf750ms',750), ('ETimingAlignTimerThDcm_sf1280',1280), ('ETimingAlignTimerThDcm_sf2560',2560), ('ETimingAlignTimerThDcm_sf5120',5120), ('ETimingAlignTimerThDcm_sf10240',10240), ('ETimingAlignTimerThDcm_infinity',0xFFFFFFFF)]
class EPowerAdjEnableDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EPowerAdjEnableDcm_OFF',0), ('EPowerAdjEnableDcm_ON',1), ('EPowerAdjEnableDcm_DL',2)]
class ESiTypeDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ESiTypeDcm_NA',0), ('ESiTypeDcm_Si2',2), ('ESiTypeDcm_Si3',3), ('ESiTypeDcm_Si4',4), ('ESiTypeDcm_Si5',5), ('ESiTypeDcm_Si6',6), ('ESiTypeDcm_Si7',7), ('ESiTypeDcm_Si8',8), ('ESiTypeDcm_Si9',9), ('ESiTypeDcm_Si10',10), ('ESiTypeDcm_Si11',11), ('ESiTypeDcm_Si12',12), ('ESiTypeDcm_Si13',13), ('ESiTypeDcm_Si14',14), ('ESiTypeDcm_Si15',15), ('ESiTypeDcm_Si16',16)]
class EMaxNumOfMsg3Dcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EMaxNumOfMsg3Dcm_NA',0), ('EMaxNumOfMsg3Dcm_1',1), ('EMaxNumOfMsg3Dcm_2',2), ('EMaxNumOfMsg3Dcm_4',4), ('EMaxNumOfMsg3Dcm_8',8), ('EMaxNumOfMsg3Dcm_10',10), ('EMaxNumOfMsg3Dcm_12',12), ('EMaxNumOfMsg3Dcm_14',14), ('EMaxNumOfMsg3Dcm_16',16)]
class EFlagDistributedDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EFlagDistributedDcm_LVRB',0), ('EFlagDistributedDcm_DVRB',1)]
class EThDelayPackedDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EThDelayPackedDcm_0',0), ('EThDelayPackedDcm_5',5), ('EThDelayPackedDcm_10',10), ('EThDelayPackedDcm_15',15), ('EThDelayPackedDcm_20',20), ('EThDelayPackedDcm_25',25), ('EThDelayPackedDcm_30',30), ('EThDelayPackedDcm_35',35), ('EThDelayPackedDcm_40',40), ('EThDelayPackedDcm_45',45), ('EThDelayPackedDcm_50',50), ('EThDelayPackedDcm_60',60), ('EThDelayPackedDcm_80',80), ('EThDelayPackedDcm_100',100), ('EThDelayPackedDcm_120',120), ('EThDelayPackedDcm_140',140)]
class EThSCellActivationDl2(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EThSCellActivationDl2_0ms',0), ('EThSCellActivationDl2_5ms',1), ('EThSCellActivationDl2_10ms',2), ('EThSCellActivationDl2_15ms',3), ('EThSCellActivationDl2_20ms',4), ('EThSCellActivationDl2_30ms',5), ('EThSCellActivationDl2_40ms',6), ('EThSCellActivationDl2_50ms',7), ('EThSCellActivationDl2_60ms',8), ('EThSCellActivationDl2_80ms',9), ('EThSCellActivationDl2_100ms',10), ('EThSCellActivationDl2_120ms',11), ('EThSCellActivationDl2_150ms',12), ('EThSCellActivationDl2_180ms',13), ('EThSCellActivationDl2_200ms',14), ('EThSCellActivationDl2_250ms',15), ('EThSCellActivationDl2_300ms',16), ('EThSCellActivationDl2_350ms',17), ('EThSCellActivationDl2_400ms',18), ('EThSCellActivationDl2_450ms',19), ('EThSCellActivationDl2_500ms',20), ('EThSCellActivationDl2_750ms',21), ('EThSCellActivationDl2_1s',22), ('EThSCellActivationDl2_infinity',23)]
class EAverTimeDMRSSDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EAverTimeDMRSSDcm_NA',0), ('EAverTimeDMRSSDcm_10ms',10), ('EAverTimeDMRSSDcm_20ms',20), ('EAverTimeDMRSSDcm_50ms',50), ('EAverTimeDMRSSDcm_100ms',100), ('EAverTimeDMRSSDcm_200ms',200), ('EAverTimeDMRSSDcm_500ms',500), ('EAverTimeDMRSSDcm_1000ms',1000)]
class ESCellDeactivationTimer(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ESCellDeactivationTimer_rf2',0), ('ESCellDeactivationTimer_rf4',1), ('ESCellDeactivationTimer_rf8',2), ('ESCellDeactivationTimer_rf16',3), ('ESCellDeactivationTimer_rf32',4), ('ESCellDeactivationTimer_rf64',5), ('ESCellDeactivationTimer_rf128',6), ('ESCellDeactivationTimer_spare',7), ('ESCellDeactivationTimer_infinity',255)]
class EAllocationModeDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EAllocationModeDcm_Mode0',0), ('EAllocationModeDcm_Mode1',1)]
class ETpcPdcchPeriodicityDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETpcPdcchPeriodicityDcm_NA',0), ('ETpcPdcchPeriodicityDcm_2ms',2), ('ETpcPdcchPeriodicityDcm_5ms',5), ('ETpcPdcchPeriodicityDcm_10ms',10), ('ETpcPdcchPeriodicityDcm_20ms',20), ('ETpcPdcchPeriodicityDcm_40ms',40), ('ETpcPdcchPeriodicityDcm_80ms',80), ('ETpcPdcchPeriodicityDcm_160ms',160), ('ETpcPdcchPeriodicityDcm_320ms',320), ('ETpcPdcchPeriodicityDcm_640ms',640), ('ETpcPdcchPeriodicityDcm_1280ms',1280)]
class EAverTimeSRSIDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EAverTimeSRSIDcm_NA',0), ('EAverTimeSRSIDcm_10ms',10), ('EAverTimeSRSIDcm_20ms',20), ('EAverTimeSRSIDcm_50ms',50), ('EAverTimeSRSIDcm_100ms',100), ('EAverTimeSRSIDcm_200ms',200)]
class EAperiodicCQIUsageDCM(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EAperiodicCQIUsageDCM_OFF',0), ('EAperiodicCQIUsageDCM_Enabled',1), ('EAperiodicCQIUsageDCM_Disabled',2)]
class EAperiodicCqiNotTriggeredTimerDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EAperiodicCqiNotTriggeredTimerDcm_NA',0), ('EAperiodicCqiNotTriggeredTimerDcm_10',10), ('EAperiodicCqiNotTriggeredTimerDcm_20',20), ('EAperiodicCqiNotTriggeredTimerDcm_30',30), ('EAperiodicCqiNotTriggeredTimerDcm_40',40), ('EAperiodicCqiNotTriggeredTimerDcm_60',60), ('EAperiodicCqiNotTriggeredTimerDcm_80',80), ('EAperiodicCqiNotTriggeredTimerDcm_100',100), ('EAperiodicCqiNotTriggeredTimerDcm_Infinity',2147483647)]
class ESCellType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ESCellType_0',0), ('ESCellType_1',1)]
class EAverTimePersistentSirUlDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EAverTimePersistentSirUlDcm_NA',0), ('EAverTimePersistentSirUlDcm_20ms',20), ('EAverTimePersistentSirUlDcm_40ms',40), ('EAverTimePersistentSirUlDcm_100ms',100), ('EAverTimePersistentSirUlDcm_200ms',200), ('EAverTimePersistentSirUlDcm_500ms',500), ('EAverTimePersistentSirUlDcm_1000ms',1000)]
class EHoppingPatternDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EHoppingPatternDcm_00',0), ('EHoppingPatternDcm_01',1), ('EHoppingPatternDcm_10',2), ('EHoppingPatternDcm_11',3)]
class EPersistentTimerDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EPersistentTimerDcm_NA',0), ('EPersistentTimerDcm_1ms',1), ('EPersistentTimerDcm_2ms',2), ('EPersistentTimerDcm_3ms',3), ('EPersistentTimerDcm_4ms',4), ('EPersistentTimerDcm_5ms',5), ('EPersistentTimerDcm_6ms',6), ('EPersistentTimerDcm_8ms',8), ('EPersistentTimerDcm_10ms',10), ('EPersistentTimerDcm_12ms',12), ('EPersistentTimerDcm_14ms',14), ('EPersistentTimerDcm_16ms',16), ('EPersistentTimerDcm_20ms',20), ('EPersistentTimerDcm_30ms',30), ('EPersistentTimerDcm_40ms',40), ('EPersistentTimerDcm_50ms',50), ('EPersistentTimerDcm_100ms',100), ('EPersistentTimerDcm_200ms',200)]
class ETimerProhibitActivationCommand(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETimerProhibitActivationCommand_0ms',0), ('ETimerProhibitActivationCommand_100ms',1), ('ETimerProhibitActivationCommand_200ms',2), ('ETimerProhibitActivationCommand_300ms',3), ('ETimerProhibitActivationCommand_400ms',4), ('ETimerProhibitActivationCommand_600ms',5), ('ETimerProhibitActivationCommand_800ms',6), ('ETimerProhibitActivationCommand_1s',7), ('ETimerProhibitActivationCommand_2s',8), ('ETimerProhibitActivationCommand_3s',9), ('ETimerProhibitActivationCommand_4s',10), ('ETimerProhibitActivationCommand_5s',11), ('ETimerProhibitActivationCommand_10s',12), ('ETimerProhibitActivationCommand_20s',13), ('ETimerProhibitActivationCommand_30s',14), ('ETimerProhibitActivationCommand_40s',15), ('ETimerProhibitActivationCommand_50s',16), ('ETimerProhibitActivationCommand_60s',17), ('ETimerProhibitActivationCommand_90s',18), ('ETimerProhibitActivationCommand_120s',19), ('ETimerProhibitActivationCommand_180s',20), ('ETimerProhibitActivationCommand_240s',21), ('ETimerProhibitActivationCommand_300s',22)]
class ESrsBandwidthDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ESrsBandwidthDcm_bw0',0), ('ESrsBandwidthDcm_bw1',1), ('ESrsBandwidthDcm_bw2',2), ('ESrsBandwidthDcm_bw3',3)]
class EThSCellActivationUl1(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EThSCellActivationUl1_0byte',0), ('EThSCellActivationUl1_100byte',1), ('EThSCellActivationUl1_200byte',2), ('EThSCellActivationUl1_300byte',3), ('EThSCellActivationUl1_400byte',4), ('EThSCellActivationUl1_500byte',5), ('EThSCellActivationUl1_750byte',6), ('EThSCellActivationUl1_1000byte',7), ('EThSCellActivationUl1_1500byte',8), ('EThSCellActivationUl1_2kbyte',9), ('EThSCellActivationUl1_3kbyte',10), ('EThSCellActivationUl1_4kbyte',11), ('EThSCellActivationUl1_6kbyte',12), ('EThSCellActivationUl1_8kbyte',13), ('EThSCellActivationUl1_10kbyte',14), ('EThSCellActivationUl1_15kbyte',15), ('EThSCellActivationUl1_20kbyte',16), ('EThSCellActivationUl1_30kbyte',17), ('EThSCellActivationUl1_40kbyte',18), ('EThSCellActivationUl1_50kbyte',19), ('EThSCellActivationUl1_60kbyte',20), ('EThSCellActivationUl1_80kbyte',21), ('EThSCellActivationUl1_100kbyte',22), ('EThSCellActivationUl1_120kbyte',23), ('EThSCellActivationUl1_150kbyte',24), ('EThSCellActivationUl1_200kbyte',25), ('EThSCellActivationUl1_250kbyte',26), ('EThSCellActivationUl1_300kbyte',27), ('EThSCellActivationUl1_400kbyte',28), ('EThSCellActivationUl1_500kbyte',29), ('EThSCellActivationUl1_600kbyte',30), ('EThSCellActivationUl1_infinity',31)]
class EThSCellActivationUl2(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EThSCellActivationUl2_0ms',0), ('EThSCellActivationUl2_5ms',1), ('EThSCellActivationUl2_10ms',2), ('EThSCellActivationUl2_15ms',3), ('EThSCellActivationUl2_20ms',4), ('EThSCellActivationUl2_30ms',5), ('EThSCellActivationUl2_40ms',6), ('EThSCellActivationUl2_50ms',7), ('EThSCellActivationUl2_60ms',8), ('EThSCellActivationUl2_80ms',9), ('EThSCellActivationUl2_100ms',10), ('EThSCellActivationUl2_120ms',11), ('EThSCellActivationUl2_150ms',12), ('EThSCellActivationUl2_180ms',13), ('EThSCellActivationUl2_200ms',14), ('EThSCellActivationUl2_250ms',15), ('EThSCellActivationUl2_300ms',16), ('EThSCellActivationUl2_350ms',17), ('EThSCellActivationUl2_400ms',18), ('EThSCellActivationUl2_450ms',19), ('EThSCellActivationUl2_500ms',20), ('EThSCellActivationUl2_750ms',21), ('EThSCellActivationUl2_1s',22), ('EThSCellActivationUl2_infinity',23)]
class EAverTimePucchSirDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EAverTimePucchSirDcm_NA',0), ('EAverTimePucchSirDcm_1ms',1), ('EAverTimePucchSirDcm_10ms',10), ('EAverTimePucchSirDcm_20ms',20), ('EAverTimePucchSirDcm_50ms',50), ('EAverTimePucchSirDcm_100ms',100), ('EAverTimePucchSirDcm_200ms',200)]
class EDelayPackedTimerDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EDelayPackedTimerDcm_NA',0), ('EDelayPackedTimerDcm_50',50), ('EDelayPackedTimerDcm_100',100), ('EDelayPackedTimerDcm_200',200), ('EDelayPackedTimerDcm_300',300), ('EDelayPackedTimerDcm_400',400), ('EDelayPackedTimerDcm_500',500), ('EDelayPackedTimerDcm_600',600), ('EDelayPackedTimerDcm_700',700), ('EDelayPackedTimerDcm_800',800), ('EDelayPackedTimerDcm_900',900), ('EDelayPackedTimerDcm_1000',1000), ('EDelayPackedTimerDcm_1500',1500), ('EDelayPackedTimerDcm_2000',2000), ('EDelayPackedTimerDcm_3000',3000), ('EDelayPackedTimerDcm_4000',4000), ('EDelayPackedTimerDcm_5000',5000)]
class EPeriodicGrantTimer(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EPeriodicGrantTimer_NA',0), ('EPeriodicGrantTimer_10',10), ('EPeriodicGrantTimer_20',20), ('EPeriodicGrantTimer_30',30), ('EPeriodicGrantTimer_40',40), ('EPeriodicGrantTimer_50',50), ('EPeriodicGrantTimer_60',60), ('EPeriodicGrantTimer_80',80), ('EPeriodicGrantTimer_100',100), ('EPeriodicGrantTimer_120',120), ('EPeriodicGrantTimer_140',140), ('EPeriodicGrantTimer_160',160)]
class ESCellDeactivationTimerEnb(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ESCellDeactivationTimerEnb_400ms',0), ('ESCellDeactivationTimerEnb_600ms',1), ('ESCellDeactivationTimerEnb_800ms',2), ('ESCellDeactivationTimerEnb_1000ms',3), ('ESCellDeactivationTimerEnb_1200ms',4), ('ESCellDeactivationTimerEnb_1400ms',5), ('ESCellDeactivationTimerEnb_1600ms',6), ('ESCellDeactivationTimerEnb_1800ms',7), ('ESCellDeactivationTimerEnb_2000ms',8), ('ESCellDeactivationTimerEnb_2500ms',9), ('ESCellDeactivationTimerEnb_3000ms',10), ('ESCellDeactivationTimerEnb_3500ms',11), ('ESCellDeactivationTimerEnb_4s',12), ('ESCellDeactivationTimerEnb_5s',13), ('ESCellDeactivationTimerEnb_6s',14), ('ESCellDeactivationTimerEnb_8s',15), ('ESCellDeactivationTimerEnb_10s',16), ('ESCellDeactivationTimerEnb_15s',17), ('ESCellDeactivationTimerEnb_20s',18), ('ESCellDeactivationTimerEnb_25s',19), ('ESCellDeactivationTimerEnb_30s',20), ('ESCellDeactivationTimerEnb_40s',21), ('ESCellDeactivationTimerEnb_50s',22), ('ESCellDeactivationTimerEnb_60s',23), ('ESCellDeactivationTimerEnb_Infinity',255)]
class EPeriodicGrantTimerDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EPeriodicGrantTimerDcm_NA',0), ('EPeriodicGrantTimerDcm_50',50), ('EPeriodicGrantTimerDcm_100',100), ('EPeriodicGrantTimerDcm_200',200), ('EPeriodicGrantTimerDcm_300',300), ('EPeriodicGrantTimerDcm_400',400), ('EPeriodicGrantTimerDcm_500',500), ('EPeriodicGrantTimerDcm_600',600), ('EPeriodicGrantTimerDcm_700',700), ('EPeriodicGrantTimerDcm_800',800), ('EPeriodicGrantTimerDcm_900',900), ('EPeriodicGrantTimerDcm_1000',1000), ('EPeriodicGrantTimerDcm_1500',1500), ('EPeriodicGrantTimerDcm_2000',2000), ('EPeriodicGrantTimerDcm_3000',3000), ('EPeriodicGrantTimerDcm_4000',4000), ('EPeriodicGrantTimerDcm_5000',5000)]
class EAmbrPeriodDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EAmbrPeriodDcm_Undefined',0), ('EAmbrPeriodDcm_100ms',100), ('EAmbrPeriodDcm_200ms',200), ('EAmbrPeriodDcm_500ms',500), ('EAmbrPeriodDcm_1000ms',1000), ('EAmbrPeriodDcm_2000ms',2000), ('EAmbrPeriodDcm_Infinity',65535)]
class EPowerTypeDcm(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EPowerTypeDcm_P0_PUCCH',0), ('EPowerTypeDcm_P0_PUSCH',1), ('EPowerTypeDcm_P0_Pre',2)]

class STxPowersDlDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('referenceSignalPower',TTxPowerAbsoluteDcm), ('pASch',TTxPowerRelativeDcm), ('pAPbch',TTxPowerRelativeDcm), ('pBPbch',TTxPowerRelativeDcm), ('pAPdsch',TTxPowerRelativeDcm), ('pBPdsch',TTxPowerRelativeDcm)]
class SCchInformationDlDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sirCommonDbchTable',prophy.bytes(size=SIZE_OF_RB_INFO_DBCH_TABLE_DCM)), ('sirCommonPch',TSirCommonDcm), ('sirCommonRachResp',TSirCommonDcm)]
class SPdcchTpcParamsDlDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('txPowerPdcchRef0',prophy.bytes(size=SIZE_OF_DCI_FORMAT_TABLE_DCM)), ('txPowerPdcchRef1',prophy.bytes(size=SIZE_OF_DCI_FORMAT_TABLE_DCM)), ('txPowerPdcchRef2',prophy.bytes(size=SIZE_OF_DCI_FORMAT_TABLE_DCM)), ('txPowerPdcchRef3',prophy.bytes(size=SIZE_OF_DCI_FORMAT_TABLE_DCM)), ('cqiDefaultPdcch0',prophy.bytes(size=SIZE_OF_DCI_FORMAT_TABLE_DCM)), ('cqiDefaultPdcch1',prophy.bytes(size=SIZE_OF_DCI_FORMAT_TABLE_DCM)), ('cqiDefaultPdcch2',prophy.bytes(size=SIZE_OF_DCI_FORMAT_TABLE_DCM)), ('cqiDefaultPdcch3',prophy.bytes(size=SIZE_OF_DCI_FORMAT_TABLE_DCM)), ('pdcchFormat0ThTable',prophy.bytes(size=SIZE_OF_DCI_FORMAT_TABLE_DCM)), ('pdcchFormat1ThTable',prophy.bytes(size=SIZE_OF_DCI_FORMAT_TABLE_DCM)), ('pdcchFormat2ThTable',prophy.bytes(size=SIZE_OF_DCI_FORMAT_TABLE_DCM)), ('txPowerAdjUlEnable',EPowerAdjEnableDcm), ('numOfOfdmaSymbolsMode',ENumOfOfdmaSymbolsModeDcm), ('txPowerOfRachRespPdcch',TTxControlPowerDcm), ('txPowerOfPchPdcch',TTxControlPowerDcm), ('txPowerOfDbchPdcch',TTxControlPowerDcm), ('maxTxPowerOfPdcch',TTxControlPowerDcm), ('minTxPowerOfPdcch',TTxControlPowerDcm), ('txPowerAdjStepSize',TTxPowerAdjStepSizeDcm), ('dlSchPdcchTargetBler',TTargetBlerDcm), ('ulSchPdcchTargetBler',TTargetBlerDcm), ('txPowerAdjDlEnable',TBooleanDcm), ('numOfOfdmaSymbolsDbchOffset',TNumOfOfdmaSymbolsDcm), ('numOfOfdmaSymbolsPchOffset',TNumOfOfdmaSymbolsDcm), ('numOfOfdmaSymbolsRachRespOffset',TNumOfOfdmaSymbolsDcm), ('pdcchFormatDbch',TPdcchFormatDcm), ('pdcchFormatPch',TPdcchFormatDcm), ('pdcchFormatTpcPucch',TPdcchFormatDcm), ('pdcchFormatTpcPusch',TPdcchFormatDcm), ('pdcchFormatRachResp',TPdcchFormatDcm), ('offsetPdcchMax',TOffsetPdcchMaxDcm), ('offsetPdcchMin',TOffsetPdcchMinDcm), ('thCfi1to2',TThCfiDcm), ('thCfi2to3',TThCfiDcm), ('pdcchFormatMch',TPdcchFormatDcm), ('txPowerOfMchPdcch',TTxPowerDcm), ('txPowerOfTpcPucchPdcch',TTxPowerDcm), ('txPowerOfTpcPuschPdcch',TTxPowerDcm), ('pdcchResourceAmount',prophy.u16)]
class SPhichTpcParamsDlDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('txPowerAdjPhichEnable',ETxPowerAdjPhichEnableDcm), ('refTxPowerOfPhichNormal',TTxControlPowerDcm), ('cqiDefaultPhichNormal',TCqiDefaultDlDcm), ('refTxPowerOfPhichExtended',TTxControlPowerDcm), ('cqiDefaultPhichExtended',TCqiDefaultDlDcm), ('offsetPhich0',TOffsetPhichDcm), ('offsetPhich1',TOffsetPhichDcm), ('offsetPhich2',TOffsetPhichDcm), ('cqiAdjustPhich',TCqiAdjStepDcm)]
class SCplaParamsDlDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('pdcchTpcParamsDl',SPdcchTpcParamsDlDcm), ('phichTpcParamsDl',SPhichTpcParamsDlDcm), ('txPowerOfPcfich',TTxControlPowerDcm), ('cqiAvgForgetFactorCpla',TCqiAvgForgetFactorCplaDcm)]
class SDrxParamsDlDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('drxCommandTh',ETimerDcm)]
class STaParamsDlDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('periodicityTa',EPeriodicTaTimerThDcm), ('timeAlignmentTimerDedicated',ETimeAlignTimerDcm), ('periodicTaEnable',TBooleanDcm), ('eventTriggeredTaEnable',TBooleanDcm), ('thStopPeriodicTaTh',TStopPeriodicTaThDcm), ('thTatRestartTA',TThTatRestartTA), ('tProhibitRestartTA',TTProhibitRestartTA), ('thStopRestartTA',TThStopRestartTA), ('tProhibitPaddingTA',TTProhibitPaddingTA), ('thPduSizePaddingTA',TThPduSizePaddingTA), ('thTatPaddingTA',TThTatPaddingTA), ('padding',prophy.u16)]
class SSpsTfDlDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('modulation',EModulationInfoDcm), ('payloadSize',TPayloadSizeDcm), ('numOfRbs',TNumOfRbsDcm), ('padding',prophy.u16)]
class SDLPersistentParamsDlDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('persistentTfDlTable',prophy.bytes(size=SIZE_OF_PERSISTENT_DL_TABLE_DCM)), ('persistentDlTfrUpTable',prophy.bytes(size=SIZE_OF_PERSISTENT_DLTFR_TABLE_DCM)), ('persistentDlTfrDownTable',prophy.bytes(size=SIZE_OF_PERSISTENT_DLTFR_TABLE_DCM)), ('persistentTfrInitDlTable',prophy.bytes(size=SIZE_OF_PERSISTENT_TF_TABLE_DCM)), ('mcsIndexDl',prophy.bytes(size=SIZE_OF_DL_PERSISTENT_RB_NUM_TABLE_DCM)), ('numRbDl',prophy.bytes(size=SIZE_OF_DL_PERSISTENT_RB_NUM_TABLE_DCM)), ('padding1',prophy.u16), ('cqiAverForgetFactor',ECqiAverForgetFactorDcm), ('silentPeriodTimerTh',ESilentPeriodTimerDcm), ('persistentTttDlTh',EPersistentTimerDcm), ('persistentReconfigDlTimerTh',EPersistentTimerDcm), ('dlTalkSpurtUpperDataTh',TDataSizeDcm), ('dlTalkSpurtLowerDataSIDTh',TDataSizeDcm), ('powerAdjStepCqiPersistentDl',TPowerAdjStepCqiDcm), ('targetBlerPersistentDl',TTargetBlerDcm), ('numOfNackTh',TNumOfAckNackThDcm), ('weightDBCH',TWeightPersistentDlDcm), ('weightPch',TWeightPersistentDlDcm), ('averTimePchRbUsage',TAverTimeRbUsageDcm), ('averTimeDbchRbUsage',TAverTimeRbUsageDcm), ('weightRachRes',TWeightPersistentDlDcm), ('rbMbms',TRBmbmsDcm), ('weightMbms',TWeightPersistentDlDcm), ('weightPersistentDl',TWeightPersistentDlDcm), ('averTimeRachResRbUsage',TAverTimeRbUsageDcm), ('averTimePersistentDlRbUsage',TAverTimeRbUsageDcm), ('cqiAdjustPersistent',TCqiAdjStepDcm)]
class SCoeffReTxInfoDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('coeffNumReTx0',TPrioCoeffDcm), ('coeffNumReTx1',TPrioCoeffDcm), ('coeffNumReTx2to3',TPrioCoeffDcm), ('coeffNumReTx4to15',TPrioCoeffDcm)]
class SSIDLSpecificParamsDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('schedPriorityGroupIndexDl',ESchedPrioGroupIndexDcm), ('prioLcp',TPrioCoeffDcm), ('dlTargetDataRate',TTargetDataRateIndexDcm), ('dlFlagAMBR',TBooleanDcm), ('flagSCellSchedulingDl',TBooleanDcm)]
class SCoeffParamsLCPDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('prioHarqDl',SCoeffReTxInfoDcm), ('sidlSpecificParamsTable',prophy.bytes(size=SIZE_OF_SIDL_SPECIFIC_PARAMS_TABLE_DCM)), ('buffTimeLowTh',TTimerDcm), ('buffTimeHighTh',TTimerDcm), ('weightCoeffNumReTx',TPrioCoeffDcm), ('weightCoeffBuffTime',TPrioCoeffDcm), ('weightCoeffDlADR',TPrioCoeffDcm), ('forgettingFactorConvAdrDl',TForgettingFactorConvDcm)]
class SCqiParamsLCPDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('deltaCqiAdjDl',TCqiAdjStepDcm), ('targetBlerDl',TTargetBlerDcm), ('powerOffsetCqiDl',TPowerOffsetCqiDcm), ('padding',prophy.u16)]
class SDcmLCPInfoCSDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('coeffParamsLCP',SCoeffParamsLCPDcm), ('cqiParamsLCP',SCqiParamsLCPDcm), ('dlTargetDataRateMeas',TTargetDataRateMeasDcm), ('maxNumHarqRetransmissionsDl',TMaxHarqReTxNumDcm), ('flagOrderingLowClass',TBooleanDcm)]
class SP0PucchInfoDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('p0PucchRef',TP0PucchRefDcm), ('tInterferenceUp',TInterferenceDcm), ('tInterferenceDown',TInterferenceDcm), ('padding',prophy.u16)]
class SPucchTpcParamsDlDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('p0PucchInfoTable',prophy.bytes(size=SIZE_OF_P0_PUCCH_REF_TABLE_DCM)), ('averTimePucchAvgTpcS',EAverTimePucchSirDcm), ('averTimePucchAvgTpcI',EAverTimePucchSirDcm), ('averTimePucchInstTpcI',EAverTimePucchSirDcm), ('averTimePucchI',EAverTimeInterferenceDcm), ('tSirPucchInst',TSirPucchDcm), ('tSirPucchAver',TSirPucchDcm), ('pucchTpcOffset',TSirPucchDcm), ('tttP0PucchTh',TTttP0PuxchThDcm), ('flagPucchTpcCommandReset',TBooleanDcm), ('padding',prophy.u16)]
class SDCIParamsDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dCIFlagPch',EDCIFlagDcm), ('dCIFlagDbch',EDCIFlagDcm), ('dCIFlagRachres',EDCIFlagDcm), ('flagDistributed',EFlagDistributedDcm), ('nGap',ENGapDcm)]
class SSyncInfoDlDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('syncInitialTimer',TSyncInitialTimerDcm), ('nSyncReqMax',TNumOfSyncReqDcm), ('syncTimerR',TSyncTimerDcm), ('syncTimerD',TSyncTimerDcm), ('maxNumOfSyncReqs',TMaxNumOfSyncReqDcm), ('padding',prophy.u16)]
class SAperiodicCqiParamsDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('aperiodicCqiTimer',EAperiodicCqiTimerDcm), ('aperiodicCqiLifetime',EAperiodicCqiLifetimeDcm), ('aperiodicCqiUsageTable',prophy.bytes(size=MAX_NUM_OF_LCP_DCM)), ('aperiodicCqiNotTriggeredTimer',prophy.bytes(size=SIZE_OF_CQI_TIMER_TABLE_DCM)), ('numOfUELimit',prophy.bytes(size=SIZE_OF_NUMBER_OF_UE_TABLE_DCM)), ('minTotalDLBufferSize',TMinTotalDLBufferSizeDcm)]
class SRbRestrictionParamsDlDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cchStartRb',TRbIndexDcm), ('cchEndRb',TRbIndexDcm), ('spsStartRb',TRbIndexDcm), ('spsEndRb',TRbIndexDcm), ('dynamicStartRb',TRbIndexDcm), ('dynamicEndRb',TRbIndexDcm)]
class SDelayPackedInfoDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('thDelayPacked',EThDelayPackedDcm), ('thDataSizePacked',prophy.u16), ('numTxCount',prophy.u16), ('numPdu',prophy.u16), ('tfMinDelayPacked',prophy.u16), ('rbMinDelayPacked',prophy.u16), ('reserved1',prophy.u16), ('reserved2',prophy.u16)]
class SDlVoLteParamsDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('delayPackedIndexRefTable',prophy.bytes(size=SIZE_OF_DELAY_PACKED_INDEX_REF_TABLE_DCM)), ('yDelayPacked',prophy.bytes(size=SIZE_OF_DELAY_PACKED_THRESHOLD)), ('delayPackedTimer',EDelayPackedTimerDcm), ('cqiDelayPackedDiff',prophy.u16), ('alphaDelayPacked',prophy.u16), ('delayPackedInitIndex',prophy.u16), ('numProhibitDelayPacked',prophy.u16), ('reserved1',prophy.u16), ('reserved2',prophy.u16)]
class SAssuredPucchInfoDl(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('thTimeCqiRiDropForDcmAlgorithmDl',TThTimeCqiRiDropDcm), ('thTimeCqiRiDropForHst1Dl',TThTimeCqiRiDropDcm), ('thTimeCqiRiDropForHst3Dl',TThTimeCqiRiDropDcm), ('padding',prophy.u16), ('thTimeCqiRiDropForDcmAlgorithmDlSCell',EThTimeCqiRiDropForSCell), ('thTimeCqiRiDropForHst1DlSCell',EThTimeCqiRiDropForSCell), ('thTimeCqiRiDropForHst3DlSCell',EThTimeCqiRiDropForSCell)]
class SDlDcmMacPsContainerCSDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('txPowers',STxPowersDlDcm), ('cchInformationDl',SCchInformationDlDcm), ('cplaParamsDl',SCplaParamsDlDcm), ('drxParams',SDrxParamsDlDcm), ('taParamsDl',prophy.bytes(size=SIZE_OF_TA_PARAMS_TABLE_DCM)), ('dLPersistentParams',SDLPersistentParamsDlDcm), ('dcmLCPInfoTable',prophy.bytes(size=MAX_NUM_OF_LCP_DCM)), ('pucchTpcParamsDl',SPucchTpcParamsDlDcm), ('dciParams',SDCIParamsDcm), ('syncInfoDl',SSyncInfoDlDcm), ('aperiodicCqiParams',SAperiodicCqiParamsDcm), ('rbRestrictionParamsDl',SRbRestrictionParamsDlDcm), ('voLteDlParams',SDlVoLteParamsDcm), ('rvInfoTable',prophy.bytes(size=SIZE_OF_RV_INFO_TABLE_DCM)), ('nCapabilityTable',prophy.bytes(size=MAX_NUM_OF_UE_CATEGORY_DCM)), ('rMinDl',ERMinDcm), ('dlAmbrPeriod',EAmbrPeriodDcm), ('thUeInactivityTimeHo',EThUeInactivityTimeDcm), ('thUeInactivityTimeReEst',EThUeInactivityTimeDcm), ('ueInactivityTimerIdleTh',TUeInactivityTimerDcm), ('fdEstimationUsage',EFDEstimationUsageDcm), ('maxNumOfEmergCallsDl',TMaxNumEmergencyCallsDcm), ('prioDrx',TPrioCoeffDcm), ('prioMacCe',TPrioCoeffDcm), ('crTh',TCrThDcm), ('nDlMax',TMaxNumPdcchDlUlDcm), ('maxCqiOffsetDl',TCqiOffsetDcm), ('minCqiOffsetDl',TCqiOffsetDcm), ('cqiRef',TCqiDefaultDlDcm), ('assuredPucchInfoDl',SAssuredPucchInfoDl), ('lteT1TimeTh',TLteT1TimeThresholdDcm), ('nDlCandidateMax',TNDlCandidateMax), ('alphaDlPDCCH',TAlphaDlPDCCH), ('betaDlPDCCHCommon',TBetaDlPDCCHCommon), ('gammaDlPDCCH',TGammaDlPDCCH), ('bCaPCell',TBCaPCell), ('bCaSCell',TBCaSCell), ('bCaTpc',prophy.bytes(size=SIZE_OF_B_CA_TPC_TABLE_DCM)), ('thSCellCqiState',TThSCellCqiState), ('flagACqiCellSelection',TFlagACqiCellSelection), ('padding1',prophy.u16), ('thSCellActivationDl1',EThSCellActivationDl1), ('thSCellActivationDl2',EThSCellActivationDl2), ('timerProhibitActivationCommand',ETimerProhibitActivationCommand), ('timerSCellCqiCheck',ETimerSCellCqiCheck), ('actDeactRetxTimer',EActDeactRetxTimer), ('flagTaSCell',TBooleanDcm), ('padding2',prophy.u16), ('sCellType',ESCellType), ('thPucchTpc',prophy.bytes(size=SIZE_OF_TH_PUCCH_TPC_TABLE_DCM)), ('nDlUELargeData',prophy.bytes(size=SIZE_OF_NUM_DL_UE_LARGE_DATA)), ('thUELargeData',prophy.bytes(size=SIZE_OF_TH_UE_LARGE_DATA)), ('flagOrdering',prophy.bytes(size=SIZE_OF_SPG)), ('nDlPRBRemain',TNDlPRBRemain), ('thCQIOrdering',TThCQIOrdering), ('dlCsearch',TDlCsearch), ('dlCdataSize',TDlCdataSize), ('thSumRBOrdering',TThSumRBOrdering), ('reserved1',prophy.u16), ('reserved2',prophy.u16), ('reserved3',prophy.u16)]
class SP0PrachInfoDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('p0Prach',TP0PrachDcm), ('interferencePrachUp',TInterferenceDcm), ('interferencePrachDown',TInterferenceDcm), ('padding',prophy.u16)]
class SPrachTpcParamsUlDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('p0PrachInfoDcm',prophy.bytes(size=SIZE_OF_P0_PRACH_INFO_TABLE_DCM)), ('averTimePrachI',EAverTimeInterferenceDcm), ('tttP0PrachTh',TThDcm), ('deltaMsg2',TDeltaMsg2Dcm), ('deltaPowerRamping',TPowerRampingDcm), ('padding',prophy.u16)]
class SPuschFreqHoppingInformationDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('hoppingModeRachMsg3',EHoppingModeDcm), ('hoppingPatternRachMsg3',EHoppingPatternDcm), ('hoppingModeUlSchDynamicHighFd',EHoppingModeDcm), ('hoppingModeUlSchDynamicLowFd',EHoppingModeDcm), ('hoppingPatternUlSchDynamic',EHoppingPatternDcm), ('hoppingModeUlSchSPS0',EHoppingModeDcm), ('hoppingModeUlSchSPS1',EHoppingModeDcm), ('hoppingPatternUlSchSPS0',EHoppingPatternDcm), ('hoppingPatternUlSchSPS1',EHoppingPatternDcm), ('puschHoppingOffset',TPuschHoppingOffsetDcm), ('padding',prophy.u16)]
class SPSrsOffsetInfoDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('srsBandwidth',ESrsBandwidthDcm), ('pSrsOffsetRef',TPSrsOffsetRefDcm), ('tSirSoundingRef',TSirSoundingRefDcm), ('pathlossUp',TPathlossThDcm), ('pathlossDown',TPathlossThDcm)]
class SSrsBandwidthControlInfoDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('pSrsOffsetRefTable',prophy.bytes(size=SIZE_OF_PSRS_OFFSET_REF_TABLE_DCM)), ('tttSrsTh',TTttSrsThDcm), ('tttSrsRenewalCycle',TTttSrsRenewalCycleDcm), ('indexSrsInitIndex',TIndexDcm), ('padding',prophy.u16)]
class SRbgOffsetControlInfoDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('rbgOffsetInfoA',prophy.bytes(size=SIZE_OF_RBG_OFFSET_INFO_TABLE_DCM)), ('rbgOffsetInfoB',prophy.bytes(size=SIZE_OF_RBG_OFFSET_INFO_TABLE_DCM)), ('rbgOffsetHighTh',TRbgOffsetThDcm), ('rbgOffsetLowTh',TRbgOffsetThDcm)]
class SP0PuschInfoDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('p0PuschRef',TP0PuschRefDcm), ('tInterferenceUp',TInterferenceDcm), ('tInterferenceDown',TInterferenceDcm)]
class SPuschTpcParamsUlDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('p0PuschInfoTable',prophy.bytes(size=SIZE_OF_P0_PUSCH_REF_TABLE_DCM)), ('averTimePuschI',EAverTimeInterferenceDcm), ('averTimeItpcRefI',EAverTimeInterferenceDcm), ('tttP0PuschTh',TTttP0PuxchThDcm), ('flagPuschTpcCommandReset',TBooleanDcm)]
class SCchInformationUlDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('maxNumOfMsg3',TMaxNumOfMsg3Dcm), ('nRach',TNRachDcm), ('flagPRACHposition',TFlagDcm), ('rbRachM3start0',TRbIndexDcm), ('rbRachM3start1',TRbIndexDcm), ('sizeRachM3RA',TSizeOfRaMsg3Dcm), ('sizeRachM3D',TSizeOfRaMsg3Dcm), ('numOfRbsRachM3RA',TNumOfRbsDcm), ('numOfRbsRachM3D',TNumOfRbsDcm), ('padding',prophy.u16)]
class SSpsTfUlDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('modulation',EModulationInfoDcm), ('persistentUlBundling',EUlBundlingDcm), ('payloadSize',TPayloadSizeDcm), ('numOfRbs',TNumOfRbsDcm), ('persistentTargetSir',TPersistentSirUlDcm)]
class SUlPersistentParamsUlDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('persistentTfUlTable',prophy.bytes(size=SIZE_OF_PERSISTENT_TF_UL_TABLE_DCM)), ('persistentUlTfrUpTable',prophy.bytes(size=SIZE_OF_PERSISTENT_ULTFR_TABLE_DCM)), ('persistentUlTfrDownTable',prophy.bytes(size=SIZE_OF_PERSISTENT_ULTFR_TABLE_DCM)), ('persistentTfrInitUlTable',prophy.bytes(size=SIZE_OF_PERSISTENT_TFR_INIT_UL_TABLE_DCM)), ('mcsIndexUl',prophy.bytes(size=SIZE_OF_UL_PERSISTENT_MCS_INDEX_TABLE_DCM)), ('numRbUl',prophy.bytes(size=SIZE_OF_UL_PERSISTENT_RB_NUM_TABLE_DCM)), ('padding',prophy.u16), ('persistentTttUlTh',EPersistentTimerDcm), ('persistentReconfigUlTimerTh',EPersistentTimerDcm), ('averTimePersistentSir',EAverTimePersistentSirUlDcm), ('ulTalkSpurtUpperDataTh',TDataSizeDcm), ('ulTalkSpurtLowerDataTh',TDataSizeDcm), ('rbPersistent0',TNumOfRbsDcm), ('rbPersistent1',TNumOfRbsDcm), ('numOfMaxTxTh',TNumOfMaxTxThDcm), ('weightRachMsg3',TWeightPersistentUlDcm), ('weightPersistentUl',TWeightPersistentUlDcm), ('averTimeRachMsg3RBUsage',TAverTimeRbUsageDcm), ('averTimePersistentUlRBUsage',TAverTimeRbUsageDcm), ('implicitReleaseAfter',TImplicitReleaseAfterDcm)]
class SSIULSpecificParamsDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('schedPriorityGroupIndexUl',ESchedPrioGroupIndexDcm), ('ulTargetDataRateMeas',TTargetDataRateMeasDcm), ('prioLcg',TPrioCoeffDcm), ('ulTargetDataRate',TTargetDataRateIndexDcm), ('ulFlagAMBR',TBooleanDcm), ('flagSCellSchedulingUl',TBooleanDcm)]
class SCoeffParamsLCGDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('siulSpecificParamsTable',prophy.bytes(size=SIZE_OF_SIUL_SPECIFIC_PARAMS_TABLE_DCM)), ('nonAllocTimeLowTh',TTimerDcm), ('nonAllocTimeHighTh',TTimerDcm), ('weightCoeffNonAllocTime',TPrioCoeffDcm), ('weightCoeffUlADR',TPrioCoeffDcm), ('forgettingFactorConvAdrUl',TForgettingFactorConvDcm), ('padding',prophy.u16)]
class SSirParamsLCGDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('deltaSirAdjUl',TSirAdjStepDcm), ('targetBlerUl',TTargetBlerDcm), ('powerOffsetSirUl',TPowerOffsetSirDcm), ('padding',prophy.u16)]
class SDcmLCGInfoCSDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('coeffParamsLCG',SCoeffParamsLCGDcm), ('sirParamsLCG',SSirParamsLCGDcm), ('nTmpUlBuffer',TNTmpUlBuffer), ('reserved1',prophy.u16)]
class SBackoffIndicatorInfoDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('thNumUp',TThNumDcm), ('thNumDown',TThNumDcm), ('thCntUp',TThCntDcm), ('thCntDown',TThCntDcm)]
class SPeriodicGrantInfoDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('periodicGrantTimer',EPeriodicGrantTimer), ('sizePeriodicGrant',prophy.u16), ('flagTbPeriodicGrant',TBooleanDcm), ('numTxCountUl',prophy.u16), ('numPduUl',prophy.u16), ('rbPeriodicGrant',prophy.u16), ('tfPeriodicGrant',prophy.u16), ('rbPeriodicGrantTb',prophy.u16), ('tfPeriodicGrantTb',prophy.u16), ('reserved1',prophy.u16), ('reserved2',prophy.u16)]
class SUlVoLteParamsDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('periodicGrantIndexRefTable',prophy.bytes(size=SIZE_OF_PERIODIC_GRANT_INDEX_REF_TABLE_DCM)), ('yPeriodicGrantInit',prophy.bytes(size=SIZE_OF_PERIODIC_GRANT_THRESHOLD)), ('yPeriodicGrant',prophy.bytes(size=SIZE_OF_PERIODIC_GRANT_THRESHOLD)), ('periodicGrantAveDmrsSTimer',EPeriodicGrantTimerDcm), ('periodicGrantControlTimer',EPeriodicGrantTimerDcm), ('talkSpurtOffTimer',ETalkSpurtOffTimerDcm), ('periodicGrantSizeMax',prophy.u16), ('periodicGranttInitIndex',prophy.u16), ('numProhibitPeriodicGrant',prophy.u16), ('numProhibitTbReconfig',prophy.u16), ('sizeHeaderAssumed',prophy.u16), ('reserved1',prophy.u16), ('reserved2',prophy.u16)]
class SAssuredPucchInfoUl(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('thTimeCqiRiDropForDcmAlgorithmUl',TThTimeCqiRiDropDcm), ('thTimeCqiRiDropForHst1Ul',TThTimeCqiRiDropDcm), ('thTimeCqiRiDropForHst3Ul',TThTimeCqiRiDropDcm), ('padding',prophy.u16), ('thTimeCqiRiDropForDcmAlgorithmUlSCell',EThTimeCqiRiDropForSCell), ('thTimeCqiRiDropForHst1UlSCell',EThTimeCqiRiDropForSCell), ('thTimeCqiRiDropForHst3UlSCell',EThTimeCqiRiDropForSCell)]
class SSrsIndexRestrictionInfoDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('thTARestrict',prophy.bytes(size=SIZE_OF_TA_RESTRICT_TABLE_DCM)), ('indexMinRestrictInit',prophy.bytes(size=SIZE_OF_TA_RESTRICT_TABLE_DCM)), ('indexMinRestrictLowPL',prophy.bytes(size=SIZE_OF_TA_RESTRICT_TABLE_DCM)), ('indexMinRestrictMiddlePL',prophy.bytes(size=SIZE_OF_TA_RESTRICT_TABLE_DCM)), ('indexMinRestrictHighPL',prophy.bytes(size=SIZE_OF_TA_RESTRICT_TABLE_DCM)), ('thPLRestrictLow',prophy.bytes(size=SIZE_OF_TA_RESTRICT_TABLE_DCM)), ('thPLRestrictHigh',prophy.bytes(size=SIZE_OF_TA_RESTRICT_TABLE_DCM)), ('rbMaxRestrictInit',prophy.bytes(size=SIZE_OF_TA_RESTRICT_TABLE_DCM)), ('rbMaxRestrictLowPL',prophy.bytes(size=SIZE_OF_TA_RESTRICT_TABLE_DCM)), ('rbMaxRestrictMiddlePL',prophy.bytes(size=SIZE_OF_TA_RESTRICT_TABLE_DCM)), ('rbMaxRestrictHighPL',prophy.bytes(size=SIZE_OF_TA_RESTRICT_TABLE_DCM))]
class SUlDcmMacPsContainerCSDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('prachTpcParamsUl',SPrachTpcParamsUlDcm), ('puschFreqHoppingInformation',SPuschFreqHoppingInformationDcm), ('srsBandwidthControlInfo',SSrsBandwidthControlInfoDcm), ('rbgOffsetControlInfo',SRbgOffsetControlInfoDcm), ('puschTpcParamsUl',SPuschTpcParamsUlDcm), ('cchInformationUl',SCchInformationUlDcm), ('ulPersistentParamsUl',SUlPersistentParamsUlDcm), ('dcmLCGInfoTable',prophy.bytes(size=MAX_NUM_OF_LCG_DCM)), ('backoffIndicatorInfo',SBackoffIndicatorInfoDcm), ('voLteUlParams',SUlVoLteParamsDcm), ('averTimeSRSI',EAverTimeSRSIDcm), ('averTimeSRSS',EAverTimeSRSSDcm), ('modulationSchemeMsg3',EModulationSchemeMsg3Dcm), ('rMinUl',ERMinDcm), ('ulRbAllocationMode',EAllocationModeDcm), ('coeffKs',EUCoeffKsDcm), ('averTimeDMRSS',EAverTimeDMRSSDcm), ('ueInactivityTimerIdleTh',TUeInactivityTimerDcm), ('fdEstimationUsage',EFDEstimationUsageDcm), ('guardRbLow',TGuardRbDcm), ('guardRbHigh',TGuardRbDcm), ('maxNumEmergCallsUl',TMaxNumEmergencyCallsDcm), ('prioSr',TPrioCoeffDcm), ('numUlHighPl',TNumOfRbsDcm), ('numUlLowPl',TNumOfRbsDcm), ('pathlossUlTh',TPathlossThDcm), ('ulTxTypeMode',TBooleanDcm), ('pathlossUlPhichTh',TPathlossThDcm), ('coeffPathloss',TCoeffPathlossDcm), ('coeffTFRS',TCoeffTfrsDcm), ('coefAdjust',TCqiAdjStepDcm), ('nRBUlBufferMin',TNRBUlBufferMin), ('pathlossDlTh',TPathlossThDcm), ('nUlMax',TMaxNumPdcchDlUlDcm), ('refPathloss',TPathlossThDcm), ('maxSirOffsetUl',TSirOffsetDcm), ('minSirOffsetUl',TSirOffsetDcm), ('plAperCQINotTriggered',TPathlossThDcm), ('pathlossUlThNoSRS',TPathlossThDcm), ('minAperiodicCqiMCS',TMCSIndexDcm), ('ttiBundlingSirOffset',TSirOffsetDcm), ('assuredPucchInfoUl',SAssuredPucchInfoUl), ('srsIndexRestrictionInfoDcm',SSrsIndexRestrictionInfoDcm), ('ulAmbrPeriod',EAmbrPeriodDcm), ('deltaPreambleMsg3',prophy.u16), ('minCostAMBR',TMinCostAMBRDcm), ('maxTbsAMBR',TMaxTbsAMBRDcm), ('flagRBReduction',TBooleanDcm), ('flagPhichHopping',TBooleanDcm), ('nUlCandidateMax',TNUlCandidateMax), ('alphaUlPDCCH',TAlphaUlPDCCH), ('betaUlPDCCHCommon',TBetaUlPDCCHCommon), ('gammaUlPDCCH',TGammaUlPDCCH), ('minPuschSir',TMinPuschSir), ('thSCellActivationUl1',EThSCellActivationUl1), ('thSCellActivationUl2',EThSCellActivationUl2), ('reserved1',prophy.u16), ('reserved2',prophy.u16), ('reserved3',prophy.u16), ('reserved4',prophy.u16)]
class SDcmCellContainerDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dlDcmMacPsContainerCS',SDlDcmMacPsContainerCSDcm), ('ulDcmMacPsContainerCS',SUlDcmMacPsContainerCSDcm)]
class SDcmCellReconfigurationContainerDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('txPowers',STxPowersDlDcm)]
class SSCellsParams(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCellIdScell',TCellIdDcm), ('lcpForCqiOffsetAdjSCell',prophy.u16)]
class STpcPdcchForPucchParamsDlDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('startOffsetForTpcPdcchForPucch',TTpcPdcchStartOffsetDcm), ('padding',prophy.u16), ('periodicityForTpcPdcchForPucch',ETpcPdcchPeriodicityDcm)]
class SDlDcmMacPsContainerUSDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numSSCellsParams',u16), ('sCellsParams',prophy.array(SSCellsParams,bound='numSSCellsParams')), ('padding',prophy.u16), ('tpcPdcchForPucchTpcParams',STpcPdcchForPucchParamsDlDcm), ('callTypeDl',ECallTypeDcm), ('initialUEInactivityTimerValue',TUeInactivityTimerDcm), ('maxPayloadSizeDlAmbr',TPayloadSizeDcm), ('ueInactivityTimerIdleTh',TUeInactivityTimerDcm), ('lcpForCqiOffsetAdj',TLcpDcm), ('p0UePucch',TP0UePucchDcm), ('initialNumProhibitDelayPacked',prophy.u16), ('initialMinDelayPackedIndex',prophy.u16)]
class STpcPdcchForPuschParamsUlDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('startOffsetForTpcPdcchForPusch',TTpcPdcchStartOffsetDcm), ('padding',prophy.u16), ('periodicityForTpcPdcchForPusch',ETpcPdcchPeriodicityDcm)]
class SUlDcmMacPsContainerUSDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tpcPdcchForPuschTpcParamsUl',STpcPdcchForPuschParamsUlDcm), ('callTypeUl',ECallTypeDcm), ('initialUEInactivityTimerValue',TUeInactivityTimerDcm), ('maxPayloadSizeUlAmbr',TPayloadSizeDcm), ('ueInactivityTimerIdleTh',TUeInactivityTimerDcm), ('lcgForSIROffsetAdj',TLcgDcm), ('ueMaxTxPower',TTxPowerAbsoluteDcm), ('tMaxNumHarqRetransmissionsUlSch',TMaxNumHarqRetransmissionsUlSchDcm), ('p0UePusch',TP0UePuschDcm), ('flagFirstBearerSetup',TBooleanDcm), ('initialPathloss',TPathlossThDcm), ('initialPeriodicGrantIndexandStatus',TPeriodicGrantIdxStsDCM), ('initialNumProhibitPeriodicGrant',prophy.u16), ('initialMinPeriodicGrantIndex',prophy.u16), ('initialDmrsSirForPeriodicGrant',prophy.u16), ('initialProhibitTbReconfig',prophy.u16), ('reserved4',prophy.u16)]
class SDcmUserContainerDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dlDcmMacPsContainerUS',SDlDcmMacPsContainerUSDcm), ('ulDcmMacPsContainerUS',SUlDcmMacPsContainerUSDcm)]
class SDlDcmMacPsContainerRbSDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('persistentDlEnable',TBooleanDcm), ('lcpDl',TLcpDcm), ('sidl',TSidlDcm), ('reserved1',prophy.u16), ('reserved2',prophy.u16), ('reserved3',prophy.u16), ('reserved4',prophy.u16), ('reserved5',prophy.u16)]
class SUlDcmMacPsContainerRbSDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('persistentUlEnable',TBooleanDcm), ('siul',TSiulDcm), ('reserved1',prophy.u16), ('reserved2',prophy.u16), ('reserved3',prophy.u16), ('reserved4',prophy.u16), ('reserved5',prophy.u16), ('padding',prophy.u16)]
class SDcmRbContainerDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dlDcmMacPsContaineRbS',SDlDcmMacPsContainerRbSDcm), ('ulDcmMacPsContainerRbS',SUlDcmMacPsContainerRbSDcm)]
class SSCellStatusParameters(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCellIdScell',TCellIdDcm), ('currentSCellStatus',TBooleanDcm), ('currentSCellInactivityTimer',prophy.u32)]
class SDcmUeStatusReportContainerDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numSCellStatusParameters',u16), ('sCellStatusParameters',prophy.array(SSCellStatusParameters,bound='numSCellStatusParameters')), ('padding',prophy.u16), ('ueIAT',TUeInactivityTimerDcm), ('pathloss',TPathlossThDcm), ('periodicGrantIndexandStatus',TPeriodicGrantIdxStsDCM), ('currentNumProhibitDelayPacked',prophy.u16), ('currentMinDelayPackedIndex',prophy.u16), ('currentNumProhibitPeriodicGrant',prophy.u16), ('currentMinPeriodicGrantIndex',prophy.u16), ('currentDmrsSirForPeriodicGrant',prophy.u16), ('currentProhibitTbReconfig',prophy.u16)]
class SDcmUlTfrParamContainerDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('srsBandwidth',ESrsBandwidthDcm), ('pSrsOffset',TPSrsOffsetRefDcm), ('flagTtiBundling',TBooleanDcm)]
class SDcmUlPowerControlUpdateIndContainerDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('powerType',EPowerTypeDcm), ('p0Power',TPowerDcm), ('padding',prophy.u16)]
class SDcmBackoffIndIndexUpdateIndContainerDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('updatedIndex',TIndexDcm), ('padding',prophy.u16)]
class SSiRepetitionDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('siType',ESiTypeDcm), ('siRepetitionBitmap',prophy.bytes(size=SIZE_OF_SI_BITMAP_DCM))]
class SDcmSystemInfoContainerDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numSi',TNumSiDcm), ('padding',prophy.u16), ('siRepetition',prophy.bytes(size=SIZE_OF_SI_REPETITION_TABLE_DCM))]
class SDcmUlResCtrlParamContainerDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tpcPdcchForPucchTpcParamsDl',STpcPdcchForPucchParamsDlDcm), ('tpcPdcchForPuschTpcParamsUl',STpcPdcchForPuschParamsUlDcm)]
class SDcmLCPInfoUSDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('prioLcp',TPrioCoeffDcm), ('dlTargetDataRate',TTargetDataRateIndexDcm)]
class SDcmLCGInfoUSDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('prioLcg',TPrioCoeffDcm), ('ulTargetDataRate',TTargetDataRateIndexDcm)]
class SRlcLcpInfoDcm(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('umReorderingBufferSize',EUmBufferSizeDcm), ('umTransmitBufferSize',EUmBufferSizeDcm), ('bufferingTimeTh',TThDcm), ('rlcDiscardTh',TThDcm)]
class SCaDcmSCellContainer(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sCellDeactivationTimer',ESCellDeactivationTimer), ('sCellDeactivationTimerEnb',ESCellDeactivationTimerEnb), ('sCellAddKeepFlag',prophy.u16), ('sCellInitialActiveDeactiveStatus',prophy.u16), ('thSCellRemove',prophy.u16), ('lcpForCqiOffsetAdjSCell',prophy.u16), ('initialSCellInactivityTimerR',prophy.u32)]
