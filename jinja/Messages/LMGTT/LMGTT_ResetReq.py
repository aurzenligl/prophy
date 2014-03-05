import sackparser.jinja.Templates.LMGTT as LMGTT

lmgtt = LMGTT.LMGTT_ResetReq()
lmgtt.spare = 0x00000000

print lmgtt
print repr(lmgtt.encode(">"))