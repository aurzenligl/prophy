import aprot

class SDlSchPduMuxCwAttributes(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('tbSize',TTbSize),('drxCommEnable',TBooleanU8),('ueTaCeAvail',TBooleanU8),('ueTaCeValue',aprot.u16),('ueCaCeInfo',SCaCeInfo),('tfi',TMcs),('modulation',TEModulationU8),('newDataIndicator',TNewDataIndicatorU8),('redundancyVersion',TRedundancyVersionU8),('codeWordIndex',TCodeWordIndexU8),('harqIdCw',THarqProcessNumberU8),('trnumCw',aprot.u8),('amountRbs',aprot.u8),('amountRbOctets', aprot.bytes(size = MAX_NUM_RB_PER_USER))]
	
	