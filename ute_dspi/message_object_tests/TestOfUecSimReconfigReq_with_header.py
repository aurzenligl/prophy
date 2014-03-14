import templates.header as Templates
from sackparser.ute_dspi.templates.UecSim import *
import protophy
import binascii
from sackparser.ute_dspi.templates.generated import *


def open_message_with_header(Message,header = Templates.header):
    class Message(protophy.struct):
        __metaclass__ = protophy.struct_generator
        _descriptor = [('header',header),
                       ('payload',Message)]
    return Message()

msg = open_message_with_header(UecSim_ReconfigReq) 
print msg

x='7E040024    00010000    000022DB    10110F30    10110308    00240000    00000000    12331110    12311104    12341105    10110308'
x=x.replace(" ", "")
print len(x)

print len(binascii.hexlify(msg.encode(">")))

y = msg.decode(binascii.unhexlify(x),'>')
print msg
print binascii.hexlify(msg.encode(">"))

