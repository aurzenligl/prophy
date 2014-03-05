import sackparser.jinja.Templates.UecSim as s
import binascii

ue =  s.UecSim_ReconfigResp()
ue.macUserBoard = 0x12
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

print dir(binascii)
print ue
print str(ue.encode(">"))
print repr(ue.encode(">"))