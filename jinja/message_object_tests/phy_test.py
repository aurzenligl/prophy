from Out_files import *

print "==============MSG PHY_AddressConfigReq=================="
phy = PHY.PHY_AddressConfigReq()
print phy
phy.transactionId = 10
phy.dupa1 = 20
print repr(phy.encode("<"))
print str(phy.encode("<"))
print "==============SPhyDeployableNode=================="
struct = PHY.SPhyDeployableNode()
print struct
struct.nodeAddr = 20
#struct.no1 = 10


print "==============MSG PHY_AddressConfigReq=================="
phy.DeployableNode.extend([struct])
print phy
print repr(phy.encode("<"))
print str(phy.encode("<"))