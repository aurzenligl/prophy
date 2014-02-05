import aprot

class MAC_PcchDataSendReq(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('lnCelId',TCellId),('pagingItems', aprot.bytes(size = MAX_PAGING_ITEMS))]
	
	