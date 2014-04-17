import prophy
from enumerations import *

TBrowserObjectId = prophy.u32
TLomHandle = prophy.u32
TBrowserContextId = prophy.u32
TBrowserProcedureId = prophy.u32
TLomSessionId = prophy.u32
TNumberOfItems = prophy.u32
TDataCount = prophy.u32

class SBrowserObjectInfo(prophy.struct_packed):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("objectName", EBrowserObjectName),
                   ("objectId", TBrowserObjectId),
                   ("objectHandle", TLomHandle)]

class LteBrowserObjectsResp(prophy.struct_packed):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("status", EBrowserStatus),
                   ("contextId", TBrowserContextId),
                   ("procedureId", TBrowserProcedureId),
                   ("sessionId", TLomSessionId),
                   ("numOfAssociatedObjects", TNumberOfItems),
                   ("itemSize", TDataCount),
                   ("dynamicData", prophy.array(SBrowserObjectInfo, bound = "numOfAssociatedObjects"))]

def test_it():
    info = SBrowserObjectInfo()
    info.objectName = "EBrowserObjectName_LteUserMacTm"
    info.objectId = 2
    info.objectHandle = 3

    print repr(info.encode(">"))
    print info

    resp = LteBrowserObjectsResp()
    resp.status = "EBrowserStatus_MergedToOngoing"
    resp.contextId = 8
    resp.procedureId = 7
    resp.sessionId = 6
    resp.itemSize = 5
    resp.dynamicData.extend([info])
    info = resp.dynamicData.add()
    info.objectName = "EBrowserObjectName_LteCellAdjGsmUec"
    info.objectId = 5
    info.objectHandle = 6
    print repr(resp.encode(">"))
    print resp

    resp2 = LteBrowserObjectsResp()
    resp2.decode("\x00\x00\x00\x03\x00\x00\x00\x08\x00\x00\x00\x07\x00\x00\x00\x06\x00\x00\x00\x02\x00\x00\x00\x05\x00\x00\x05\x1a\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x08\x9c\x00\x00\x00\x05\x00\x00\x00\x06", ">")
    del resp2.dynamicData[0]
    print resp2
