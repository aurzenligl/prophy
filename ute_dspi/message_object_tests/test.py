from Out_files import *


phy = PHY.PHY_UlCompParamUpdateReq()
phy.lnCelId = 10 
phy.ulCoMPInfo.ulCoMpSinrThreshold = 20
print phy
print repr(phy.encode('<').__str__())

phy2 = PHY.PHY_AddressConfigReq()
phy2.transactionId = 10
struct = PHY.SPhyDeployableNode()
struct.nodeAddr = 10
struct.explicitPadding = 10
struct.nodeType = 10
phy2.DeployableNode.extend([struct])
struct.nodeType = 20
phy2.DeployableNode.extend([struct])
print phy2
