import templates.header as Templates
from templates.UecSim import UecSim_ReconfigReq as s
import protophy
import binascii
from templates.generated import *


h = Templates.header()
print h     
ue = s() 
print ue

x='7E040024    00010000    000022DB    10110F30    10110308    00240000    00000000    12331110    12311104    12341105    10110308'
x=x.replace(" ", "")
print len(x)

print len(binascii.hexlify(ue.encode(">")))

#y = ue.decode(binascii.unhexlify(x),'>')
#print ue

