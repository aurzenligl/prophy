import protophy

class header(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('protocol_id',protophy.u8),
                   ('msg_type',protophy.u8),
                   ('msg_len',protophy.u16),
                   ('msg_nr',protophy.u16),
                   ('spare',protophy.u16),
                   ('pad',protophy.u16),
                   ('id',protophy.u16),
                   ('board',protophy.u8),
                   ('cpu',protophy.u8),
                   ('task',protophy.u16),
                   ('board',protophy.u8),
                   ('cpu',protophy.u8),
                   ('task',protophy.u16),
                   ('length',protophy.u16),
                   ('system',protophy.u8),
                   ('user',protophy.u8)]
