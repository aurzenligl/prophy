import protophy

class LMGTT_UserDeactivateReq(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('NumOfValidElements',protophy.u32),
    				('UeId',protophy.u32),
					('NumOfSrbs',protophy.u32),
					('Srb_SrbId',protophy.u32),
					('NumOfDrbs',protophy.u32),
					('Drb_DrbId',protophy.u32)]