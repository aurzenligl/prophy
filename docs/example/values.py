import prophy

class Keys(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('key_a', prophy.u32),
                   ('key_b', prophy.u32),
                   ('key_c', prophy.u32)]

class Nodes(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('num_of_nodes', prophy.u32),
                   ('nodes', prophy.array(prophy.u32, bound = 'num_of_nodes', size = 3))]

class Token(prophy.union):
    __metaclass__ = prophy.union_generator
    _descriptor = [('id', prophy.u32, 0),
                   ('keys', Keys, 1),
                   ('nodes', Nodes, 2)]

class Object(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('token', Token),
                   ('num_of_values', prophy.u32),
                   ('values', prophy.array(prophy.i64, bound = 'num_of_values')),
                   ('num_of_updated_values', prophy.u32),
                   ('updated_values', prophy.bytes(bound = 'num_of_updated_values'))]

class Values(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('transaction_id', prophy.u32),
                   ('num_of_objects', prophy.u32),
                   ('objects', prophy.array(Object, bound = 'num_of_objects'))]
