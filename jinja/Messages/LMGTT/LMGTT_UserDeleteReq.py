import sackparser.jinja.Templates.LMGTT as LMGTT

lmgtt = LMGTT.LMGTT_UserDeleteReq()
lmgtt.cellid = 0x00000000
lmgtt.crnti = 0x00009BD9
lmgtt.ueid = 0x00000001
lmgtt.transactionid = 0x00000201

print lmgtt
print repr(lmgtt.encode(">"))