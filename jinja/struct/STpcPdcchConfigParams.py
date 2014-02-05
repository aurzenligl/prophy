import aprot

class STpcPdcchConfigParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('tpcPucchRnti',TTpcRnti),('tpcPucchIndexOfFormat3',TTpcIndex),('tpcPuschRnti',TTpcRnti),('tpcPuschIndexOfFormat3',TTpcIndex)]
	
	