import sackparser.jinja.templates.LMGTT as LMGTT

lmgtt = LMGTT.LMGTT_UserDeactivateResp
lmgtt.status = 0x00000000
lmgtt.subunit = 0x00000010
lmgtt.cause = 0x00000000

print lmgtt
print repr(lmgtt.encode(">"))