import aprot

class SHarqReleaseInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('servingCellIndex',aprot.u8),('ueIndex',TUeIndex),('crnti',aprot.u16),('harqId1',aprot.u8),('harqId2',aprot.u8),('validHarqId1',aprot.u8),('validHarqId2',aprot.u8),('ackReceivedHarqId1',aprot.u8),('ackReceivedHarqId2',aprot.u8),('lnCellIdServCell',TOaMLnCelId)]
	
	