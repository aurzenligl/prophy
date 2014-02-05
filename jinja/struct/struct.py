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

class SAmbrParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ambrUl',TAmbr),('ambrDl',TAmbr)]

class SBitRateParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('minBitrateUl',TOaMMinBitrateUl),('minBitrateDl',TOaMMinBitrateDl),('maxBitrateUl',TOaMMaxBitrateUl),('maxBitrateDl',TOaMMaxBitrateDl)]

class SUserInfoMac(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('dedicRaPreParams',UDedicRaPreParams)]

class SSysInfoSchedule(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('siType',ESysInfoTypeId),('siPeriodicity',TSiPeriodicity),('siRepetition',TSiRepetition)]

class SSrbInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('srbId',TSrbId),('logicalChannelId',TLogicalChannelId),('logicalChannelGrId',TLogicalChannelGrId),('logicalChannelIndex',TLcp),('rlcMode',ERlcMode),('rlcAmParameters',SRlcAmParameters),('container',UWmpDcmSrbContainer)]

class SRbInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('drbId',TDrbId),('drbType',EDrbType),('logicalChannelId',TLogicalChannelId),('logicalChannelGrId',TLogicalChannelGrId),('logicalChannelIndex',TLcp),('rlcMode',ERlcMode),('rlcUmParameters',SRlcUmParameters),('rlcAmParameters',SRlcAmParameters),('container',UWmpDcmRbContainer)]

class SRlcUmParameters(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('umRlcSnFieldLengthDownlink',TSnFieldLength),('umRlcSnFieldLengthUplink',TSnFieldLength),('umTimerReordering',TTimerReordering)]

class SRlcAmParameters(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('amRlcPollPdu',EPollPDU),('amPollBytes',EPollByte),('amRlcTimerPollReTransmit',TTimerPollReTransmit),('amRlcTimerReordering',TTimerReordering),('amRlcTimerStatusProhibit',TTimerStatusProhibit),('maxRlcReTrans',TMaxRlcReTrans)]

class SRachParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('prachFreqOff',TPrachFreqOff),('prachConfIndex',TOaMPrachConfIndex),('raNondedPreamb',TRaNondedPreamb),('raPreambGrASize',ERaPreambGrASize),('raRespWinSize',ERaRespWinSize),('crntiParams',UCrntiParams),('raContResoT',ERaContResoT),('prachCS',TOaMPrachCS),('timerRaComp',TTimerRaComp),('raMsg3Thr',TRaMsg3Thr),('raMsg3ThrLowParameters',SRaMsg3ThrLowParameters),('raMsg3ThrCntParameters',SRaMsg3ThrCntParameters),('prachHsFlag',TBoolean)]

class STupUserAddress(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('dlTupUserAddress',TAaSysComSicad)]

class SSiList(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('siType',ESysInfoTypeId),('data', aprot.bytes(size = MAX_SI_DATA))]

class SDRbList(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('drbId',TDrbId),('messageResult',SMessageResult)]

class SPduTimeStamp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('frameNumber',TFrameNumber),('subFrameNumber',TSubFrameNumber)]

class SPagingItem(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('frameNumber',TFrameNumber),('subFrameNumber',TSubFrameNumber),('data', aprot.bytes(size = MAX_PCCH_DATA))]

class SFrameConfTdd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('tddFrameConf',TOaMTddFrameConf),('tddSpecSubfConf',TOaMTddSpecSubfConf)]

class SCommonCellParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lCelId',TLocalCellResId),('dlChBw',ECarrierBandwidth),('ulChBw',ECarrierBandwidth),('pMax',TMaxTxPower),('dlPhyDataAddress',TAaSysComSicad),('ulPhyDataAddress',TAaSysComSicad),('maxNrSymPdcch',TOaMMaxNrSymPdcch),('taTimer',ETimeAlignTimer),('taMaxOffset',TTaMaxOffset),('dlMimoMode',EDlMimoMode),('cycPrefixDl',TCycPrefix),('cycPreFixUl',TCycPrefix),('frameConfTdd',SFrameConfTdd)]

class SPhichParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('phichRes',EOaMPhichRes),('phichDur',EOaMPhichDur)]

class SCrntiParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('raContResoT',ERaContResoT),('raCrntiReuseT',TOaMRaCrntiReuseT)]

class SDcmDedicRaParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('dedicRaPreExpT',TDedicRaPreExpT),('dedicRaPreIHoT',TDedicRaPreExpT)]

class SCqiParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cqiAperMode',ECqiAperMode),('cqiPerEnable',ECqiPerEnable),('numOfCqiPmi',aprot.u32),('iCqiPmi', aprot.bytes(size = MAX_NUM_OF_RI_PMI_INFORMATION)),('resourceIndexCqi',TResourceIndexCqi),('cqiPerMode',ECqiPerMode),('riEnable',TBoolean),('numOfRi',aprot.u32),('iRi', aprot.bytes(size = MAX_NUM_OF_RI_PMI_INFORMATION)),('cqiPerSimulAck',ECqiPerSimulAck),('cqiPerSbCycK',TCqiPerSbCycK),('cqiPerSbPeriodFactor',EOaMCqiPerSbPeriodFactor)]

class SDrxParameters(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('drxCommEnable',EDrxCommEnable),('drxLongEnable',TBoolean),('drxStartOffset',TDrxStartOffset),('drxOnDuratT',TDrxOnDuratT),('drxInactivityT',TDrxInactivityT),('drxRetransT',TDrxRetransT),('drxLongCycle',TDrxLongCycle),('drxShortEnable',TBoolean),('drxShortCycle',TDrxShortCycle),('drxShortCycleTimer',TDrxShortCycleTimer),('smartStInactFactor',TSmartStInactFactor),('drxProfileIndex',aprot.u32),('drxConfigType',EDrxConfigType),('drxConfigId',TConfigurationId)]

class SSoundingRsUlConfigDedicated(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('enableSRS',TBoolean),('srsBandwidth',TSrsBandwidth),('srsHoppingBw',TSrsHoppingBw),('freqDomPos',TFrequencyDomainPosition),('srsDuration',TBoolean),('srsConfIndex',TSrsConfIndex),('transComb',TTransmissionComb),('cyclicShift',TCyclicShift)]

class SSoundingRsUlConfigCommon(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('enableSRS',TBoolean),('srsBwConf',TSrsBandwidthConfiguration),('srsSubfrConf',TSrsSubframeConfiguration),('anSrsSimulTx',TBoolean),('srsMaxUpPts',TOaMSrsMaxUpPts)]

class SUeHoParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueCategory',TUeCategory),('ueCategoryR10',TUeCategory),('ambrParams',SAmbrParams),('bitRateParams',SBitRateParams),('drxParameters',SDrxParameters)]

class SUeParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('transmMode',ETransmMode),('accessStratumRelease',EUeRelease),('ueHoParams',SUeHoParams)]

class SSRbList(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('srbId',TSrbId),('messageResult',SMessageResult)]

class SUeSetupParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('srEnable',TBoolean),('pucchResourceIndex',TPucchResourceIndex),('srPeriod',ESrPeriod),('srOffset',TSrOffset)]

class SDuration(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('bcchModPeriodLength',TBcchModPeriodLength),('bcchModPeriodNumber',TBcchModPeriodNumber)]

class SSpsCrntiReleaseInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('status',EStatusLte),('specificCause',ESpecificCauseLte)]

class SSiSegmentSize(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('siSegmentSize',TL3MsgSize)]

class SMacCoefficientValues(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('caBw',ECarrierBandwidth),('cDlMac1',TCoEffValue),('cDlMac2',TCoEffValue),('cDlMac3',TCoEffValue),('cUlMac1',TCoEffValue),('cUlMac2',TCoEffValue),('cUlMac3',TCoEffValue),('cDlMacPs1',TCoEffValue),('cDlMacPs2',TCoEffValue),('cDlMacPs3',TCoEffValue),('cDlMacPs4',TCoEffValue),('cUlMacPs1',TCoEffValue),('cUlMacPs2',TCoEffValue),('culMacPs3',TCoEffValue),('cUlMacPs4',TCoEffValue)]

class SRlcLcpInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('umReorderingBufferSize',TBufferSize),('umTransmitBufferSize',TBufferSize),('bufferingTimeTh',TThresholdRlcT),('rlcDiscardTh',TThresholdRlc)]

class STpcPdcchConfigParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('tpcPucchRnti',TTpcRnti),('tpcPucchIndexOfFormat3',TTpcIndex),('tpcPuschRnti',TTpcRnti),('tpcPuschIndexOfFormat3',TTpcIndex)]

class SRbStopSchedulingInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('drbId',TDrbId),('dataForwardingType',EDataForwarding)]

class SUeRbPacketId(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',TUeId),('radioBearerId',TRadioBearerId),('packetId',TPacketId)]

class SRingBufferDlParam(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('destinationSrioId',TAaSysComNid),('addressLastReadMarkerPtr',aprot.u32),('startAddressBlocks',aprot.u32),('lengthBlocks',aprot.u32)]

class SRingBufferUlParam(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('destinationSrioId',TAaSysComNid),('addressLastReadMarkerPtr',aprot.u32),('startAddressBlocks',aprot.u32),('lengthBlocks',aprot.u32)]

class SRingBufferSendReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',aprot.u16),('radioBearerId',aprot.u8),('validDrxConfigId',aprot.u8),('drxConfigId',TConfigurationId),('packetId',aprot.u16),('frameNumber',aprot.u16),('harqRespFlag',aprot.u8),('subFrameNumber',aprot.u8),('size',aprot.u16),('dataPtr',aprot.u32)]

class SRingBufferDlCtrl(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('sendReq', aprot.bytes(size = MAX_RINGBUF_CTRL_DL)),('padding',aprot.u32),('nextMarkerPtr',aprot.u32),('marker',aprot.u32)]

class SRingBufferDlPayload(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('d', aprot.bytes(size = SIZE_RINGBUF_PAYLOAD_DL))]

class SRingBufferDlBlock(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('data',SRingBufferDlPayload),('ctrl',SRingBufferDlCtrl)]

class SRingBufferUlItem(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',aprot.u16),('radioBearerId',aprot.u8),('subFrameNumber',aprot.u8),('frameNumber',aprot.u16),('lastUlSdu',aprot.u8),('unused1',aprot.u8),('unused2',aprot.u16),('size',aprot.u16),('dataPtr',aprot.u32)]

class SRingBufferUlCtrl(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('item', aprot.bytes(size = MAX_RINGBUF_CTRL_UL)),('totalPayloadLen',aprot.u32),('nextMarkerPtr',aprot.u32),('marker',aprot.u32)]

class SRingBufferUlPayload(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('d', aprot.bytes(size = SIZE_RINGBUF_PAYLOAD_UL))]

class SRingBufferUlBlock(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('data',SRingBufferUlPayload),('ctrl',SRingBufferUlCtrl)]

class SMeasurementA7or8(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('enableTwoUserMeasurement',TBoolean),('stationaryUeResources',TBoolean)]

class SUlTestModelConfig(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('noOfHarqTransmissions',ENoOfHarqTransmissions),('hstConfig',EHstConfig),('resourceIndexCqi',TResourceIndexCqi),('iCqiPmi',TICqiPmi)]

class SMeasurementDcm5toDcm8(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('mcsIndex',aprot.u32)]

class SBearerList(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('drbId',TDrbId),('packetId',TPacketId)]

class SRbUePacketId(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('rlcDataSendRespCause',ERlcDataSendRespCause),('ueId',TUeId),('radioBearerId',TRadioBearerId),('packetIdLow',TPacketId),('packetIdHigh',TPacketId)]

class SBufferDiscardParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('thOverflowDiscard',TThOverflowDiscard),('flagOverflowDiscard',TFlagOverflowDiscard),('discBuffThrAct',TBoolean),('discBuffHighThr',TDiscBuffThr)]

class SMsg3Info(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('crnti',TCrnti),('ueGroup',TUeGroup),('data', aprot.bytes(size = MAX_CCCH_DATA_UL))]

class SNodeAddress(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ulCellMac',TAaSysComNid),('ulUeMac',TAaSysComNid),('ulSchedulerMac',TAaSysComNid),('dlCellMac',TAaSysComNid),('dlUeMac',TAaSysComNid),('dlSchedulerMac',TAaSysComNid),('cellManager',TAaSysComNid)]

class SUeList(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',TUeId),('drbIdList', aprot.bytes(size = 4)),('bearerReleaseIndCause',ESpecificCauseLte)]

class SRbModifyInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('drbId',TDrbId),('congestionWeight',aprot.u32),('qciInfo',SRbModifyQciInfo)]

class SRbModifyQciInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('schedulWeight',TSchedulingWeight),('qci',aprot.u32)]

class SUePhr(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueIndex',TUeIndex),('paddingUeIndex',aprot.u16),('crnti',aprot.u16),('powerLevel',aprot.u16)]

class SAmountOctets(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('rbId',TRadioBearerId),('isDataOctetsLeft',aprot.u8),('isCtrlOctetsLeft',aprot.u8)]

class SDlTbAttributes(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('maxNumOfHarqTx',TNumHarqTransmissions),('ndiForPdcch',TNewDataIndicator)]

class SCaCqiParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cqiParams',SCqiParams),('cqiParamsWmp',SCqiParamsWmp)]

class SVoLteThresholdParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ulTalkSpurtUpperDataTh',TDataSize),('ulTalkSpurtLowerDataTh',TDataSize)]

class SR10n1PucchAnCsElement(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('pucchResourceIndex', aprot.bytes(size = 4))]

class SDrxShortParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('drxShortEnable',TBoolean),('drxShortCycle',TDrxShortCycle),('drxShortCycleTimer',TDrxShortCycleTimer),('smartStInactFactor',TSmartStInactFactor)]

class SUeInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('crnti',TCrntiU16),('ueIndex',TUeIndex)]

class SDlSchPduMuxCwAttributes(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('tbSize',TTbSize),('drxCommEnable',TBooleanU8),('ueTaCeAvail',TBooleanU8),('ueTaCeValue',aprot.u16),('ueCaCeInfo',SCaCeInfo),('tfi',TMcs),('modulation',TEModulationU8),('newDataIndicator',TNewDataIndicatorU8),('redundancyVersion',TRedundancyVersionU8),('codeWordIndex',TCodeWordIndexU8),('harqIdCw',THarqProcessNumberU8),('trnumCw',aprot.u8),('amountRbs',aprot.u8),('amountRbOctets', aprot.bytes(size = MAX_NUM_RB_PER_USER))]

class SDlSchPduMuxAmountOctets(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('logicalChannelId',aprot.u16),('ctrl',aprot.u16),('data',aprot.u16)]

class SHarqReleaseInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('servingCellIndex',aprot.u8),('ueIndex',TUeIndex),('crnti',aprot.u16),('harqId1',aprot.u8),('harqId2',aprot.u8),('validHarqId1',aprot.u8),('validHarqId2',aprot.u8),('ackReceivedHarqId1',aprot.u8),('ackReceivedHarqId2',aprot.u8),('lnCellIdServCell',TOaMLnCelId)]

class SMgmtMeasurement(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('val',aprot.u32),('offsetInGroup',aprot.u16),('groupId',aprot.u8),('status',aprot.u8)]

class SPduMuxDataResultEntry(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('crnti',TCrntiU16),('ueIndex',TUeIndex),('cw0',EPduMuxDataResultCause),('cw1',EPduMuxDataResultCause)]

class SMacMessageHeader(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',TCellId),('frameNumber',TFrameNumber),('subFrameNumber',TSubFrameNumber),('srioDioBufferAddr',aprot.u32),('srioDioBufferSize',aprot.u32)]

class SUlBufStatusIndPayload(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueIdInfo', aprot.bytes(size = MAX_NUM_OF_USERS_IN_TTI))]

class SUeBufferStatus(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueIndex',TUeIndex),('crnti',TCrntiU16),('usefulDataReceived',TBooleanU8),('numBearerIdList',aprot.u8),('dtchMacSduReceived',TBooleanU8),('harqProcessNumber',THarqProcessNumberU8),('lcgIdList', aprot.bytes(size = MAX_NUM_LCG_IDS)),('bearerIdList', aprot.bytes(size = MAX_NUM_GBR_BEARER_PER_UE))]

class SLcgIds(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueBufferStatusReport',TBufferSize),('receivedDataSize',TBufferSize)]

class SBearerIds(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('drbId',TRadioBearerIdU8),('lcgId',TLogicalChannelGrIdU8),('rcvdData',aprot.u16)]

class SContentionResInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('cellId',aprot.u16),('crnti',aprot.u16),('ueIndex',TUeIndex),('raEvent',aprot.u8),('ueContentionResolutionId',aprot.u64)]

class SDlBufferStatusInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('amountDataOctets',aprot.u32),('amountOfRlcSduData',aprot.u32),('amountCtrlOctets',aprot.u16),('ueIndex',TUeIndex),('rbId',TRadioBearerIdU8),('lcId',TLogicalChannelIdU8),('xsfnTimeStamp',aprot.u16)]

class SUeBufferStatusWmp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('crnti',TCrnti),('ueIndex',TUeIndex),('usefulDataReceived',TBooleanU8),('lcgIdList', aprot.bytes(size = MAX_NUM_LCG_IDS))]

class SLcgIdsWmp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueBufferStatusReport',TBufferSize),('receivedDataSize',TBufferSize)]

class SCaCeInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('caCeAvail',TBooleanU8),('caCeValue',TCaCeValue),('unused',aprot.u16)]

class SPduMuxDataReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueIndex',TUeIndex),('macId',TCrntiU16),('txPower',TTxPower),('spatialMode',TSpatialMode),('numOfLayers',TNumOfLayersU8),('codebookIndex',TCodebookIndexU8),('nIr',TNIr),('resources',SPdschResources),('mimoIndicator',TBooleanU8),('servingCellIndex',TServingCellIndex),('lnCellIdServCell',TOaMLnCelId),('reqType',TEPduMuxReqTypeU8),('hasDlBfTbFormat',TBooleanU8),('dlBfTbFormat',SDlBfTbFormat),('tbFlags',aprot.u32),('cwAttributes', aprot.bytes(size = MAX_NMBR_CODEWORDS))]

class SDataReceived(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('crnti',TCrntiU16),('ueIndex',TUeIndex)]

class SPrachUsageRatio(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfGroupARAPreambleReceived',TMeasurementValue),('nbrOfGroupBRAPreambleReceived',TMeasurementValue),('nbrOfRAPreambleReceivedDedicPreamble',TMeasurementValue),('nbrOfRARespTransmitForGroupAPreamble',TMeasurementValue),('nbrOfRARespTransmitForGroupBPreamble',TMeasurementValue),('nbrOfRARespTransmitForDedicPreamble',TMeasurementValue),('nbrOfAssignNGDedicPreambleSyncReq',TMeasurementValue),('nbrOfOpportDedicPreambleReception',TMeasurementValue),('nbrOfDedicPreambleAllocated',TMeasurementValue),('nbrOfOpportGroupARAPreambleRecept',TMeasurementValue),('nbrOfOpportGroupBRAPreambleRecept',TMeasurementValue)]

class STransmittedAndReceivedPower(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('phichTransmitPower',TMeasurementValue),('transmitPowerOfControlPart',TMeasurementValue),('totalTransmitPowerBranch1',TMeasurementValue),('totalTransmitPowerBranch2',TMeasurementValue),('receivedTotalPowerBranch1',TMeasurementValue),('receivedTotalPowerBranch2',TMeasurementValue)]

class SMacPduTransmissionRate(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('dlMacPduTransmissionRate1',TMeasurementValue),('dlMacPduTransmissionRate2',TMeasurementValue),('dlMacPduTransmissionRate3',TMeasurementValue),('dlMacPduTransmissionRate4',TMeasurementValue),('dlMacPduTransmissionRate5',TMeasurementValue),('dlMacPduTransmissionRate6',TMeasurementValue),('dlMacPduTransmissionRate7',TMeasurementValue),('dlMacPduTransmissionRate8',TMeasurementValue),('dlMacPduTransmissionRate9',TMeasurementValue),('dlMacPduTransmissionRate10',TMeasurementValue),('dlMacPduTransmissionRate11',TMeasurementValue),('dlMacPduTransmissionRate12',TMeasurementValue),('dlMacPduTransmissionRate13',TMeasurementValue),('dlMacPduTransmissionRate14',TMeasurementValue),('dlMacPduTransmissionRate15',TMeasurementValue),('dlMacPduTransmissionRate16',TMeasurementValue),('dlMacPduTransmissionRate17',TMeasurementValue),('dlMacPduTransmissionRate18',TMeasurementValue),('dlMacPduTransmissionRate19',TMeasurementValue),('dlMacPduTransmissionRate20',TMeasurementValue),('dlMacPduTransmissionRate21',TMeasurementValue),('dlMacPduTransmissionRate22',TMeasurementValue),('dlMacPduTransmissionRate23',TMeasurementValue),('dlMacPduTransmissionRate24',TMeasurementValue),('dlMacPduTransmissionRate25',TMeasurementValue),('dlMacPduTransmissionRate26',TMeasurementValue),('dlMacPduTransmissionRate27',TMeasurementValue),('dlMacPduTransmissionRate28',TMeasurementValue),('dlMacPduTransmissionRate29',TMeasurementValue),('dlMacPduTransmissionRate30',TMeasurementValue),('dlMacPduTransmissionRate31',TMeasurementValue),('dlMacPduTransmissionRate32',TMeasurementValue),('ulMacPduTransmissionRate0',TMeasurementValue),('ulMacPduTransmissionRate1',TMeasurementValue),('ulMacPduTransmissionRate2',TMeasurementValue),('ulMacPduTransmissionRate3',TMeasurementValue),('ulMacPduTransmissionRateCrcOked0',TMeasurementValue),('ulMacPduTransmissionRateCrcOked1',TMeasurementValue),('ulMacPduTransmissionRateCrcOked2',TMeasurementValue),('ulMacPduTransmissionRateCrcOked3',TMeasurementValue)]

class SNbrOfDrxUe(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfNonDrxUe',TMeasurementValue),('nbrOfLongDrxUe',TMeasurementValue)]

class SRlcPdcpTraffic(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('transmittedDataRateIni',TMeasurementValue),('transmittedDataRateReTrans',TMeasurementValue),('receivedDataRate',TMeasurementValue),('nbrOfReset',TMeasurementValue),('amountOfDataBufferedRlcPdcp',TMeasurementValue)]

class SPersistentRbUsage(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('dlResource0',TMeasurementValue),('dlResource1',TMeasurementValue),('dlResource2',TMeasurementValue),('dlResource3',TMeasurementValue),('dlResource4',TMeasurementValue),('dlResource5',TMeasurementValue),('dlResource6',TMeasurementValue),('dlResource7',TMeasurementValue),('dlResource8',TMeasurementValue),('dlResource9',TMeasurementValue),('dlResource10',TMeasurementValue),('dlResource11',TMeasurementValue),('dlResource12',TMeasurementValue),('dlResource13',TMeasurementValue),('dlResource14',TMeasurementValue),('dlResource15',TMeasurementValue),('dlResource16',TMeasurementValue),('dlResource17',TMeasurementValue),('dlResource18',TMeasurementValue),('dlResource19',TMeasurementValue),('ulResource0',TMeasurementValue),('ulResource1',TMeasurementValue),('ulResource2',TMeasurementValue),('ulResource3',TMeasurementValue),('ulResource4',TMeasurementValue),('ulResource5',TMeasurementValue),('ulResource6',TMeasurementValue),('ulResource7',TMeasurementValue),('ulResource8',TMeasurementValue),('ulResource9',TMeasurementValue),('ulResource10',TMeasurementValue),('ulResource11',TMeasurementValue),('ulResource12',TMeasurementValue),('ulResource13',TMeasurementValue),('ulResource14',TMeasurementValue),('ulResource15',TMeasurementValue),('ulResource16',TMeasurementValue),('ulResource17',TMeasurementValue),('ulResource18',TMeasurementValue),('ulResource19',TMeasurementValue)]

class SChannelUsageStatus(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfPdcchOfdmSymbol1',TMeasurementValue),('nbrOfPdcchOfdmSymbol2',TMeasurementValue),('nbrOfPdcchOfdmSymbol3',TMeasurementValue),('nbrOfProcessingResourceShortageSituation',TMeasurementValue),('nbrOfUnTransmitUesDueLackOfPdcchResource',TMeasurementValue),('pdfOfWidebankCQI', aprot.bytes(size = 256)),('pdfOfDlAverageDataRate',TMeasurementValue),('pdfOfUlAverageDataRate',TMeasurementValue),('pdfOfUeInactiveTimer', aprot.bytes(size = 11))]

class SInterferenceLevel(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('interferenceLevelPucch',TMeasurementValue),('interferenceLevelPusch',TMeasurementValue),('interferenceLevelPrach',TMeasurementValue)]

class SPathloss(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfUes', aprot.bytes(size = 124))]

class SNbrLogChMeasType1(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfLogChHavingDataInBufferDl1',TMeasurementValue),('nbrOfLogChHavingDataInBufferDl2',TMeasurementValue),('nbrOfLogChHavingDataInBufferDl3',TMeasurementValue),('nbrOfLogChHavingDataInBufferDl4',TMeasurementValue),('nbrOfLogChHavingDataInBufferDl5',TMeasurementValue),('nbrOfLogChHavingDataInBufferDl6',TMeasurementValue),('nbrOfLogChHavingDataInBufferDl7',TMeasurementValue),('nbrOfLogChHavingDataInBufferDl8',TMeasurementValue),('nbrOfLogChHavingDataInBufferDl9',TMeasurementValue),('nbrOfLogChHavingDataInBufferDl10',TMeasurementValue),('nbrOfLogChHavingDataInBufferDl11',TMeasurementValue),('nbrOfLogChHavingDataInBufferDl12',TMeasurementValue),('nbrOfLogChHavingDataInBufferDl13',TMeasurementValue),('nbrOfLogChHavingDataInBufferDl14',TMeasurementValue),('nbrOfLogChHavingDataInBufferDl15',TMeasurementValue),('nbrOfLogChHavingDataInBufferDl16',TMeasurementValue),('nbrOfLogChHavingDataInBufferUl0',TMeasurementValue),('nbrOfLogChHavingDataInBufferUl1',TMeasurementValue),('nbrOfLogChHavingDataInBufferUl2',TMeasurementValue),('nbrOfLogChHavingDataInBufferUl3',TMeasurementValue),('nbrOfLogChAverageDataRateBelowThreshDl1',TMeasurementValue),('nbrOfLogChAverageDataRateBelowThreshDl2',TMeasurementValue),('nbrOfLogChAverageDataRateBelowThreshDl3',TMeasurementValue),('nbrOfLogChAverageDataRateBelowThreshDl4',TMeasurementValue),('nbrOfLogChAverageDataRateBelowThreshDl5',TMeasurementValue),('nbrOfLogChAverageDataRateBelowThreshDl6',TMeasurementValue),('nbrOfLogChAverageDataRateBelowThreshDl7',TMeasurementValue),('nbrOfLogChAverageDataRateBelowThreshDl8',TMeasurementValue),('nbrOfLogChAverageDataRateBelowThreshDl9',TMeasurementValue),('nbrOfLogChAverageDataRateBelowThreshDl10',TMeasurementValue),('nbrOfLogChAverageDataRateBelowThreshDl11',TMeasurementValue),('nbrOfLogChAverageDataRateBelowThreshDl12',TMeasurementValue),('nbrOfLogChAverageDataRateBelowThreshDl13',TMeasurementValue),('nbrOfLogChAverageDataRateBelowThreshDl14',TMeasurementValue),('nbrOfLogChAverageDataRateBelowThreshDl15',TMeasurementValue),('nbrOfLogChAverageDataRateBelowThreshDl16',TMeasurementValue),('nbrOfLogChAverageDataRateBelowThreshUl0',TMeasurementValue),('nbrOfLogChAverageDataRateBelowThreshUl1',TMeasurementValue),('nbrOfLogChAverageDataRateBelowThreshUl2',TMeasurementValue),('nbrOfLogChAverageDataRateBelowThreshUl3',TMeasurementValue)]

class SNbrLogChMeasType2(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfLogChBufferingTimeAboveTreshDl1',TMeasurementValue),('nbrOfLogChBufferingTimeAboveTreshDl2',TMeasurementValue),('nbrOfLogChBufferingTimeAboveTreshDl3',TMeasurementValue),('nbrOfLogChBufferingTimeAboveTreshDl4',TMeasurementValue),('nbrOfLogChBufferingTimeAboveTreshDl5',TMeasurementValue),('nbrOfLogChBufferingTimeAboveTreshDl6',TMeasurementValue),('nbrOfLogChBufferingTimeAboveTreshDl7',TMeasurementValue),('nbrOfLogChBufferingTimeAboveTreshDl8',TMeasurementValue),('nbrOfLogChBufferingTimeAboveTreshDl9',TMeasurementValue),('nbrOfLogChBufferingTimeAboveTreshDl10',TMeasurementValue),('nbrOfLogChBufferingTimeAboveTreshDl11',TMeasurementValue),('nbrOfLogChBufferingTimeAboveTreshDl12',TMeasurementValue),('nbrOfLogChBufferingTimeAboveTreshDl13',TMeasurementValue),('nbrOfLogChBufferingTimeAboveTreshDl14',TMeasurementValue),('nbrOfLogChBufferingTimeAboveTreshDl15',TMeasurementValue),('nbrOfLogChBufferingTimeAboveTreshDl16',TMeasurementValue)]

class SNbrLogChMeasType3(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfLogChDataDiscardDueDelayDl1',TMeasurementValue),('nbrOfLogChDataDiscardDueDelayDl2',TMeasurementValue),('nbrOfLogChDataDiscardDueDelayDl3',TMeasurementValue),('nbrOfLogChDataDiscardDueDelayDl4',TMeasurementValue),('nbrOfLogChDataDiscardDueDelayDl5',TMeasurementValue),('nbrOfLogChDataDiscardDueDelayDl6',TMeasurementValue),('nbrOfLogChDataDiscardDueDelayDl7',TMeasurementValue),('nbrOfLogChDataDiscardDueDelayDl8',TMeasurementValue),('nbrOfLogChDataDiscardDueDelayDl9',TMeasurementValue),('nbrOfLogChDataDiscardDueDelayDl10',TMeasurementValue),('nbrOfLogChDataDiscardDueDelayDl11',TMeasurementValue),('nbrOfLogChDataDiscardDueDelayDl12',TMeasurementValue),('nbrOfLogChDataDiscardDueDelayDl13',TMeasurementValue),('nbrOfLogChDataDiscardDueDelayDl14',TMeasurementValue),('nbrOfLogChDataDiscardDueDelayDl15',TMeasurementValue),('nbrOfLogChDataDiscardDueDelayDl16',TMeasurementValue)]

class SBbResourceRoom(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfDlSpsUe',TMeasurementValue),('nbrOfUlSpsUe',TMeasurementValue),('unsuccessDlSpsAssignsNdiscDlAck',TMeasurementValue),('unsuccessDlSpsAssignsNdiscDl',TMeasurementValue),('unsuccessDlSpsAssignsNdiscUl',TMeasurementValue)]

class SPhichTransmitPower(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('phichTransmitPowerForPersistentSched',TMeasurementValue)]

class SRaPreambleStatistics(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('pdfOfRaPreamblesReceived', aprot.bytes(size = 32))]

class SResourceBlockUsageRatio(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('dlRbUsageRatio',TMeasurementValue),('ulRbUsageRatio',TMeasurementValue),('dlRbUsageRatioDbch',TMeasurementValue),('dlRbUsageRatioPch',TMeasurementValue),('dlRbUsageRatioRar',TMeasurementValue),('dlRbUsageRatioVoice',TMeasurementValue),('ulRbUsageRatioVoice',TMeasurementValue)]

class SPdcchUsageRatio(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfMultiplexedPdcchDl',TMeasurementValue),('nbrOfMultiplexedPdcchUl',TMeasurementValue),('nbrOfMultiplexedPdcchVoiceDl',TMeasurementValue),('nbrOfMultiplexedPdcchVoiceUl',TMeasurementValue),('totalNbrOfCces',TMeasurementValue),('nbrOfCcesAssignedToPdcch',TMeasurementValue),('nbrOfCcesAssignedToPdcchVoice',TMeasurementValue)]

class SMacSduTransmAndReceptRate(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfSubFramesDlSdusTransmLchPrio1',TMeasurementValue),('nbrOfSubFramesDlSdusTransmLchPrio2',TMeasurementValue),('nbrOfSubFramesDlSdusTransmLchPrio3',TMeasurementValue),('nbrOfSubFramesDlSdusTransmLchPrio4',TMeasurementValue),('nbrOfSubFramesDlSdusTransmLchPrio5',TMeasurementValue),('nbrOfSubFramesDlSdusTransmLchPrio6',TMeasurementValue),('nbrOfSubFramesDlSdusTransmLchPrio7',TMeasurementValue),('nbrOfSubFramesDlSdusTransmLchPrio8',TMeasurementValue),('nbrOfSubFramesDlSdusTransmLchPrio9',TMeasurementValue),('nbrOfSubFramesDlSdusTransmLchPrio10',TMeasurementValue),('nbrOfSubFramesDlSdusTransmLchPrio11',TMeasurementValue),('nbrOfSubFramesDlSdusTransmLchPrio12',TMeasurementValue),('nbrOfSubFramesDlSdusTransmLchPrio13',TMeasurementValue),('nbrOfSubFramesDlSdusTransmLchPrio14',TMeasurementValue),('nbrOfSubFramesDlSdusTransmLchPrio15',TMeasurementValue),('nbrOfSubFramesDlSdusTransmLchPrio16',TMeasurementValue),('amountOfTransmDataDlSdusLchPrio1',TMeasurementValue),('amountOfTransmDataDlSdusLchPrio2',TMeasurementValue),('amountOfTransmDataDlSdusLchPrio3',TMeasurementValue),('amountOfTransmDataDlSdusLchPrio4',TMeasurementValue),('amountOfTransmDataDlSdusLchPrio5',TMeasurementValue),('amountOfTransmDataDlSdusLchPrio6',TMeasurementValue),('amountOfTransmDataDlSdusLchPrio7',TMeasurementValue),('amountOfTransmDataDlSdusLchPrio8',TMeasurementValue),('amountOfTransmDataDlSdusLchPrio9',TMeasurementValue),('amountOfTransmDataDlSdusLchPrio10',TMeasurementValue),('amountOfTransmDataDlSdusLchPrio11',TMeasurementValue),('amountOfTransmDataDlSdusLchPrio12',TMeasurementValue),('amountOfTransmDataDlSdusLchPrio13',TMeasurementValue),('amountOfTransmDataDlSdusLchPrio14',TMeasurementValue),('amountOfTransmDataDlSdusLchPrio15',TMeasurementValue),('amountOfTransmDataDlSdusLchPrio16',TMeasurementValue),('nbrOfSubFramesUlSdusTransmLchPrio0',TMeasurementValue),('nbrOfSubFramesUlSdusTransmLchPrio1',TMeasurementValue),('nbrOfSubFramesUlSdusTransmLchPrio2',TMeasurementValue),('nbrOfSubFramesUlSdusTransmLchPrio3',TMeasurementValue),('amountOfTransmDataUlSdusLchPrio0',TMeasurementValue),('amountOfTransmDataUlSdusLchPrio1',TMeasurementValue),('amountOfTransmDataUlSdusLchPrio2',TMeasurementValue),('amountOfTransmDataUlSdusLchPrio3',TMeasurementValue)]

class SNumberOfVoiceUE(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfVoiceUePerDelayPackedIndex0',TMeasurementValue),('nbrOfVoiceUePerDelayPackedIndex1',TMeasurementValue),('nbrOfVoiceUePerDelayPackedIndex2',TMeasurementValue),('nbrOfVoiceUePerDelayPackedIndex3',TMeasurementValue),('nbrOfVoiceUePerPeriodicGrantIndex0TtiBundlOn',TMeasurementValue),('nbrOfVoiceUePerPeriodicGrantIndex1TtiBundlOn',TMeasurementValue),('nbrOfVoiceUePerPeriodicGrantIndex2TtiBundlOn',TMeasurementValue),('nbrOfVoiceUePerPeriodicGrantIndex3TtiBundlOn',TMeasurementValue),('nbrOfVoiceUePerPeriodicGrantIndex0TtiBundlOff',TMeasurementValue),('nbrOfVoiceUePerPeriodicGrantIndex1TtiBundlOff',TMeasurementValue),('nbrOfVoiceUePerPeriodicGrantIndex2TtiBundlOff',TMeasurementValue),('nbrOfVoiceUePerPeriodicGrantIndex3TtiBundlOff',TMeasurementValue),('nbrOfDlPduPerDelayPackedIndex0',TMeasurementValue),('nbrOfDlPduPerDelayPackedIndex1',TMeasurementValue),('nbrOfDlPduPerDelayPackedIndex2',TMeasurementValue),('nbrOfDlPduPerDelayPackedIndex3',TMeasurementValue),('nbrOfDlHarqTxPerDelayPackedIndex0',TMeasurementValue),('nbrOfDlHarqTxPerDelayPackedIndex1',TMeasurementValue),('nbrOfDlHarqTxPerDelayPackedIndex2',TMeasurementValue),('nbrOfDlHarqTxPerDelayPackedIndex3',TMeasurementValue),('nbrOfUlPduPerPeriodicGrantIndex0TtiBundOn',TMeasurementValue),('nbrOfUlPduPerPeriodicGrantIndex1TtiBundOn',TMeasurementValue),('nbrOfUlPduPerPeriodicGrantIndex2TtiBundOn',TMeasurementValue),('nbrOfUlPduPerPeriodicGrantIndex3TtiBundOn',TMeasurementValue),('nbrOfUlHarqTxPerPeriodicGrantIndex0TtiBundOn',TMeasurementValue),('nbrOfUlHarqTxPerPeriodicGrantIndex1TtiBundOn',TMeasurementValue),('nbrOfUlHarqTxPerPeriodicGrantIndex2TtiBundOn',TMeasurementValue),('nbrOfUlHarqTxPerPeriodicGrantIndex3TtiBundOn',TMeasurementValue),('nbrOfUlPduPerPeriodicGrantIndex0TtiBundOff',TMeasurementValue),('nbrOfUlPduPerPeriodicGrantIndex1TtiBundOff',TMeasurementValue),('nbrOfUlPduPerPeriodicGrantIndex2TtiBundOff',TMeasurementValue),('nbrOfUlPduPerPeriodicGrantIndex3TtiBundOff',TMeasurementValue),('nbrOfUlHarqTxPerPeriodicGrantIndex0TtiBundlOff',TMeasurementValue),('nbrOfUlHarqTxPerPeriodicGrantIndex1TtiBundlOff',TMeasurementValue),('nbrOfUlHarqTxPerPeriodicGrantIndex2TtiBundlOff',TMeasurementValue),('nbrOfUlHarqTxPerPeriodicGrantIndex3TtiBundlOff',TMeasurementValue),('nbrOfAckPduPerDelayPackedIndex0',TMeasurementValue),('nbrOfAckPduPerDelayPackedIndex1',TMeasurementValue),('nbrOfAckPduPerDelayPackedIndex2',TMeasurementValue),('nbrOfAckPduPerDelayPackedIndex3',TMeasurementValue),('nbrOfExceedMaxTransmPerDelayPackedIndex0',TMeasurementValue),('nbrOfExceedMaxTransmPerDelayPackedIndex1',TMeasurementValue),('nbrOfExceedMaxTransmPerDelayPackedIndex2',TMeasurementValue),('nbrOfExceedMaxTransmPerDelayPackedIndex3',TMeasurementValue),('nbrOfAckPduPerPeriodicGrantIndex0TtiBundlOn',TMeasurementValue),('nbrOfAckPduPerPeriodicGrantIndex1TtiBundlOn',TMeasurementValue),('nbrOfAckPduPerPeriodicGrantIndex2TtiBundlOn',TMeasurementValue),('nbrOfAckPduPerPeriodicGrantIndex3TtiBundlOn',TMeasurementValue),('nbrOfExceedTransmPeriodicGrantIndex0TtiBundlOn',TMeasurementValue),('nbrOfExceedTransmPeriodicGrantIndex1TtiBundlOn',TMeasurementValue),('nbrOfExceedTransmPeriodicGrantIndex2TtiBundlOn',TMeasurementValue),('nbrOfExceedTransmPeriodicGrantIndex3TtiBundlOn',TMeasurementValue),('nbrOfAckPduPerPeriodicGrantIndex0TtiBundlOff',TMeasurementValue),('nbrOfAckPduPerPeriodicGrantIndex1TtiBundlOff',TMeasurementValue),('nbrOfAckPduPerPeriodicGrantIndex2TtiBundlOff',TMeasurementValue),('nbrOfAckPduPerPeriodicGrantIndex3TtiBundlOff',TMeasurementValue),('nbrOfExceedMaxTransmPeriodicGrantIndex0TtiBundlOff',TMeasurementValue),('nbrOfExceedMaxTransmPeriodicGrantIndex1TtiBundlOff',TMeasurementValue),('nbrOfExceedMaxTransmPeriodicGrantIndex2TtiBundlOff',TMeasurementValue),('nbrOfExceedMaxTransmPeriodicGrantIndex3TtiBundlOff',TMeasurementValue)]

class SGbrLoadCellDl(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfUsedPrbsForGbrTrafficDl',TMeasurementValue),('averageNbrOfAvailablePrbsForGbrDl',TMeasurementValue),('initTransmEfficiencyDl',TMeasurementValue),('ratioOfPdcchUtilizUesWithGbrBearersDl',TMeasurementValue)]

class SGbrLoadCellUl(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfUsedPrbsForGbrTrafficUl',TMeasurementValue),('averageNbrOfAvailablePrbsForGbrUl',TMeasurementValue),('initTransmEfficiencyUl',TMeasurementValue),('ratioOfPdcchUtilizUesWithGbrBearersUl',TMeasurementValue)]

class SGbrLoadUeDl(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('gbrLoadUeDl', aprot.bytes(size = 1))]

class SGbrLoadUe(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',TMeasurementValue),('transmEfficiency',TMeasurementValue),('nbrOfBearers',TMeasurementValue),('drbData', aprot.bytes(size = 4))]

class SDrbData(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('drbId',TMeasurementValue),('nbrOfAllocatedPrbs',TMeasurementValue)]

class SGbrLoadUeUl(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('gbrLoadUeUl', aprot.bytes(size = 1))]

class SNonGbrLoadCellDl(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('averAvailNbrOfPrbsNonGbrTraffDl',TMeasurementValue),('averSumOfWeightsBearersWithDataTransmDl',TMeasurementValue)]

class SPdcchLoadCell(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('averCellsPdcchLoad',TMeasurementValue)]

class SSCellsConfiguration(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCellIdScell',TOaMLnCelId),('sCellServCellIndex',TSCellServCellIndex),('transmModeScell',ETransmMode),('maxNumOfLayersScell',EMaxNumOfLayers),('cqiParamsScell',SCqiParamsScell),('container',UCaWmpDcmSCellContainer)]

class SSCellsRemove(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCellIdScell',TOaMLnCelId)]

class SServiceInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('serviceType',ETestabilityServiceType),('serviceAddr',TAaSysComSicad)]

class SL2DlPhyAddressess(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('pdschCw0SendReqAddress',TAaSysComSicad),('pdschCw1SendReqAddress',TAaSysComSicad),('srioType9Cos',aprot.u32),('srioType9StreamId',aprot.u32),('pdschEventQueueId',aprot.u32)]

class SL2MacPsAddresses(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('numOfUeGroups',TNumberOfItems),('psUserUl', aprot.bytes(size = MAX_NUM_UEGROUP_PER_BB_POOL)),('psUserDl', aprot.bytes(size = MAX_NUM_UEGROUP_PER_BB_POOL)),('dataCtrlDLPdcchClient',TAaSysComSicad)]

class SRaMsg3ThrLowParameters(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('raMsg3ThrLow',TRaMsg3ThrLow),('raMsg3ThrLowCnt',TRaMsg3ThrLowCnt),('flagCcchPriority',TFlagCcchPriority)]

class SPrachUsageRatio2(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfDicardedRACHMessage3Meas',TMeasurementValue),('nbrOfDicardedNonPrioritizedRACHMessage3Meas',TMeasurementValue)]

class SAperiodicCsiTriggerParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('aperiodicCsiTrigger1',TAperiodicCsiTrigger),('aperiodicCsiTrigger2',TAperiodicCsiTrigger),('padding',aprot.u16)]

class SSCellResultsParameters(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCellIdScell',TOaMLnCelId),('messageResult',SMessageResult)]

class SRaMsg3ThrCntParameters(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('discardingCellGroupId',TCntId),('raMsg3ThrCnt',TRaMsg3ThrCnt)]

class SAaTime(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('year',aprot.u32),('month',aprot.u32),('day',aprot.u32),('hour',aprot.u32),('minute',aprot.u32),('second',aprot.u32),('millisec',aprot.u32)]

	
	