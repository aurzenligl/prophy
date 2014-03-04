import protophy

class LMGTT_UserSetupReq(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('NumOfValidElements',protophy.u32),
    				('TargetForSrbs',protophy.u32),
					('CellIdForSrbs',protophy.u32),
					('CrntiForSrbs',protophy.u32)]