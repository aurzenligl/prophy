import aprot

class MAC_RlcDataBufferResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('dlRbMasterParam',SRingBufferDlParam),('dlRbSlaveParam',SRingBufferDlParam),('ulRbMasterParam',SRingBufferUlParam)]
	
	