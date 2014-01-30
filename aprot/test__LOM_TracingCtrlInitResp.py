import aprot
from test__enumerations import *

TTraceHandle = aprot.u32
TENodeBId = aprot.u32
TAaSysComSicad = aprot.u32
TTraceSessionProtocol = aprot.u32
TNumberOfItems = aprot.u32
TTracePort = aprot.u32
TEci = aprot.u32

class STransportLayerAddress(aprot.struct):
    __metaclass__ = aprot.struct_generator
    _descriptor = [("addressLength", TTraceHandle),
                   ("address", aprot.bytes(size = 16, bound = "addressLength"))]

class SUdpAddress(aprot.struct):
    __metaclass__ = aprot.struct_generator
    _descriptor = [("ipAddress", STransportLayerAddress),
                   ("port", TTracePort)]

class LOM_TracingCtrlInitResp(aprot.struct):
    __metaclass__ = aprot.struct_generator
    _descriptor = [("handle", TTraceHandle),
                   ("eutranTraceId", aprot.bytes(size = 8)),
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
    import pdb;pdb.set_trace()
    print resp
    
test_it()
