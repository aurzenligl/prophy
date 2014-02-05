import aprot

class EMeasurementGroupTypeWmp(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('EMeasurementGroupTypeWmp_Pdcch_load_cell',6),
	 			    ('EMeasurementGroupTypeWmp_Last',7),
	 			    ('EMeasurementGroupTypeWmp_GBR_load_cell_UL',2),
	 			    ('EMeasurementGroupTypeWmp_nonGBR_load_cell_DL',5),
	 			    ('EMeasurementGroupTypeWmp_GBR_load_UE_UL',4),
	 			    ('EMeasurementGroupTypeWmp_NotDefined',0),
	 			    ('EMeasurementGroupTypeWmp_GBR_load_UE_DL',3),
	 			    ('EMeasurementGroupTypeWmp_GBR_load_cell_DL',1)]