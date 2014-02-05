import aprot

class EMeasurementGroupType(aprot.enum):
	__metaclass__ = aprot.enum_generator
	_enumerators = [('EMeasurementGroupType_PHICH_Transmit_Power',14),
	 			    ('EMeasurementGroupType_PRACH_UsageRatio',1),
	 			    ('EMeasurementGroupType_Channel_Usage_Status',7),
	 			    ('EMeasurementGroupType_MAC_PDU_Transmission_Rate',3),
	 			    ('EMeasurementGroupType_Number_Of_Voice_UE',19),
	 			    ('EMeasurementGroupType_Interference_Level',8),
	 			    ('EMeasurementGroupType_Pathloss',9),
	 			    ('EMeasurementGroupType_Transmitted_And_Received_Power',2),
	 			    ('EMeasurementGroupType_RaPreambleStatistics',15),
	 			    ('EMeasurementGroupType_PDCCH_Usage_Ratio',17),
	 			    ('EMeasurementGroupType_Channel_Usage_Status2',22),
	 			    ('EMeasurementGroupType_NotDefined',0),
	 			    ('EMeasurementGroupType_Persistent_RB_Usage',6),
	 			    ('EMeasurementGroupType_MAC_SDU_Transmission_And_Reception_Rate',18),
	 			    ('EMeasurementGroupType_Nbr_LogCH_Meas_Type1',10),
	 			    ('EMeasurementGroupType_RLC_PDCP_Traffic',5),
	 			    ('EMeasurementGroupType_Nbr_Of_DRX_UE',4),
	 			    ('EMeasurementGroupType_BB_Resource_Room',13),
	 			    ('EMeasurementGroupType_Nbr_LogCH_Meas_Type3',12),
	 			    ('EMeasurementGroupType_PRACH_UsageRatio_2',20),
	 			    ('EMeasurementGroupType_Nbr_LogCH_Meas_Type2',11),
	 			    ('EMeasurementGroupType_Resource_Block_Usage_Ratio',16),
	 			    ('EMeasurementGroupType_SCell_Status',21)]