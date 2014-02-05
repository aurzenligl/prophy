import aprot

class SUeList(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ueId',TUeId),('drbIdList', aprot.bytes(size = 4)),('bearerReleaseIndCause',ESpecificCauseLte)]
	
	