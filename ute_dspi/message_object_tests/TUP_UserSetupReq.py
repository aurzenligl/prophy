from templates.generated import TUPu
import templates.header as Templates
import protophy
import binascii

class TUP_UserSetupReq(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('header',Templates.header),
                   ('payload',TUPu.TUP_UserSetupReq)]

str = '7E040064    00010000    00002353    12331110    10110308    00640008    0000CAFE    00009BD9    00000001    00000201    00000002    00000000    00000000    10110308    10110308    12331110    00000000    00000000    00000000    00000001    00000001    00000002    00000005    00000000    00000000    00000000    00000000'
str = str.replace(" ","")
tup = TUP_UserSetupReq()
print tup
print tup.payload._descriptor
#y = tup.decode(binascii.unhexlify(str),'>')
print TUP.SPlmnId()._descriptor