from sackparser.jinja.Out_files import *
import sackparser.jinja.Templates.header as Templates
import protophy
import binascii

class MAC_CcchDataSendReq(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('header',Templates.header),
                   ('payload',MAC.MAC_CcchDataSendReq)]

mac = MAC_CcchDataSendReq()

print mac.payload._descriptor

str2= '7E040025    00010000    0000235F    10110308    10110F30    00250008    0000CAFE    00009BD9    00000006    40000000    0010'
str2 = str2.replace(" ","")
mac.decode(binascii.unhexlify(str2),'>')
print mac