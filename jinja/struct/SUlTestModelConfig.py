import aprot

class SUlTestModelConfig(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('noOfHarqTransmissions',ENoOfHarqTransmissions),('hstConfig',EHstConfig),('resourceIndexCqi',TResourceIndexCqi),('iCqiPmi',TICqiPmi)]
	
	