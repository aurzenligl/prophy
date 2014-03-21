import prophy

TENodeBId = prophy.u32
TTimeUnit = prophy.u32
TCrnti = prophy.u32
TEci = prophy.u32
TUeS1X2Id = prophy.u32
ETraceType8 = prophy.u8
TLinkItfName = prophy.u8
TTraceSessionProtocol8 = prophy.u8
ETraceProtocolFormat8 = prophy.u8

class EMsgType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators = [("EMsgType_IsAlive", 0x0100),
                    ("EMsgType_TraceReport", 0x1100),
                    ("EMsgType_TraceStart", 0x1200),
                    ("EMsgType_TraceStop", 0x1300),
                    ("EMsgType_TraceFailure", 0x1A00)]

class Version(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("eNodeBVersion", prophy.u8),
                   ("eNodeBSubversion", prophy.u8),
                   ("threeGPPVersion", prophy.u8),
                   ("vendorVersion", prophy.u8)]

class MsgInfo(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("msgType", EMsgType),
                   ("udpSeqNumber", prophy.u16),
                   ("udpOffset", prophy.u16),
                   ("reserved", prophy.u32)]

class TraceReportHeader(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("traceReference", prophy.bytes(size = 6)),
                   ("seqNum", prophy.u32)]

class MsgReportHeader(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("synchId", prophy.u32),
                   ("length", prophy.u32),
                   ("version", Version),
                   ("plmnId", prophy.u32),
                   ("eNodeBId", TENodeBId),
                   ("msgInfo", MsgInfo)]

class SUtcTime(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("seconds", TTimeUnit),
                   ("microseconds", TTimeUnit)]

class Type(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("traceType", ETraceType8),
                   ("linkItfName", TLinkItfName),
                   ("protName", TTraceSessionProtocol8),
                   ("protFormat", ETraceProtocolFormat8),
                   ("protMsgType", prophy.u16)]

class Value(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("cellIdentity", TEci),
                   ("ueId", TUeS1X2Id)]

class TraceObject(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("type", Type),
                   ("value", Value),
                   ("crnti", TCrnti)]

class TraceMsg(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("sizeofTraceMsg", prophy.u32),
                   ("timeStamp", SUtcTime),
                   ("traceRecSessionId", prophy.u16),
                   ("traceObject", TraceObject),
                   ("traceData", prophy.bytes(bound = "sizeofTraceMsg", shift = 32))]

class LOM_TracingExtReportInd(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("header", MsgReportHeader),
                   ("reportHeader", TraceReportHeader),
                   ("traceMsgs", prophy.array(TraceMsg))]

def test_it():
    report = LOM_TracingExtReportInd()
    print len(report.encode(">")), repr(report.encode(">"))
    print report
    report.traceMsgs.add().traceData = "lorem ipsum"
    print len(report.encode(">")), repr(report.encode(">"))
    print report
    report.header.plmnId = 0xABBD
    report.header.msgInfo.udpOffset = 10
    report.reportHeader.traceReference = "abcdef"
    report.traceMsgs[0].timeStamp.microseconds = 2
    report.traceMsgs[0].traceObject.type.protFormat = 0xFF
    report.traceMsgs[0].traceObject.crnti = 0xDEADBEEF
    print len(report.encode(">")), repr(report.encode(">"))
    print report

def test_it_2():
    report = LOM_TracingExtReportInd()
    report.decode("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xab\xbd\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\n\x00\x00\x00\x00abcdef\x00\x00\x00\x00\x00\x00\x00+\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xde\xad\xbe\xeflorem ipsum", ">")
    print len(report.encode(">")), repr(report.encode(">"))
    print report
