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