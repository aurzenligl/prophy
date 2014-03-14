from sackparser.ute_dspi.templates.generated.MAC import *
import binascii




print "==============MSG MAC_RadioBearerSetupReq=================="
mac = MAC_RadioBearerSetupReq()
print mac
print 

print "==============Print elements of MAC_RadioBearerSetupReq=================="
print mac._descriptor


print "==============How to set element of MAC_RadioBearerSetupReq value=================="
mac.lnCelId = 10
mac.ueSetupParams.srEnable =10
print mac

print "==============How to set element of MAC_RadioBearerSetupReq value=================="
print repr(mac.encode("<"))

print "==============MSG MAC_RadioBearerSetupReq as readable string=================="
print binascii.hexlify(mac.encode("<"))

