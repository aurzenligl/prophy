import aprot

class SBbResourceRoom(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('nbrOfDlSpsUe',TMeasurementValue),('nbrOfUlSpsUe',TMeasurementValue),('unsuccessDlSpsAssignsNdiscDlAck',TMeasurementValue),('unsuccessDlSpsAssignsNdiscDl',TMeasurementValue),('unsuccessDlSpsAssignsNdiscUl',TMeasurementValue)]
	
	