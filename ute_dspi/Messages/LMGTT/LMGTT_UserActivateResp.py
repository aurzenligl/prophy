import sackparser.jinja.templates.LMGTT as LMGTT

lmgtt = LMGTT.LMGTT_UserActivateResp()
lmgtt.Status = 0x00000000
lmgtt.SubUnit = 0x00000010
lmgtt.Cause = 0x00000000

print lmgtt
print repr(lmgtt.encode(">"))