from sackparser.jinja.Out_files import *
import sackparser.jinja.Templates.header as Templates
import protophy
import binascii

class PHY_DlPhysicalChannelDeleteReq(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('header',Templates.header),
                   ('payload',PHY.PHY_DlPhysicalChannelDeleteReq)]
    

phy = PHY_DlPhysicalChannelDeleteReq()
str = '7E040014    00010000    00002762    12440F41    10110308    00140008    0000CAFE'
str=str.replace(" ", "")
y =phy.decode(binascii.unhexlify(str),'>')
print phy





