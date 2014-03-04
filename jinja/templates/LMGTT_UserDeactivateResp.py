import protophy

class LMGTT_UserDeactivateResp(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('Status',protophy.u32),
    				('Subunit',protophy.u32),
					('Cause',protophy.u32)]