import prophy 
from externals import *
from globals import *
from OAM_MERGED import *
from DCM_MAC_PS import *
from WMP_MAC_PS import *
from MAC import *
from PHY import *



PS_CellReconfigurationDeltaReq = MAC_CellReconfigurationDeltaReq
PS_CellReconfigurationDeltaResp = MAC_CellReconfigurationDeltaResp
PS_CellReconfigurationReq = MAC_CellReconfigurationReq
PS_CellReconfigurationResp = MAC_CellReconfigurationResp
PS_CellSetupReq = MAC_CellSetupReq
PS_DefaultUserConfigReq = MAC_DefaultUserConfigReq
PS_RachSetupReq = MAC_RachSetupReq
PS_StartRefSyncSReq = MAC_StartRefSyncSReq
PS_StartRefSyncSResp = MAC_StartRefSyncSResp
PS_StopRefSyncSReq = MAC_StopRefSyncSReq
PS_StopRefSyncSResp = MAC_StopRefSyncSResp
PS_StopSchedulingCellResp = MAC_StopSchedulingCellResp
PS_TxAntennaConfChangeReq = MAC_TxAntennaConfChangeReq
PS_TxAntennaConfChangeResp = MAC_TxAntennaConfChangeResp
PS_DisableDiscTimerInd = MAC_DisableDiscTimerInd
PS_ResumeDiscTimerInd = MAC_ResumeDiscTimerInd
PS_UlPhyDataAddressSetReq = PHY_UlPhyDataAddressResp
TDlPhyDataAddressResp = PHY_DlPhyDataAddressResp
TRoutingIndex = prophy.u32

class EUeIndexMgmtOperationType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EUeIndexMgmtOperationType_Allocate',0), ('EUeIndexMgmtOperationType_Reassign',1), ('EUeIndexMgmtOperationType_Free',2), ('EUeIndexMgmtOperationType_FreeAll',3), ('EUeIndexMgmtOperationType_GroupReserve',4), ('EUeIndexMgmtOperationType_GroupFree',5), ('EUeIndexMgmtOperationType_GroupFreeInternal',6), ('EUeIndexMgmtOperationType_AllocateSCellAdd',7), ('EUeIndexMgmtOperationType_AllocateSCellAddByHo',8)]
class ETypeOfOperation(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ETypeOfOperation_CaCellSetup',0), ('ETypeOfOperation_CaCellDelete',1)]
class EOperation(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EOperation_CellSetup',0), ('EOperation_RachSetup',1), ('EOperation_Delete',2)]

class SCellCarrierInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('dlChBw',ECarrierBandwidth), ('ulChBw',ECarrierBandwidth)]
class SMemBuffer(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('addressPtr',prophy.u32), ('sizeInBytes',TSize)]
class SMacPsAddresses(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ulCell',TAaSysComSicad), ('dlCell',TAaSysComSicad), ('ulScheduler',TAaSysComSicad), ('dlScheduler',TAaSysComSicad)]
class SL2Addresses(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numOfUeGroups',TNumberOfItems), ('dataCtrlDlData',prophy.bytes(size=MAX_NUM_UEGROUP_PER_BB_POOL)), ('dataCtrlDlBsr',prophy.bytes(size=MAX_NUM_UEGROUP_PER_BB_POOL))]
class SServingCellConfiguration(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sCellConfiguration',SSCellsConfiguration), ('ueIndexSCell',TUeIndex)]
class PS_CellDeleteReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId)]
class PS_CellDeleteResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('messageResult',SMessageResult)]
class PS_CellReconfigInternalReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('operation',EOperation), ('numCellsFsp',TNumberOfItems), ('numCellsFsp',TNumberOfItems), ('cellCarrierInfo',prophy.array(SCellCarrierInfo,bound='numCellsFsp'))]
class PS_CellReconfigInternalResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('operation',EOperation)]
class PS_CellSetupResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('cellId',TCellId), ('macSgnl',TAaSysComSicad), ('macCellMeas',TAaSysComSicad), ('macUserPs',TAaSysComSicad), ('dataCtrlDLPdcchClient',TAaSysComSicad)]
class PS_CrntiReleaseReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('ueIndex',TUeIndex)]
class PS_DlPhyDataAddressSetReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('dlPhyDataAddress',TDlPhyDataAddressResp), ('raContResoT',TRaContResoT)]
class PS_ExternalAddressSetReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('ueIndex',TUeIndex), ('tupUserAddress',STupUserAddress)]
class PS_HoUeAddReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('ueIndex',TUeIndex), ('numOfScellIds',TNumberOfItems), ('lnCelIdSCell',prophy.array(TOaMLnCelId,bound='numOfScellIds')), ('maxNumberOfHarqTransmissionsMsg3',TNumHarqTransmissions), ('ueSetupParams',SUeSetupParams), ('dcmContainer',UWmpDcmUserContainer), ('controlOffsets',SPuschControlOffsets), ('cqiParams',SCqiParams), ('handoverType',EHandoverType), ('ueParams',SUeParams), ('ttiBundlingEnable',TBoolean), ('tpcPdcchConfigParams',STpcPdcchConfigParams), ('ulPCUeParams',SUlPCUeParams), ('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated), ('numSRbs',TNumberOfItems), ('sRbInfoList',prophy.bytes(size=MAX_NUM_SRB_PER_USER)), ('numRbs',TNumberOfItems), ('rbInfoList',prophy.bytes(size=MAX_NUM_DRB_PER_USER))]
class PS_HoUeAddResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('ueIndex',TUeIndex)]
class PS_AddressConfigReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ulCellMac',TAaSysComSicad), ('ulSchedulerMac',TAaSysComSicad), ('dlCellMac',TAaSysComSicad), ('dlSchedulerMac',TAaSysComSicad), ('numOfUeGroups',TNumberOfItems), ('dataCtrlUl',prophy.bytes(size=MAX_NUM_UEGROUP_PER_BB_POOL)), ('dataCtrlDlData',prophy.bytes(size=MAX_NUM_UEGROUP_PER_BB_POOL)), ('dataCtrlDlBsr',prophy.bytes(size=MAX_NUM_UEGROUP_PER_BB_POOL)), ('puschReceiveRespUAddress',prophy.bytes(size=MAX_NUM_UEGROUP_PER_BB_POOL)), ('macUser',TAaSysComSicad), ('dataMeas',TAaSysComSicad), ('psCellClient',TAaSysComSicad), ('psUserDiscardClient',prophy.bytes(size=MAX_NUM_UEGROUP_PER_BB_POOL)), ('psUserClient',TAaSysComSicad), ('poolId',TPoolId), ('numOfPools',TNumberOfItems), ('poolInfo',prophy.array(SL2PoolInfo,bound='numOfPools'))]
class PS_AddressConfigResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('numOfUeGroups',TNumberOfItems), ('psUserUl',prophy.bytes(size=MAX_NUM_UEGROUP_PER_BB_POOL)), ('psUserDl',prophy.bytes(size=MAX_NUM_UEGROUP_PER_BB_POOL)), ('dataCtrlUlClient',prophy.bytes(size=MAX_NUM_UEGROUP_PER_BB_POOL)), ('dataCtrlDlClient',prophy.bytes(size=MAX_NUM_UEGROUP_PER_BB_POOL)), ('dataCtrlRachClient',prophy.bytes(size=MAX_NUM_UEGROUP_PER_BB_POOL)), ('psUserDisableDlAndSCell',TBoolean), ('numOfTestabilityServices',TNumberOfItems), ('serviceInfo',prophy.array(SServiceInfo,bound='numOfTestabilityServices'))]
class PS_RachParaReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('ueId',TUeId), ('crnti',TCrnti), ('numOfScellIds',TNumberOfItems), ('lnCelIdSCell',prophy.array(TOaMLnCelId,bound='numOfScellIds')), ('handoverType',EHandoverType), ('dedicRaPreExpT',TDedicRaPreExpT), ('ueGroup',TUeGroup), ('ttiBundlingEnable',TBoolean), ('intentionalContentionbasedRaEnabled',TBoolean)]
class PS_RachParaResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('messageResult',SMessageResult), ('ueId',TUeId), ('crnti',TCrnti), ('raPreambleIndex',TRaPreamble), ('prachMaskIndex',TPrachMaskIndex), ('ueIndex',TUeIndex)]
class PS_RachSetupResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('cellId',TCellId)]
class PS_RbAddReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('ueIndex',TUeIndex), ('crnti',TCrnti), ('ueSetupParams',SUeSetupParams), ('container',UWmpDcmUserContainer), ('cqiParams',SCqiParams), ('ueParams',SUeParams), ('tpcPdcchConfigParams',STpcPdcchConfigParams), ('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated), ('numSRbs',TNumberOfItems), ('sRbInfoList',prophy.bytes(size=MAX_NUM_SRB_PER_USER)), ('numRbs',TNumberOfItems), ('rbInfoList',prophy.bytes(size=MAX_NUM_DRB_PER_USER))]
class PS_RbAddResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('ueIndex',TUeIndex), ('container',UUlTfrParamContainer)]
class PS_RbDeleteReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('ueIndex',TUeIndex), ('container',UWmpDcmUserContainer), ('ueParams',SUeParams), ('numSRbs',TNumberOfItems), ('srbList',prophy.bytes(size=MAX_NUM_SRB_PER_USER)), ('sLogicalChannelList',prophy.bytes(size=MAX_NUM_SRB_PER_USER)), ('numRbs',TNumberOfItems), ('rbList',prophy.bytes(size=MAX_NUM_DRB_PER_USER)), ('logicalChannelId',prophy.bytes(size=MAX_LCID))]
class PS_RbDeleteResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('ueIndex',TUeIndex), ('container',UUlTfrParamContainer)]
class PS_RbModifyResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueIndex',TUeIndex), ('spsCrnti',TCrnti), ('container',UUlTfrParamContainer)]
class PS_StartSchedulingReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('ueIndex',TUeIndex)]
class PS_StopSchedulingCellReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('shutDownFlag',TBoolean)]
class PS_StopSchedulingReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('ueIndex',TUeIndex), ('handoverType',EHandoverType)]
class PS_StopUeReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('ueIndex',TUeIndex)]
class PS_StopUeResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('ueIndex',TUeIndex), ('messageResult',SMessageResult)]
class PS_UeDeleteReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('ueIndex',TUeIndex), ('crnti',TCrnti), ('validUeId',TBoolean)]
class PS_UeDeleteResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('cellId',TCellId), ('ueIndex',TUeIndex), ('crnti',TCrnti)]
class PS_UeReconfigReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('ueIndex',TUeIndex), ('handoverType',EHandoverType), ('ueSetupParams',SUeSetupParams), ('container',UWmpDcmUserContainer), ('controlOffsets',SPuschControlOffsets), ('cqiParams',SCqiParams), ('ueParams',SUeParams), ('ttiBundlingEnable',TBoolean), ('tpcPdcchConfigParams',STpcPdcchConfigParams), ('ulPCUeParams',SUlPCUeParams), ('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated), ('numSRbs',TNumberOfItems), ('sRbInfoList',prophy.bytes(size=MAX_NUM_SRB_PER_USER)), ('numRbs',TNumberOfItems), ('rbInfoList',prophy.bytes(size=MAX_NUM_DRB_PER_USER))]
class PS_UeReconfigResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('ueIndex',TUeIndex)]
class PS_DefaultUserConfigResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('cellId',TCellId)]
class PS_SrioBsrBufferAddrInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('ulSrioId',prophy.u16), ('ulSrioBsrAddr',prophy.bytes(size=4))]
class PS_RachUserSetupReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('subFrameNumber',TSubFrameNumber), ('RAPreambleList',SRaPreambleList)]
class PS_RachUserSetupResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('subFrameNumber',TSubFrameNumber), ('ueIndex',TUeIndex), ('RAPreambleList',SRaPreambleResList)]
class PS_UlUserPlaneReportInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueId',prophy.u16), ('crnti',prophy.u16), ('utUlsReceivedNonGbrBytes',prophy.u32), ('utUlsReceivedGbrBytes',prophy.u32), ('utMaxDelayUl',prophy.u16), ('utNumOfReceivedTxAll',prophy.u16), ('utNumOf1stTx',prophy.u16), ('utNumOfFailed1stTx',prophy.u16), ('utNumOfFailedLastTx',prophy.u16), ('utNumOfTtiPositiveUlBuf',prophy.u16), ('utMeanUlMcs',prophy.u8), ('utMeanPuschRssi',prophy.u8), ('utMeanPuschSinr',prophy.i8), ('utMeanPhr',prophy.i8), ('utMeanPucchRssi',prophy.u8), ('utMeanPdcchAggUl',prophy.u8), ('utMeanPdcchAggDl',prophy.u8)]
class PS_DlUserPlaneReportInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ueId',prophy.u16), ('crnti',prophy.u16), ('utDlsSentNonGbrBytes',prophy.u32), ('utDlsSentGbrBytes',prophy.u32), ('utMaxDelayDl',prophy.u16), ('utSingleCWTx',prophy.u16), ('utSingleCW1stTx',prophy.u16), ('utSingleCW1stTxNackDtx',prophy.u16), ('utSingleCWTxFailed',prophy.u16), ('utDualCWTx',prophy.u16), ('utDualCW1stTx',prophy.u16), ('utDualCW1stTxNackDtx',prophy.u16), ('utDualCWTxFailed',prophy.u16), ('utPdcchDtx',prophy.u16), ('utNumOfTtiPositiveDlBuf',prophy.u16), ('utMeanDeltaCqi',prophy.i16), ('utMeanLaWbCqi',prophy.u8)]
class PS_UeIndexMgmtReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('relatedPCell',TCellId), ('ueId',TUeId), ('crnti',TCrnti), ('operationType',EUeIndexMgmtOperationType), ('ueIndex',TUeIndex), ('ueGroup',TUeGroup)]
class PS_UeIndexMgmtResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('cellId',TCellId), ('ueId',TUeId), ('crnti',TCrnti), ('operationType',EUeIndexMgmtOperationType), ('ueIndex',TUeIndex), ('ueGroup',TUeGroup)]
class PS_BearerModifyReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('crnti',TCrnti), ('ueIndex',TUeIndex), ('ttiBmMeasActivate',TBoolean), ('ambrParams',SAmbrParams), ('numDrbs',TNumberOfItems), ('drbInfoList',prophy.array(SRbModifyInfo,bound='numDrbs'))]
class PS_BearerModifyResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TOaMLnCelId), ('crnti',TCrnti), ('ueIndex',TUeIndex)]
class PS_MeasGapStartReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueIndex',TUeIndex), ('transactionId',TTransactionID), ('measGapOffset',UMeasGapOffset)]
class PS_MeasGapStartResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueIndex',TUeIndex), ('transactionId',TTransactionID)]
class PS_MeasGapStopReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueIndex',TUeIndex), ('transactionId',TTransactionID)]
class PS_MeasGapStopResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueIndex',TUeIndex), ('transactionId',TTransactionID)]
class PS_RbModifyReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueIndex',TUeIndex), ('transactionId',TTransactionID), ('spsCrntiAllocationReq',TBoolean), ('ueSetupParams',SUeSetupParams), ('container',UWmpDcmUserContainer), ('cqiParams',SCqiParams), ('ueParams',SUeParams), ('tpcPdcchConfigParams',STpcPdcchConfigParams), ('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated), ('tmpName',TNumberOfItems), ('cqiParamsScell',prophy.array(SCqiParamsScell,bound='tmpName')), ('numSRbs',TNumberOfItems), ('sRbInfoList',prophy.array(SSrbInfo,bound='numSRbs')), ('numRbs',TNumberOfItems), ('rbInfoList',prophy.array(SRbInfo,bound='numRbs'))]
class PS_StartSchedulingResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('ueIndex',TUeIndex)]
class PS_StopSchedulingResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('ueIndex',TUeIndex), ('numBearers',TNumberOfItems), ('bearerList',prophy.array(SBearerList,bound='numBearers'))]
class PS_UeInfoReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('ueIndex',TUeIndex), ('ueInfo',EUeInfo)]
class PS_UeInfoResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TOaMLnCelId), ('ueIndex',TUeIndex), ('ueInfo',UUeInfo)]
class PS_UlResourceControlReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueIndex',TUeIndex), ('transactionId',TTransactionID), ('cqiParams',SCqiParams), ('ueSetupParams',SUeSetupParams), ('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated), ('tpcPdcchConfigParams',STpcPdcchConfigParams), ('container',UUlResCtrlParamContainer), ('tmpName',TNumberOfItems), ('cqiParamsScell',prophy.array(SCqiParamsScell,bound='tmpName'))]
class PS_UlResourceControlResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueIndex',TUeIndex), ('transactionId',TTransactionID), ('sCellServCellIndex',TSCellServCellIndex), ('container',UUlTfrParamContainer)]
class PS_UserModifyReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('crnti',TCrnti), ('ueIndex',TUeIndex), ('measGapStopRequired',TBoolean), ('gapPattern',EMeasGapOffset), ('measGapOffset',TMeasGapOffset), ('ambrParams',SAmbrParams), ('drxParameters',SDrxParameters), ('actNewTransmMode',ETransmMode), ('cqiParams',SCqiParams), ('ueInactivityTimer',TOaMInactivityTimer)]
class PS_UserModifyResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TOaMLnCelId), ('crnti',TCrnti), ('ueIndex',TUeIndex)]
class PS_RrcConnectionReconfCompletedReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('ueIndex',TUeIndex), ('relatedProcedure',ERelatedProcedure), ('sCellServCellIndex',TSCellServCellIndex), ('cqiParams',SCqiParams), ('cqiParamsScell',SCqiParamsScell)]
class PS_CaUserReconfigurationReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('crnti',TCrnti), ('ueId',TUeId), ('ueIndex',TUeIndex), ('relatedProcedure',ERelatedProcedure), ('aperiodicCsiTriggerParams',SAperiodicCsiTriggerParams), ('container',UCaUserReconfigurationContainer), ('tmpName',TNumberOfItems), ('r10n1PucchAnCsList',prophy.array(SR10n1PucchAnCsElement,bound='tmpName')), ('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated), ('tmpName',TNumberOfItems), ('sCellsRemove',prophy.array(SSCellsRemove,bound='tmpName')), ('tmpName',TNumberOfItems), ('servingCellConfiguration',prophy.array(SServingCellConfiguration,bound='tmpName'))]
class PS_CaUserReconfigurationResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('crnti',TCrnti), ('ueId',TUeId), ('ueIndex',TUeIndex), ('ueIndexSCell',TUeIndex), ('tmpName',TNumberOfItems), ('sCellResultsForRemoval',prophy.array(SSCellResultsParameters,bound='tmpName')), ('tmpName',TNumberOfItems), ('sCellResultsForConfiguration',prophy.array(SSCellResultsParameters,bound='tmpName')), ('messageResult',SMessageResult)]
class PS_RaPdcchOrderReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('crnti',TCrnti), ('ueIndex',TUeIndex)]
class PS_StopUesInCellReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('tmpName',TNumberOfItems), ('ueToStop',prophy.array(TUeIndex,bound='tmpName'))]
class PS_StopUesInCellResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('messageResult',SMessageResult)]
class PS_DeleteUesInCellReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('tmpName',TNumberOfItems), ('ueToDelete',prophy.array(TUeIndex,bound='tmpName'))]
class PS_DeleteUesInCellResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('messageResult',SMessageResult)]
class PS_TimerServiceExpiryInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('timerId',TMacTimerId)]
class PS_InitSetupCollectorInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellSetupBuffer',SMemBuffer), ('ueSetupBuffer',SMemBuffer), ('rbSetupBuffer',SMemBuffer)]
class PS_TtiTraceUdpConfigReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('destMacTable',prophy.bytes(size=8)), ('srcMacTable',prophy.bytes(size=8)), ('destIp',prophy.bytes(size=4)), ('srcIp',prophy.bytes(size=4)), ('destPortSize',u32), ('destPort',prophy.array(u32,bound='destPortSize'))]
class PS_UserDeleteInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('validUeId',TBoolean), ('ueId',TUeId), ('transactionId',TTransactionID), ('spsCrntiReleaseReq',TBoolean), ('ueReleaseCause',ECauseLte), ('specificUeReleaseCause',ESpecificCauseLte)]
class PS_CaUserReconfigurationCompleteReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('lnCelId',TOaMLnCelId), ('crnti',TCrnti), ('ueId',TUeId), ('ueIndex',TUeIndex), ('procedureResults',ECAProcedureResults)]
class PS_CaUserReconfigurationCompleteResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TOaMLnCelId), ('crnti',TCrnti), ('ueId',TUeId), ('ueIndex',TUeIndex)]
class PS_DlSdlInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('connectDistanceEstimate',prophy.u16), ('releaseDistanceEstimate',prophy.u16), ('sCellAciveDuration',prophy.u16), ('lastCqi',prophy.u8), ('enbTransmitPower',prophy.u16), ('macDlReTxBytes',prophy.u32), ('harqDlAttempts',prophy.u32), ('harqDlFailures',prophy.u32)]
class PS_UlSdlInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cellId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('averagePowerHeadroom',prophy.i8), ('lastPowerHeadroom',prophy.i8), ('sinrPuschEffective',prophy.u8), ('harqUlAttempts',prophy.u32), ('harqUlFailures',prophy.u32)]
