from sackparser.ute_dspi.templates.generated.PHY import *
import sackparser.ute_dspi.templates.header as Templates
import protophy
import binascii

class Message(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('header',Templates.header),
                   ('payload',PHY_DlPhysicalChannelDeleteReq)]
    

phy = Message()
str = '7E040014    00010000    00002762    12440F41    10110308    00140008    0000CAFE'
str=str.replace(" ", "")
y =phy.decode(binascii.unhexlify(str),'>')
print phy





