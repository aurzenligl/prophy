import aprot

class SSpsCrntiReleaseInfo(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('status',EStatusLte),('specificCause',ESpecificCauseLte)]
	
	