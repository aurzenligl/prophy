import protophy

class LMGTT_UserActivateResp(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('Status',protophy.u32),
    				('SubUnit',protophy.u32),
					('Cause',protophy.u32)]