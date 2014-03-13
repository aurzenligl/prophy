import protophy
import binascii

from templates.generated.MAC import *


mac_req = MAC_RlcDataSendReq()

print mac_req
print mac_req._descriptor
print binascii.hexlify(mac_req.encode(">"))

mac2 = MAC_RlcDataSendReq()
mac2.decode(binascii.unhexlify("0000000000000100000000000000000000000000"),">")
print mac2