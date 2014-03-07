from sackparser.jinja.Out_files import *
import sackparser.jinja.Templates.header as Templates
import protophy
import binascii

class MAC_UserSetupResp(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('header',Templates.header),
                   ('payload',MAC.MAC_UserSetupResp)]
    
mac2= MAC_UserSetupResp()
# print len(binascii.hexlify(mac2.encode(">")))
mac = MAC_UserSetupResp()
# str = '7E04007C    00010000    00002222    10110308    10110F30    007C0008    00000000    00000000    00000000    0000CAFE    00009BD9    00000001    00000000    00000201    00000000    00000000    00000000    00000000    00000000    00000000'
# str=str.replace(" ", "")
# y = mac.decode(binascii.unhexlify(str),'>')
# print len(str)

struct = MAC.SSRbList()
struct_d = MAC.SDRbList()

# mac.payload.sRbList.extend([struct])
# mac.payload.sRbList.extend([struct])
#mac.payload.dRbList.extend([struct_d])

print mac
 
# print mac
#  
# print len(binascii.hexlify(mac.encode(">")))
# print binascii.hexlify(mac.encode(">"))
# str2='7E04006C    00010000    00002222    10110308    10110F30    006C0008    00000000    00000000    00000000    0000CAFE    00009BD9    00000001    00000000    00000201    00000000    31303031    12331108    00000000    00000002    00000001    00000000    00000000    00000000    00000000    00000000    00000000    00000000    00000000'
# str2 = str2.replace(" ","")
# mac2.decode(binascii.unhexlify(str2),'>')


# print str2
# print mac.payload._descriptor
# print struct.messageResult._descriptor
# print struct._descriptor
# print struct_d._descriptor
# print len(binascii.hexlify(mac.encode(">")))
# 
# print binascii.hexlify(mac.encode(">"))
# print str2