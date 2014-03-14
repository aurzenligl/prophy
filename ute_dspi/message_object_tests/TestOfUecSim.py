from sackparser.ute_dspi.templates.UecSim import *
import binascii


msg =  UecSim_ReconfigReq()
msg.macUserBoard = 0x18
msg.macUserCpu = 0x33
msg.macUserTask = 0x1110
msg.macSgnBoard = 0x12
msg.macSgnCpu = 0x31
msg.macSgnTask = 0x1104
msg.macUlCellBoard = 0x12
msg.macUlCellCpu = 0x34
msg.macUlCellTask = 0x1105
msg.ahtiBoard = 0x10
msg.ahtiCpu = 0x11
msg.ahtiTask = 0x0308

print msg

print binascii.hexlify(msg.encode(">"))

