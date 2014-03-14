import prophy 
from externals import *
from globals import *



TSmcRadDebugLogEnabledGlobal = TBoolean
TSmcRadDebugLogEnabledSmc = TBoolean
TSmcRadDebugLogEnabledCommon = TBoolean


class SUplaneAddr(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tupConfigAddr',TAaSysComSicad), ('tupCellAddr',TAaSysComSicad), ('macCellAddr',TAaSysComSicad), ('phyCellUplinkAddr',TAaSysComSicad), ('phyCellDownlinkAddr',TAaSysComSicad), ('tupDownlinkIpAddr',STransportLayerAddress)]
class SUplaneAddrForLteInMicro(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tupConfigAddr',TAaSysComSicad), ('tupCellAddr',TAaSysComSicad), ('macCellAddr',TAaSysComSicad), ('phyCellUplinkAddr',TAaSysComSicad), ('phyCellDownlinkAddr',TAaSysComSicad), ('numOfUeGroups',TNumberOfItems), ('tupDownlinkAddr',prophy.bytes(size=MAX_NUM_UEGROUP_PER_BB_POOL))]
class SUplaneAddrForWcdmaInMicro(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tupUserplaneAddr',TAaSysComSicad), ('ccdDspLtcomAddr',TAaSysComSicad), ('dcdCell1DspLtcomAddr',TAaSysComSicad), ('dcdCell2DspLtcomAddr',TAaSysComSicad), ('commonDspMeasAddr',TAaSysComSicad), ('cell1DspMeasAddr',TAaSysComSicad), ('cell2DspMeasAddr',TAaSysComSicad), ('dspMachsRmAddr',TAaSysComSicad), ('nodeSyncAddr',TAaSysComSicad), ('rake1Addr',TAaSysComSicad), ('rake2Addr',TAaSysComSicad), ('l2DctMeasMgrAddr',TAaSysComSicad), ('l1Cell1DctMeasMgrAddr',TAaSysComSicad), ('l1Cell2DctMeasMgrAddr',TAaSysComSicad)]
class SUplaneAddrForLteInLrc(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tupConfigAddr',TAaSysComSicad), ('tupCellAddr',TAaSysComSicad), ('macCellAddr',TAaSysComSicad), ('phyCellUplinkAddr',prophy.bytes(size=NUM_PHY_PER_LSP_IN_LRC)), ('phyCellDownlinkAddr',prophy.bytes(size=NUM_PHY_PER_LSP_IN_LRC)), ('numberOfValidUEGroup',TNumberOfItems), ('tupEqId',prophy.bytes(size=MAX_NUM_UEGROUP_PER_BB_POOL))]
class SUplaneAddrForWcdmaInLrc(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('mcdDspLtcomAddr',prophy.bytes(size=NUM_K2_PER_LSP_IN_LRC)), ('dcdDspLtcomAddr',prophy.bytes(size=NUM_K2_PER_LSP_IN_LRC)), ('tupL2UserplaneAddr',prophy.bytes(size=NUM_K2_PER_LSP_IN_LRC)), ('mcdDspMeasAddr',prophy.bytes(size=NUM_K2_PER_LSP_IN_LRC)), ('dcdDspMeasAddr',prophy.bytes(size=NUM_K2_PER_LSP_IN_LRC)), ('dspMachsRmAddr',prophy.bytes(size=NUM_K2_PER_LSP_IN_LRC)), ('nodeSyncAddr',prophy.bytes(size=NUM_K2_PER_LSP_IN_LRC)), ('hsupaL2MgrAddr',prophy.bytes(size=NUM_K2_PER_LSP_IN_LRC)), ('loopdelayRachRakeAddr',prophy.bytes(size=NUM_K2_PER_LSP_IN_LRC)), ('loopdelayRakeAddr',prophy.bytes(size=NUM_K2_PER_LSP_IN_LRC))]
class SMC_HwConfigReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('bbResourceId',TBoardId)]
class SMC_HwConfigResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('result',SMessageResult), ('bbResourceId',TBoardId)]
class SMC_GetUplaneAddrReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('bbResourceId',TBoardId)]
class SMC_GetUplaneAddrResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('result',SMessageResult), ('bbResourceId',TBoardId), ('uplaneAddr',SUplaneAddr)]
class SMC_GetUplaneAddrForLteInMicroResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('result',SMessageResult), ('bbResourceId',TBoardId), ('uplaneAddr',SUplaneAddrForLteInMicro)]
class SMC_GetUplaneAddrForWcdmaInMicroResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('result',SMessageResult), ('bbResourceId',TBoardId), ('uplaneAddr',SUplaneAddrForWcdmaInMicro)]
class SMC_NetworkConfigReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('bbResourceId',TBoardId), ('dscp',TDscp), ('tmpName',TNumberOfItems), ('enbIPAddrList',prophy.array(STransportLayerAddress,bound='tmpName'))]
class SMC_NetworkConfigResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('result',SMessageResult), ('bbResourceId',TBoardId)]
class SMC_GetUplaneAddrForLteInLrcResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('result',SMessageResult), ('bbResourceId',TBoardId), ('uplaneAddr',SUplaneAddrForLteInLrc)]
class SMC_GetUplaneAddrForWcdmaInLrcResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('result',SMessageResult), ('bbResourceId',TBoardId), ('uplaneAddr',SUplaneAddrForWcdmaInLrc)]
