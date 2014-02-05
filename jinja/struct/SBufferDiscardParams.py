import aprot

class SBufferDiscardParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('thOverflowDiscard',TThOverflowDiscard),('flagOverflowDiscard',TFlagOverflowDiscard),('discBuffThrAct',TBoolean),('discBuffHighThr',TDiscBuffThr)]
	
	