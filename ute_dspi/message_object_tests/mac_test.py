from templates.generated.MAC import *


# class MAC_RadioBearerSetupReq(protophy.struct):

#     __metaclass__ = protophy.struct_generator

    # _descriptor = [('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('transactionId',TTransactionID), ('spsCrntiAllocationReq',TBoolean), ('ueSetupParams',SUeSetupParams), ('container',UWmpDcmUserContainer), ('cqiParams',SCqiParams), ('ueParams',SUeParams), ('tpcPdcchConfigParams',STpcPdcchConfigParams), ('soundingRsUlConfigDedicated',SSoundingRsUlConfigDedicated), ('numSRbs',TNumberOfItems), ('sRbInfoList',protophy.array(SSrbInfo,bound='numSRbs')), ('numDRbs',TNumberOfItems), ('drbInfoList',protophy.array(SRbInfo,bound='numDRbs'))]


print "==============MSG MAC_RadioBearerSetupReq=================="
mac = MAC_RadioBearerSetupReq()
print mac
mac.lnCelId = 10
print "==============SPhyDeployableNode=================="




print "==============MSG MAC_RadioBearerSetupReq=================="
# phy.DeployableNode.extend([struct])
print mac
print repr(mac.encode("<"))
print str(mac.encode("<"))

