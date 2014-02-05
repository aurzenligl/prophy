import aprot

class SPdcchLoadCell(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('averCellsPdcchLoad',TMeasurementValue)]
	
	