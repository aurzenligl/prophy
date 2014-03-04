import sackparser.jinja.Templates.header as Templates
import sackparser.jinja.Templates.UecSim as s
import protophy
import binascii

class UecSimReconfigReq(protophy.struct):
    __metaclass__ = protophy.struct_generator
    _descriptor = [('header',Templates.header),
                   ('payload',s.UecSim_ReconfigReq)]
    
ue = UecSimReconfigReq() 
print ue

x='7E040024    00010000    000022DB    10110F30    10110308    00240000    00000000    12331110    12311104    12341105    10110308'
x=x.replace(" ", "")
print len(x)

print len(binascii.hexlify(ue.encode(">")))

y = ue.decode(binascii.unhexlify(x),'>')
print ue
