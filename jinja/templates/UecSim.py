import protophy

class UecSim_ReconfigReq(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('macUserBoard',protophy.u8), 
    			   ('macUserCpu',protophy.u8),
    			   ('macUserTask',protophy.u16),
    			   ('macSgnBoard',protophy.u8),
    			   ('macSgnCpu',protophy.u8),
    			   ('macSgnTask',protophy.u16),
    			   ('macUlCellBoard',protophy.u8),
    			   ('macUlCellCpu',protophy.u8),
    			   ('macUlCellTask',protophy.u16),
    			   ('ahtiBoard',protophy.u8),
    			   ('ahtiCpu',protophy.u8),
    			   ('ahtiTask',protophy.u16)]
    
class UecSim_ReconfigResp(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('macUserBoard',protophy.u32), 
                   ('macUserCpu',protophy.u32),
                   ('macUserTask',protophy.u32),
                   ('macSgnBoard',protophy.u32),
                   ('macSgnCpu',protophy.u32),
                   ('macSgnTask',protophy.u32),
                   ('macUlCellBoard',protophy.u32),
                   ('macUlCellCpu',protophy.u32),
                   ('macUlCellTask',protophy.u32),
                   ('ahtiBoard',protophy.u32),
                   ('ahtiCpu',protophy.u32),
                   ('ahtiTask',protophy.u32)]