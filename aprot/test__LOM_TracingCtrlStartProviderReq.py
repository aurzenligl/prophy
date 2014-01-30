import aprot
from test__enumerations import *

TTraceHandle = aprot.u32
TENodeBId = aprot.u32
TAaSysComSicad = aprot.u32
TTraceSessionProtocol = aprot.u32
TNumberOfItems = aprot.u32
TTracePort = aprot.u32
TEci = aprot.u32
TSize = aprot.u32
TTraceProtocolMsgType = aprot.u32
TTracedProtocols = aprot.u32

class STransportLayerAddress(aprot.struct):
    __metaclass__ = aprot.struct_generator
    _descriptor = [("addressLength", TTraceHandle),
                   ("address", aprot.bytes(size = 16, bound = "addressLength"))]

class SUdpAddress(aprot.struct):
    __metaclass__ = aprot.struct_generator
    _descriptor = [("ipAddress", STransportLayerAddress),
                   ("port", TTracePort)]

class STraceMsgs(aprot.struct):
    __metaclass__ = aprot.struct_generator
    _descriptor = [("ueS1State", ESTraceMsgsState),
                   ("ueS1Length", TSize),
                   ("ueS1Msgs", aprot.array(TTraceProtocolMsgType, size = 20, bound = "ueS1Length")),
                   ("nonUeS1State", ESTraceMsgsState),
                   ("nonUeS1Length", TSize),
                   ("nonUeS1Msgs", aprot.array(TTraceProtocolMsgType, size = 20, bound = "nonUeS1Length")),
                   ("ueX2State", ESTraceMsgsState),
                   ("ueX2Length", TSize),
                   ("ueX2Msgs", aprot.array(TTraceProtocolMsgType, size = 10, bound = "ueX2Length")),
                   ("nonUeX2State", ESTraceMsgsState),
                   ("nonUeX2Length", TSize),
                   ("nonUeX2Msgs", aprot.array(TTraceProtocolMsgType, size = 10, bound = "nonUeX2Length")),
                   ("ueRrcState", ESTraceMsgsState),
                   ("ueRrcLength", TSize),
                   ("ueRrcMsgs", aprot.array(TTraceProtocolMsgType, size = 10, bound = "ueRrcLength")),
                   ("nonUeRrcState", ESTraceMsgsState),
                   ("nonUeRrcLength", TSize),
                   ("nonUeRrcMsgs", aprot.array(TTraceProtocolMsgType, size = 10, bound = "nonUeRrcLength")),
                   ("vendorProtocols", TTracedProtocols)]

class LOM_TracingCtrlStartProviderReq(aprot.struct):
    __metaclass__ = aprot.struct_generator
    _descriptor = [("handle", TTraceHandle),
                   ("eutranTraceId", aprot.bytes(size = 8)),
                   ("eNodeBId", TENodeBId),
                   ("eci", TEci),
                   ("type", ETraceType),
                   ("maxTracedUes", aprot.u32),
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
    req.messages.nonUeS1Msgs[:] = [1,2,3]
    req.messages.nonUeX2Msgs[:] = [89,34,6565,66,7]
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

test_it()

