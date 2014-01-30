import aprot

TENodeBId = aprot.u32
TTimeUnit = aprot.u32
TCrnti = aprot.u32
TEci = aprot.u32
TUeS1X2Id = aprot.u32
ETraceType8 = aprot.u8
TLinkItfName = aprot.u8
TTraceSessionProtocol8 = aprot.u8
ETraceProtocolFormat8 = aprot.u8

class EMsgType(aprot.enum):
    __metaclass__ = aprot.enum_generator
    _enumerators = [("EMsgType_IsAlive", 0x0100),
                    ("EMsgType_TraceReport", 0x1100),
                    ("EMsgType_TraceStart", 0x1200),
                    ("EMsgType_TraceStop", 0x1300),
                    ("EMsgType_TraceFailure", 0x1A00)]

class Version(aprot.struct):
    __metaclass__ = aprot.struct_generator
    _descriptor = [("eNodeBVersion", aprot.u8),
                   ("eNodeBSubversion", aprot.u8),
                   ("threeGPPVersion", aprot.u8),
                   ("vendorVersion", aprot.u8)]

class MsgInfo(aprot.struct):
    __metaclass__ = aprot.struct_generator
    _descriptor = [("msgType", EMsgType),
                   ("udpSeqNumber", aprot.u16),
                   ("udpOffset", aprot.u16),
                   ("reserved", aprot.u32)]

class TraceReportHeader(aprot.struct):
    __metaclass__ = aprot.struct_generator
    _descriptor = [("traceReference", aprot.bytes(size = 6)),
                   ("seqNum", aprot.u32)]

class MsgReportHeader(aprot.struct):
    __metaclass__ = aprot.struct_generator
    _descriptor = [("synchId", aprot.u32),
                   ("length", aprot.u32),
                   ("version", Version),
                   ("plmnId", aprot.u32),
                   ("eNodeBId", TENodeBId),
                   ("msgInfo", MsgInfo)]

class SUtcTime(aprot.struct):
    __metaclass__ = aprot.struct_generator
    _descriptor = [("seconds", TTimeUnit),
                   ("microseconds", TTimeUnit)]

class Type(aprot.struct):
    __metaclass__ = aprot.struct_generator
    _descriptor = [("traceType", ETraceType8),
                   ("linkItfName", TLinkItfName),
                   ("protName", TTraceSessionProtocol8),
                   ("protFormat", ETraceProtocolFormat8),
                   ("protMsgType", aprot.u16)]

class Value(aprot.struct):
    __metaclass__ = aprot.struct_generator
    _descriptor = [("cellIdentity", TEci),
                   ("ueId", TUeS1X2Id)]

class TraceObject(aprot.struct):
    __metaclass__ = aprot.struct_generator
    _descriptor = [("type", Type),
                   ("value", Value),
                   ("crnti", TCrnti)]

class TraceMsg(aprot.struct):
    __metaclass__ = aprot.struct_generator
    _descriptor = [("sizeofTraceMsg", aprot.u32),
                   ("timeStamp", SUtcTime),
                   ("traceRecSessionId", aprot.u16),
                   ("traceObject", TraceObject),
                   ("traceData", aprot.bytes(bound = "sizeofTraceMsg", shift = 32))]

class LOM_TracingExtReportInd(aprot.struct):
    __metaclass__ = aprot.struct_generator
    _descriptor = [("header", MsgReportHeader),
                   ("reportHeader", TraceReportHeader),
                   ("traceMsgs", aprot.array(TraceMsg))]

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

test_it_2()