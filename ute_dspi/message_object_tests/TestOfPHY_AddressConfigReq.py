from sackparser.ute_dspi.templates.generated.PHY import *
import binascii

print "==============MSG PHY_AddressConfigReq=================="
msg = PHY_AddressConfigReq()
msg.transactionId = 10
print msg
print binascii.hexlify(msg.encode("<"))

print "==============SPHYDeployableNode=================="
struct = SPhyDeployableNode()
struct.nodeAddr = 20
print struct

print "==============MSG PHY_AddressConfigReq=================="
msg.DeployableNode.extend([struct])
print msg
print repr(msg.encode("<"))
print binascii.hexlify(msg.encode("<"))