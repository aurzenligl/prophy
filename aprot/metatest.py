import aprot

#class X(aprot.struct):
#    __metaclass__ = aprot.struct_generator()
#    _descriptor = [("len", aprot.u32,
#                   ("value", aprot.array(aprot.u32, size = 3, bound = "len"))]
#
#a = X()
#print repr(a.encode(">"))
#print a
#a.value[:] = [1,2,3]
#print repr(a.encode(">"))
#print a

#class Enumeration(aprot.enum8):
#    __metaclass__ = aprot.enum_generator
#    _enumerators = [("Enumeration_One", 1),
#                    ("Enumeration_Two", 2),
#                    ("Enumeration_Three", 3)]

class X(aprot.struct):
    __metaclass__ = aprot.struct_generator
    _descriptor = [("len", aprot.u8),
                   ("value", aprot.array(aprot.i8, bound = "len", shift = 5))]

x = X()
x.value[:] = [1,1,2]
print repr(x.encode(">"))
print x

x = X()
x.decode('\x08\x01\x01\x02', ">")
print repr(x.encode(">"))
print x

class Y(aprot.struct):
    __metaclass__ = aprot.struct_generator
    _descriptor = [("len", aprot.u8),
                   ("value", aprot.bytes(bound = "len", shift = 5))]
    
x = Y()
x.value = "bcd"
print repr(x.encode(">"))
print x

x = Y()
x.decode('\x08\x01\x01\x02', ">")
print x
print repr(x.encode(">"))
print x

