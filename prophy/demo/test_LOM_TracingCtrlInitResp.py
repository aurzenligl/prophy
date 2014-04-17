import prophy
from enumerations import *

TTraceHandle = prophy.u32
TENodeBId = prophy.u32
TAaSysComSicad = prophy.u32
TTraceSessionProtocol = prophy.u32
TNumberOfItems = prophy.u32
TTracePort = prophy.u32
TEci = prophy.u32

class STransportLayerAddress(prophy.struct_packed):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("addressLength", TTraceHandle),
                   ("address", prophy.bytes(size = 16, bound = "addressLength"))]

class SUdpAddress(prophy.struct_packed):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("ipAddress", STransportLayerAddress),
                   ("port", TTracePort)]

class LOM_TracingCtrlInitResp(prophy.struct_packed):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("handle", TTraceHandle),
                   ("eutranTraceId", prophy.bytes(size = 8)),
                   ("eNodeBId", TENodeBId),
                   ("eci", TEci),
                   ("omsTcpSessionSicad", TAaSysComSicad),
                   ("thirdPartyTcpSessionSicad", TAaSysComSicad),
                   ("extIpAddress", STransportLayerAddress),
                   ("mode", ETraceReportingMode),
                   ("depth", ETraceDepth),
                   ("protocols", TTraceSessionProtocol),
                   ("status", ELomStatus),
                   ("udpAddress", SUdpAddress)]

def test_it():
    resp = LOM_TracingCtrlInitResp()
    resp.eutranTraceId = "abcd"
    resp.extIpAddress.address = "\xff\xfe\xff\xfe\xff\xfe"
    resp.udpAddress.ipAddress.address = "\x01\x02\x03\x04"
    print resp
