import aprot


class MAC_CellSetupReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('phyCellId',TPhyCellId),('commonCellParams',SCommonCellParams),('phichParams',SPhichParams),('pucchParams',SPucchConfiguration),('soundingRsUlConfigCommon',SSoundingRsUlConfigCommon),('hsTrainScenario',EHsTrainScenario),('harqMaxMsg3',TOaMHarqMaxMsg3),('bufferDiscardParams',SBufferDiscardParams),('voLteThresholdParams',SVoLteThresholdParams),('rlcDlLcpInfo', aprot.bytes(size = MAX_NUM_OF_LCP_DCM)),('container',UWmpDcmCellContainer)]

class MAC_CellSetupResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('macUser',TAaSysComSicad),('macSgnl',TAaSysComSicad),('macCellMeas',TAaSysComSicad),('macTest',TAaSysComSicad),('macUserPsService',TAaSysComSicad)]

class MAC_CellReconfigurationReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('activationTimeSFN',TSfn),('commonCellParams',SCommonCellParams),('phichParams',SPhichParams),('pucchParams',SPucchConfiguration),('soundingRsUlConfigCommon',SSoundingRsUlConfigCommon),('hsTrainScenario',EHsTrainScenario),('harqMaxMsg3',TOaMHarqMaxMsg3),('container',UWmpDcmCellContainer)]

class MAC_CellReconfigurationResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TOaMLnCelId)]

class MAC_RachSetupReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('lCelId',TLocalCellResId),('rachParams',SRachParams)]

class MAC_RachSetupResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId)]

class MAC_CellDeleteReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId)]

class MAC_CellDeleteResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId)]

class MAC_TxAntennaConfChangeReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('numAvailableTxAntennas',TNumAntennas)]

class MAC_TxAntennaConfChangeResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId)]

class MAC_UserSetupReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('ueGroup',TUeGroup),('transactionId',TTransactionID),('lnCelIdSCell', aprot.bytes(size = 1)),('spsCrntiAllocationReq',TBoolean),('handoverType',EHandoverType),('ueSetupParams',SUeSetupParams),('container',UWmpDcmUserContainer),('cqiParams',SCqiParams),('controlOffsets',SPuschControlOffsets),('ueParams',SUeParams),('ttiBundlingEnable',TBoolean),('tpcPdcchConfigParams',STpcPdcchConfigParams),('ulPCUeParams',SUlPCUeParams),('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated),('sRbInfoList', aprot.bytes(size = MAX_NUM_SRB_PER_USER)),('rbInfoList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]

class MAC_UserSetupResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('ueGroup',TUeGroup),('transactionId',TTransactionID),('spsCrnti',TCrnti),('macUserAddress',TAaSysComSicad),('raPreambleIndex',TRaPreambleIndex),('prachMaskIndex',TPrachMaskIndex),('sRbList', aprot.bytes(size = MAX_NUM_SRB_PER_USER)),('dRbList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]

class MAC_L2CallConfigReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('ueGroup',TUeGroup),('transactionId',TTransactionID),('lnCelIdSCell', aprot.bytes(size = 1)),('spsCrntiAllocationReq',TBoolean),('handoverType',EHandoverType),('ueSetupParams',SUeSetupParams),('container',UWmpDcmUserContainer),('cqiParams',SCqiParams),('controlOffsets',SPuschControlOffsets),('ueParams',SUeParams),('ttiBundlingEnable',TBoolean),('tpcPdcchConfigParams',STpcPdcchConfigParams),('ulPCUeParams',SUlPCUeParams),('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated),('sRbInfoList', aprot.bytes(size = MAX_NUM_SRB_PER_USER)),('rbInfoList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]

class MAC_L2CallConfigResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('ueGroup',TUeGroup),('transactionId',TTransactionID),('spsCrnti',TCrnti),('macUserAddress',TAaSysComSicad),('raPreambleIndex',TRaPreambleIndex),('prachMaskIndex',TPrachMaskIndex),('sRbList', aprot.bytes(size = MAX_NUM_SRB_PER_USER)),('dRbList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]

class MAC_UserModifyReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('crnti',TCrnti),('ueId',TUeId),('measGapStopRequired',TBoolean),('gapPattern',EMeasGapOffset),('measGapOffset',TMeasGapOffset),('ambrParams',SAmbrParams),('drxParameters',SDrxParameters),('actNewTransmMode',ETransmMode),('cqiParams',SCqiParams),('ueInactivityTimer',TOaMInactivityTimer)]

class MAC_UserModifyResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TOaMLnCelId),('crnti',TCrnti),('ueId',TUeId)]

class MAC_UserDeleteReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('validUeId',TBoolean),('ueId',TUeId),('transactionId',TTransactionID),('spsCrntiReleaseReq',TBoolean),('ueReleaseCause',ECauseLte),('specificUeReleaseCause',ESpecificCauseLte)]

class MAC_UserDeleteResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID)]

class MAC_RadioBearerSetupReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID),('spsCrntiAllocationReq',TBoolean),('ueSetupParams',SUeSetupParams),('container',UWmpDcmUserContainer),('cqiParams',SCqiParams),('ueParams',SUeParams),('tpcPdcchConfigParams',STpcPdcchConfigParams),('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated),('sRbInfoList', aprot.bytes(size = MAX_NUM_SRB_PER_USER_WO_SRB1)),('drbInfoList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]

class MAC_RadioBearerSetupResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID),('spsCrnti',TCrnti),('container',UUlTfrParamContainer),('sRbList', aprot.bytes(size = MAX_NUM_SRB_PER_USER_WO_SRB1)),('dRbList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]

class MAC_RadioBearerDeleteReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID),('spsCrntiReleaseReq',TBoolean),('spsCrnti',TCrnti),('container',UWmpDcmUserContainer),('ueParams',SUeParams),('sRbList', aprot.bytes(size = MAX_NUM_SRB_PER_USER_WO_SRB1)),('dRbList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]

class MAC_RadioBearerDeleteResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID),('container',UUlTfrParamContainer),('sRbList', aprot.bytes(size = MAX_NUM_SRB_PER_USER_WO_SRB1)),('dRbList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]

class MAC_RadioBearerModifyReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID),('spsCrntiAllocationReq',TBoolean),('ueSetupParams',SUeSetupParams),('container',UWmpDcmUserContainer),('cqiParams',SCqiParams),('ueParams',SUeParams),('tpcPdcchConfigParams',STpcPdcchConfigParams),('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated),('cqiParamsScell', aprot.bytes(size = 1)),('sRbInfoList', aprot.bytes(size = MAX_NUM_SRB_PER_USER)),('rbInfoList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]

class MAC_RadioBearerModifyResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID),('spsCrnti',TCrnti),('container',UUlTfrParamContainer),('sRbList', aprot.bytes(size = MAX_NUM_SRB_PER_USER)),('dRbList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]

class MAC_TriggerInactivityInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('lnCellIdScell',TOaMLnCelId),('crnti',TCrnti),('ueId',TUeId),('direction',EDirection),('trigger',TTrigger)]

class MAC_DefaultUserConfigReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('l3Address',TAaSysComSicad),('userInfo',SUserInfoMac)]

class MAC_DefaultUserConfigResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('nodeAddress', aprot.bytes(size = MAX_NUM_OF_L2DEPLOYABLE_NODE))]

class MAC_PcchDataSendReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('pagingItems', aprot.bytes(size = MAX_PAGING_ITEMS))]

class MAC_CcchDataSendReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('data', aprot.bytes(size = MAX_CCCH_DATA))]

class MAC_CcchDataReceiveInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('msg3Info', aprot.bytes(size = MAX_MSG3_PER_TTI))]

class MAC_RadioLinkStatusInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('sCellServCellIndex',TSCellServCellIndex),('srbId',TSrbId),('drbId',TDrbId),('rlsCause',ERlsCause)]

class MAC_UlResourceControlReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID),('cqiParams',SCqiParams),('ueSetupParams',SUeSetupParams),('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated),('tpcPdcchConfigParams',STpcPdcchConfigParams),('container',UUlResCtrlParamContainer),('cqiParamsScell', aprot.bytes(size = 1))]

class MAC_UlResourceControlResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID),('sCellServCellIndex',TSCellServCellIndex),('container',UUlTfrParamContainer)]

class MAC_ErrorInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('sRbList', aprot.bytes(size = MAX_NUM_SRB_PER_USER)),('dRbList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]

class MAC_CrntiReserveReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crntiList', aprot.bytes(size = MAX_NUM_USER_PER_CELL))]

class MAC_CrntiReserveResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId)]

class MAC_CrntiFreeReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId)]

class MAC_CrntiFreeResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId)]

class MAC_SpsCrntiAllocationReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID)]

class MAC_SpsCrntiAllocationResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID),('spsCrnti',TCrnti)]

class MAC_SpsCrntiReleaseReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID),('spsCrnti',TCrnti)]

class MAC_SpsCrntiReleaseResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID)]

class MAC_SystemInfoScheduleReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('transactionId',TTransactionID),('activationTimePresent',TBoolean),('activationTime',TFrameNumber),('mibSfnPosition',TMibSfnPosition),('mibSfnLength',TMibSfnLength),('siWindowLen',EOaMSiWindowLen),('siSchedule', aprot.bytes(size = MAX_NUM_SIS)),('siList', aprot.bytes(size = MAX_NUM_SIS)),('container',USystemInfoContainer),('siTypeSegmented',ESysInfoTypeId),('siSegmentSize', aprot.bytes(size = MAX_NUM_SI_SEGMENT)),('siSegmentData', aprot.bytes(size = MAX_SI_SEGMENT_DATA))]

class MAC_SystemInfoScheduleResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('transactionId',TTransactionID)]

class MAC_SystemInfoInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('gpsTimeAvailable',TBoolean)]

class MAC_EnableSystemInfoReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('ibType',EIbType),('activationFlag',EActivationFlag)]

class MAC_EnableSystemInfoResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId)]

class MAC_SIB12BroadcastReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('transactionId',TTransactionID),('messageIdentifier',aprot.u16),('serialNumber',aprot.u16),('numberOfBroadcastsRequested',aprot.u16),('padding',aprot.u16),('repetitionPeriod',aprot.u32),('killFlag',TBoolean),('siSegmentSize', aprot.bytes(size = MAX_NUM_SI_SEGMENT)),('siSegmentData', aprot.bytes(size = MAX_SI_SEGMENT_DATA))]

class MAC_SIB12BroadcastResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('transactionId',TTransactionID),('messageIdentifier',aprot.u16),('serialNumber',aprot.u16),('messageResult',SMessageResult)]

class MAC_SIB12BroadcastInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('messageIdentifier',aprot.u16),('serialNumber',aprot.u16),('numberOfBroadcasts',aprot.u16)]

class MAC_BcchModIndReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('transactionId',TTransactionID),('activationTimePresent',TBoolean),('activationTime',TFrameNumber),('duration',SDuration),('pagingNb',EPagingNB),('pagingBitmapData', aprot.bytes(size = MAX_PAGING_BITMAP_DATA)),('data', aprot.bytes(size = MAX_PCCH_DATA))]

class MAC_BcchModIndResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('transactionId',TTransactionID),('activationTime',TFrameNumber)]

class MAC_UeStatusReportReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID)]

class MAC_UeStatusReportResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID),('container',UUeStatusReportRespContainerDcm)]

class MAC_UlTfrParamUpdateInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('container',UUlTfrParamContainer)]

class MAC_UlTfrParamReportReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID)]

class MAC_UlTfrParamReportResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID),('container',UUlTfrParamContainer)]

class MAC_UlPowerOffsetControlUpdateInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('container',UUlPowerControlUpdateIndContainer)]

class MAC_BackOffIndIndexUpdateInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('container',UBackoffIndIndexUpdateIndContainer)]

class MAC_RlcDataRegisterReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',TUeId),('tupUserAddress',STupUserAddress)]

class MAC_RlcDataRegisterResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('ueId',TUeId)]

class MAC_RlcDataReceiveInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('sRingBufferUlItem',SRingBufferUlItem)]

class MAC_RlcDataTestSupportReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('c',SRingBufferSendReq),('data', aprot.bytes(size = MAX_RLC_DATA))]

class MAC_RlcDataTestSupportUlReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('c',SRingBufferUlItem),('data', aprot.bytes(size = MAX_RLC_DATA))]

class MAC_RlcDataSendReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('sRingBufferSendReq',SRingBufferSendReq)]

class MAC_RlcDataSendResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueRbPacketIdList', aprot.bytes(size = MAX_NUM_SENDRESP_PACKET_IDS))]

class MAC_RlcDataDiscardInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueRbPacketId', aprot.bytes(size = MAX_NUM_PACKET_IDS))]

class MAC_StopSchedulingReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',TUeId),('handoverType',EHandoverType),('enableRlcBufferStateReport',TBoolean),('rbStopSchedulingInfo', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]

class MAC_StopSchedulingResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('ueId',TUeId),('bearerList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]

class MAC_StartSchedulingReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',TUeId)]

class MAC_StartSchedulingResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('ueId',TUeId)]

class MAC_StopSchedulingCellReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId)]

class MAC_StopSchedulingCellResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId)]

class MAC_RlcDataBufferResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('dlRbMasterParam',SRingBufferDlParam),('dlRbSlaveParam',SRingBufferDlParam),('ulRbMasterParam',SRingBufferUlParam)]

class MAC_InternalAddressReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('transactionId',TTransactionID),('nodeAddress',SNodeAddress)]

class MAC_InternalAddressResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('transactionId',TTransactionID)]

class MAC_MeasurementInitiationReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('measurementId',TMeasurementId),('reportPeriod',TPeriod),('samplingPeriod',TPeriod),('measurementGroupTypeList', aprot.bytes(size = MAX_MEAS_GROUP_TYPE_ID_MAC))]

class MAC_MeasurementInitiationResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('measurementId',TMeasurementId)]

class MAC_MeasurementReportInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('measurementId',TMeasurementId),('measurementGroupTypeList', aprot.bytes(size = MAX_MEAS_GROUP_TYPE_ID_MAC)),('measReportValue', aprot.bytes(size = MAX_NUM_MEAS_REPORT_VALUE_MAC))]

class MAC_MeasurementTerminationReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('measurementId',TMeasurementId)]

class MAC_MeasurementTerminationResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('measurementId',TMeasurementId)]

class MAC_CoefficientRequestReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('caBw', aprot.bytes(size = MAX_NUM_COEFF_BW))]

class MAC_CoefficientRequestResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('macCoefficientValues', aprot.bytes(size = MAX_NUM_COEFF_BW))]

class MAC_StartUlTestModelReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('referenceChannelNumber',EReferenceChannelNumber),('resourceBlockOffset',TResourceBlock),('reportingTimeInterval',TReportingTimeInterval),('harqUsed',TBoolean),('digitalOutputEnabled',TBoolean),('ulTestModelDigitalOutputParams',SUlTestModelsDigitalOutputParams),('additionalMeasurementParameters',UAdditionalMeasurementParameters)]

class MAC_StartUlTestModelResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId)]

class MAC_ThroughputMeasurementReportInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('resultStatus',EStatusLte),('throughputResult',TThroughputResult),('resultCounters',SResultCounters),('throughputResultStationaryUe',TThroughputResult),('resultCountersStationaryUe',SResultCounters)]

class MAC_StopUlTestModelReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId)]

class MAC_StopUlTestModelResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId)]

class MAC_StartUlCtrlChannelMeasReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('measType',EUlCtrlChannelMeasType),('reportingTimeInterval',TReportingTimeInterval),('receptionSubframe',TSubframes),('expectionSubframe',TSubframes),('ulCtrlChannelParams',UUlCtrlChannelParams)]

class MAC_StartUlCtrlChannelMeasResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId)]

class MAC_UlCtrlChannelMeasReportInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('resultStatus',EStatusLte),('UlCtrlChannelMeasCounters',SUlCtrlChannelMeasCounters),('container',UlCtrlChannelMeasReportContainer)]

class MAC_StopUlCtrlChannelMeasReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId)]

class MAC_StopUlCtrlChannelMeasResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId)]

class MAC_MeasGapStartReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID),('measGapOffset',UMeasGapOffset)]

class MAC_MeasGapStartResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID)]

class MAC_MeasGapStopReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID)]

class MAC_MeasGapStopResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID)]

class MAC_StartRfLoopTestReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('reportingTimeInterval',TReportingTimeInterval)]

class MAC_StartRfLoopTestResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId)]

class MAC_StopRfLoopTestReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId)]

class MAC_StopRfLoopTestResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId)]

class MAC_CellReconfigurationDeltaReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('dcmContainer',UWmpDcmCellReconfigurationContainer)]

class MAC_CellReconfigurationDeltaResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId)]

class MAC_DisableDiscTimerInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',TUeId),('ueIndex',TUeIndex)]

class MAC_ResumeDiscTimerInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',TUeId),('ueIndex',TUeIndex)]

class MAC_RaPdcchOrderReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('crnti',TCrnti),('ueId',TUeId)]

class MAC_UeInfoReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('ueId',TUeId),('ueInfo',EUeInfo)]

class MAC_UeInfoResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TOaMLnCelId),('ueId',TUeId),('ueInfo',UUeInfo)]

class MAC_TestRlcDataInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',TUeId),('radioBearerId',TRadioBearerId),('size',TL3MsgSize),('data', aprot.bytes(size = 1))]

class MAC_StartRefSyncSReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId)]

class MAC_StartRefSyncSResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId)]

class MAC_StopRefSyncSReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId)]

class MAC_StopRefSyncSResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId)]

class MAC_RadioBearerReleaseInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLCelId),('ueList', aprot.bytes(size = MAX_NUM_OF_RELEASED_UES))]

class MAC_CongestionInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('gbrCongestionCause',ESpecificCauseLte),('numOfExceedingRb',aprot.u32),('cellResourceGroupId',TCellResourceGroupId)]

class MAC_CongestionIndAck(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('cellResourceGroupId',TCellResourceGroupId),('congestionResolutionResult',SMessageResult)]

class MAC_BearerModifyReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('crnti',TCrnti),('ueId',TUeId),('ttiBmMeasActivate',TBoolean),('ambrParams',SAmbrParams),('drbInfoList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]

class MAC_BearerModifyResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TOaMLnCelId),('crnti',TCrnti),('ueId',TUeId)]

class MAC_WmpMeasurementInitiationReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCellId',TCellId),('measurementGroupTypeList', aprot.bytes(size = MAX_MEAS_GROUP_TYPE_ID_MAC_WMP))]

class MAC_WmpMeasurementInitiationResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCellId',TCellId),('requestResult',SMessageResult),('measurementGroupTypeList', aprot.bytes(size = MAX_MEAS_GROUP_TYPE_ID_MAC_WMP)),('measReportValue', aprot.bytes(size = MAX_NUM_MEAS_REPORT_VALUE_MAC_WMP))]

class MAC_WmpMeasurementReportInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCellId',TCellId),('measurementGroupTypeList', aprot.bytes(size = MAX_MEAS_GROUP_TYPE_ID_MAC_WMP)),('measReportValue', aprot.bytes(size = MAX_NUM_MEAS_REPORT_VALUE_MAC_WMP))]

class MAC_WmpMeasurementTerminationReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId)]

class MAC_WmpMeasurementTerminationResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId)]

class MAC_PowerHeadroomBundledInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('frameNumber',TFrameNumber),('subFrameNumber',TSubFrameNumber),('uePhrList', aprot.bytes(size = MAX_NUM_OF_USERS_IN_TTI))]

class MAC_CaUserReconfigurationReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('crnti',TCrnti),('ueId',TUeId),('relatedProcedure',ERelatedProcedure),('aperiodicCsiTriggerParams',SAperiodicCsiTriggerParams),('container',UCaUserReconfigurationContainer),('r10n1PucchAnCsList', aprot.bytes(size = 2)),('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated),('sCellsRemove', aprot.bytes(size = 1)),('sCellsConfiguration', aprot.bytes(size = 1))]

class MAC_CaUserReconfigurationResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('crnti',TCrnti),('ueId',TUeId),('sCellResultsForRemoval', aprot.bytes(size = 1)),('sCellResultsForConfiguration', aprot.bytes(size = 1)),('messageResult',SMessageResult)]

class MAC_RrcConnectionReconfCompletedReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('ueId',TUeId),('relatedProcedure',ERelatedProcedure),('sCellServCellIndex',TSCellServCellIndex),('cqiParams',SCqiParams),('cqiParamsScell',SCqiParamsScell),('actNewTransmMode',ETransmMode),('actNewTransmModeScell',ETransmMode)]

class MAC_UlVoLteReceptionInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellId),('frameNumber',TFrameNumber),('subFrameNumber',TSubFrameNumber),('ueInfoList', aprot.bytes(size = MAX_NUM_OF_USERS_IN_TTI))]

class MAC_UserGroupReserveReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('ueId',TUeId)]

class MAC_UserGroupReserveResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TOaMLnCelId),('ueId',TUeId),('ueGroup',TUeGroup)]

class MAC_UserGroupFreeReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('ueId',TUeId),('ueGroup',TUeGroup)]

class MAC_UserGroupFreeResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TOaMLnCelId),('ueId',TUeId)]

class MAC_BufferStatusTriggerReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellId),('lnCellIdServCell',TOaMLnCelId),('frameNumber',TFrameNumber),('subFrameNumber',TSubFrameNumber)]

class MAC_BundledContentionResInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('numberOfContResMsg',TNumberOfItems),('pduMuxContentionResInd', aprot.bytes(size = MAX_NUM_CONT_RES_PER_MSG))]

class MAC_ConfigChangeInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('ueIndex',TUeIndex),('hasDrxConfigId',TBooleanU8),('drxConfigId',TConfigurationId)]

class MAC_CcchDataInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellId),('crnti',TCrnti),('ueIndex',TUeIndex),('size',TL3MsgSize),('tempUeNeeded',TBoolean),('macCeFlag',TBoolean)]

class MAC_DlBufferStatusBundleInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellId),('numOfLchHaveData',TNumOfLch),('dlBsr', aprot.bytes(size = 1))]

class MAC_HarqReleaseReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellId),('frameNumber',TFrameNumber),('subFrameNumber',TSubFrameNumber),('harqReleaseInfo', aprot.bytes(size = 1))]

class MAC_MacCrntiCeInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellId),('crnti',TCrnti),('tempCrnti',TCrnti),('ueIndex',TUeIndex),('tempUeIndex',TUeIndex),('frameNumber',TFrameNumber),('subFrameNumber',TSubFrameNumber)]

class MAC_MeasInitReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('reportClientSicad',TAaSysComSicad),('cellId',TCellId),('reportId',TMeasurementReportId),('period',TPeriod),('samplingPeriod',TPeriod),('groupList', aprot.bytes(size = 1))]

class MAC_MeasInitResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('reportId',TMeasurementReportId),('messageResult',SMessageResult)]

class MAC_MeasReportInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('reportId',TMeasurementReportId),('measurementValues', aprot.bytes(size = 1))]

class MAC_MeasTermInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId)]

class MAC_MeasTermReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellId),('reportId',TMeasurementReportId)]

class MAC_MeasTermResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('reportId',TMeasurementReportId),('messageResult',SMessageResult)]

class MAC_OverloadInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellId),('numberOfOverloadTtis',TNumberOfItems),('maxNumberOfUesPerOverloadTti',TNumberOfItems)]

class MAC_PduMuxBundledDataReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellIdU16),('frameNumber',aprot.u16),('subFrameNumber',aprot.u8),('cfi',TCfiU8),('lastTbInTti',TBooleanU8),('latencyBudgetExceeded',TBooleanU8),('numOfBundledPduMuxMsgs',aprot.u8),('data', aprot.bytes(size = 1))]

class MAC_PduMuxDataResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('frameNumber',aprot.u16),('subFrameNumber',aprot.u16),('resLength',aprot.u32),('resArray', aprot.bytes(size = 1))]

class MAC_TCrntiDeleteInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellId),('crnti',TCrnti),('ueIndex',TUeIndex),('frameNumber',TFrameNumber),('subFrameNumber',TSubFrameNumber),('sendDeleteReqToMacData',TBoolean)]

class MAC_UlBufferStatusInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('header',SMacMessageHeader),('payload',SUlBufStatusIndPayload)]

class MAC_UlDataReceivedReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('data', aprot.bytes(size = 1))]

class MAC_UlDataReceivedResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('data', aprot.bytes(size = 1))]

class MAC_AddressConfigReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('transactionId',TTransactionID),('poolId',TPoolId),('enbId',TOaMLnBtsId),('poolInfo', aprot.bytes(size = MAX_NUM_OF_POOLS_IN_SUPER_POOL))]

class MAC_AddressConfigResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('transactionId',TTransactionID),('serviceInfo', aprot.bytes(size = MAX_NUM_OF_TESTABILITY_SERVICES))]

class MAC_CaCellConfigReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('poolId',TPoolId),('transactionId',TTransactionID),('typeOfOperation',ECATypeOfOperation),('l2DlPhyAddressess',SL2DlPhyAddressess),('l2MacPsAddresses',SL2MacPsAddresses)]

class MAC_CaCellConfigResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TOaMLnCelId),('poolId',TPoolId),('transactionId',TTransactionID)]

class MAC_UeMeasReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID)]

class MAC_UeMeasResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TOaMLnCelId),('crnti',TCrnti),('ueId',TUeId),('transactionId',TTransactionID),('roundTripDelayEstimate',aprot.u32)]

class MAC_RemoveUesInCellReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('pCelId',TOaMLnCelId),('ueToRemove', aprot.bytes(size = MAX_NUM_CA_UES))]

class MAC_RemoveUesInCellResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TOaMLnCelId)]

class MAC_CaUserReconfigurationCompleteReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TOaMLnCelId),('crnti',TCrnti),('ueId',TUeId),('procedureResults',ECAProcedureResults)]

class MAC_CaUserReconfigurationCompleteResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TOaMLnCelId),('crnti',TCrnti),('ueId',TUeId)]

class MAC_PduMuxExceptionInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('frameNumber',aprot.u16),('subFrameNumber',aprot.u16),('resLength',aprot.u32),('resArray', aprot.bytes(size = 1))]

	
	