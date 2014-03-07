import sackparser.jinja.Templates.UecSim as s
import binascii
from struct import *

ue =  s.UecSim_ReconfigReq()
ue.macUserBoard = 0x18
ue.macUserCpu = 0x33
ue.macUserTask = 0x1110
ue.macSgnBoard = 0x12
ue.macSgnCpu = 0x31
ue.macSgnTask = 0x1104
ue.macUlCellBoard = 0x12
ue.macUlCellCpu = 0x34
ue.macUlCellTask = 0x1105
ue.ahtiBoard = 0x10
ue.ahtiCpu = 0x11
ue.ahtiTask = 0x0308

print ue
print dir(ue)
print str(ue.encode(">"))
print repr(ue.encode(">"))
print binascii.unhexlify(binascii.hexlify(ue.encode(">")))


x='12331110123111041234110510110308'
y = ue.decode(binascii.unhexlify(x),'>')
print ue
