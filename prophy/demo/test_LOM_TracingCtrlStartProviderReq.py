import prophy
from enumerations import *

TTraceHandle = prophy.u32
TENodeBId = prophy.u32
TAaSysComSicad = prophy.u32
TTraceSessionProtocol = prophy.u32
TNumberOfItems = prophy.u32
TTracePort = prophy.u32
TEci = prophy.u32
TSize = prophy.u32
TTraceProtocolMsgType = prophy.u32
TTracedProtocols = prophy.u32

class STransportLayerAddress(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("addressLength", TTraceHandle),
                   ("address", prophy.bytes(size = 16, bound = "addressLength"))]

class SUdpAddress(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("ipAddress", STransportLayerAddress),
                   ("port", TTracePort)]

class STraceMsgs(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("ueS1State", ESTraceMsgsState),
                   ("ueS1Length", TSize),
                   ("ueS1Msgs", prophy.array(TTraceProtocolMsgType, size = 20, bound = "ueS1Length")),
                   ("nonUeS1State", ESTraceMsgsState),
                   ("nonUeS1Length", TSize),
                   ("nonUeS1Msgs", prophy.array(TTraceProtocolMsgType, size = 20, bound = "nonUeS1Length")),
                   ("ueX2State", ESTraceMsgsState),
                   ("ueX2Length", TSize),
                   ("ueX2Msgs", prophy.array(TTraceProtocolMsgType, size = 10, bound = "ueX2Length")),
                   ("nonUeX2State", ESTraceMsgsState),
                   ("nonUeX2Length", TSize),
                   ("nonUeX2Msgs", prophy.array(TTraceProtocolMsgType, size = 10, bound = "nonUeX2Length")),
                   ("ueRrcState", ESTraceMsgsState),
                   ("ueRrcLength", TSize),
                   ("ueRrcMsgs", prophy.array(TTraceProtocolMsgType, size = 10, bound = "ueRrcLength")),
                   ("nonUeRrcState", ESTraceMsgsState),
                   ("nonUeRrcLength", TSize),
                   ("nonUeRrcMsgs", prophy.array(TTraceProtocolMsgType, size = 10, bound = "nonUeRrcLength")),
                   ("vendorProtocols", TTracedProtocols)]

class LOM_TracingCtrlStartProviderReq(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("handle", TTraceHandle),
                   ("eutranTraceId", prophy.bytes(size = 8)),
                   ("eNodeBId", TENodeBId),
                   ("eci", TEci),
                   ("type", ETraceType),
                   ("maxTracedUes", prophy.u32),
                   ("mode", ETraceReportingMode),
                   ("depth", ETraceDepth),
                   ("messages", STraceMsgs),
                   ("omsTcpSessionSicad", TAaSysComSicad),
                   ("thirdPartyTcpSessionSicad", TAaSysComSicad),
                   ("extIpAddress", STransportLayerAddress),
                   ("udpAddress", SUdpAddress)]

def test_it():
    req = LOM_TracingCtrlStartProviderReq()
    print len(req.encode(">"))
    print repr(req.encode(">"))
    print req
    req.messages.nonUeS1Msgs[:] = [1, 2, 3]
    req.messages.nonUeX2Msgs[:] = [89, 34, 6565, 66, 7]
    req.messages.nonUeRrcMsgs[:] = [1]
    req.extIpAddress.address = "\x12\x34\x56\x78\x9a"
    req.udpAddress.ipAddress.address = "\x12\x34"
    req.udpAddress.port = 65536
    print len(req.encode(">"))
    print repr(req.encode(">"))
    print req

    req2 = LOM_TracingCtrlStartProviderReq()
    req2.copy_from(req)
    print len(req2.encode(">"))
    print repr(req2.encode(">"))
    print req2
