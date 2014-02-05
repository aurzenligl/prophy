import aprot

class SVoLteThresholdParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('ulTalkSpurtUpperDataTh',TDataSize),('ulTalkSpurtLowerDataTh',TDataSize)]
	
	