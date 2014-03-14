import prophy 
from externals import *
from globals import *
from OAM_MERGED import *
from ASN import *
from ASN import *
from ASN import *
from ASN import *
from ASN import *
from ASN import *
from ASN import *
from ASN import *
from ASN import *
from ASN import *

URimApplicationContainer = prophy.i32
URimSIorPSI = prophy.i32
URimRoutingInformation = prophy.i32
URimPDUIndicationExtension = prophy.i32
URimENBID = prophy.i32
URimApplication = prophy.i32
URimReportingCellIdentifier = prophy.i32
URimApplicationErrorContainerCause = prophy.i32

RIM_RANGE_SI3 = 21
RIM_RANGE_PSI = 22
RIM_RANGE_SI = 21
RIM_RANGE_SI_OR_PSI = 127
RIM_RANGE_SEQUENCE_NUMBER = 4
RIM_RANGE_HOME_ENB_ID = 4
RIM_RANGE_MACRO_ENB_ID = 3
RIM_RANGE_TAC = 2
RIM_RANGE_RAC = 1
RIM_RANGE_CI = 2
RIM_RANGE_LAC = 2

TRimRNCID = prophy.i32
1
TRimSONTransferRequestContainer = SAsnDynstr
TRimSONTransferApplicationContainer = SAsnDynstr
SRimMBMSDataChannelReport = SAsnDynstr
SRimSONTransferResponseContainer = SAsnDynstr
SRimUTRASIContainer = SAsnDynstr
SRimSONTransferApplicationCause = SAsnDynstr
TRimErrorPDU = SAsnDynstr

class ERimInformationRequestRIMPDUIndication(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERimInformationRequestRIMPDUIndication_Stop',0), ('ERimInformationRequestRIMPDUIndication_SingleReport',1), ('ERimInformationRequestRIMPDUIndication_MultipleReport',2)]
class ERimUTRASICause(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERimUTRASICause_Unspecified',0), ('ERimUTRASICause_SyntaxErrorInApplicationContainer',1), ('ERimUTRASICause_InconsistentReportingCellIdentifier',2)]
class ERimCause(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERimCause_ProcessorOverload',0), ('ERimCause_EquipmentFailure',1), ('ERimCause_TransitNetworkServiceFailure',2), ('ERimCause_NetworkServiceTransmissionCapacityModifiedFromZeroKbpsToGreaterThanZeroKbps',3), ('ERimCause_UnknownMS',4), ('ERimCause_BVCIUnknown',5), ('ERimCause_CellTrafficCongestion',6), ('ERimCause_SGSNCongestion',7), ('ERimCause_OAMIntervention',8), ('ERimCause_BVCIBlocked',9), ('ERimCause_PFCCreateFailure',10), ('ERimCause_PFCPreempted',11), ('ERimCause_ABQPNoMoreSupported',12), ('ERimCause_SemanticallyIncorrectPDU',32), ('ERimCause_InvalidMandatoryInformation',33), ('ERimCause_MissingMandatoryIE',34), ('ERimCause_MissingConditionalIE',35), ('ERimCause_UnexpectedConditionalIE',36), ('ERimCause_ConditionalIEError',37), ('ERimCause_PDUNotCompatibleWithTheProtocolState',38), ('ERimCause_ProtocolErrorUnspecified',39), ('ERimCause_PDUNotCompatibleWithTheFeatureSet',40), ('ERimCause_RequestedInformationNotAvailable',41), ('ERimCause_UnknownDestinationAddress',42), ('ERimCause_UnknownRIMApplicationIdentityOrRIMApplicationDisabled',43), ('ERimCause_InvalidContainerUnitInformation',44), ('ERimCause_PFCQueuing',45), ('ERimCause_PFCCreatedSuccessfully',46), ('ERimCause_T12Expiry',47), ('ERimCause_MSUnderPSHandoverTreatment',48), ('ERimCause_UplinkQuality',49), ('ERimCause_UplinkStrength',50), ('ERimCause_DownlinkQuality',51), ('ERimCause_DownlinkStrength',52), ('ERimCause_Distance',53), ('ERimCause_BetterCell',54), ('ERimCause_Traffic',55), ('ERimCause_RadioContactLostWithMS',56), ('ERimCause_MSBackOnOldChannel',57), ('ERimCause_T13Expiry',58), ('ERimCause_T14Expiry',59), ('ERimCause_NotAllRequestedPFCsCreated',60), ('ERimCause_CSCause',61), ('ERimCause_RequestedCipheringAndOrIntegrityProtectionAlgorithmsNotSupported',62), ('ERimCause_RelocationFailureInTargetSystem',63), ('ERimCause_DirectedRetry',64), ('ERimCause_TimeCriticalRelocation',65), ('ERimCause_PSHandoverTargetNotAllowed',66), ('ERimCause_PSHandoverNotSupportedInTargetBSSOrTargetSystem',67), ('ERimCause_IncomingRelocationNotSupportedDueToPUESBINEFeature',68), ('ERimCause_DTMHandoverNoCSResource',69), ('ERimCause_DTMHandoverPSAllocationFailure',70), ('ERimCause_DTMHandoverT24Expiry',71), ('ERimCause_DTMHandoverInvalidCSIndicationIE',72), ('ERimCause_DTMHandoverT23Expiry',73), ('ERimCause_DTMHandoverMSCError',74), ('ERimCause_InvalidCSGCell',75), ('ERimCause_Reserved',128)]
class ERimSIType(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERimSIType_BCCH',0), ('ERimSIType_PBCCH',1)]
class ERimNACCCause(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERimNACCCause_OtherUnspecifiedError',0), ('ERimNACCCause_SyntaxErrorInApplicationContainer',1), ('ERimNACCCause_ReportingCellDoesNotMatch',2), ('ERimNACCCause_SIOrPSITypeError',3), ('ERimNACCCause_InconsistentLenghtofSIOrPSIMessage',4), ('ERimNACCCause_InconsistentSetOfMessages',5)]
class ERimMBMSDataChannelCause(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERimMBMSDataChannelCause_OtherUnspecifiedError',0), ('ERimMBMSDataChannelCause_SyntaxErrorInApplicationContainer',1), ('ERimMBMSDataChannelCause_ReportingCellDoesNotMatch',2), ('ERimMBMSDataChannelCause_RIMReportPDUExceedsMaximumSupportedLenght',3), ('ERimMBMSDataChannelCause_InconsistentMBMSDataChannelDescription',4)]
class ERimApplicationIdentity(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERimApplicationIdentity_NACC',0), ('ERimApplicationIdentity_SI3',1), ('ERimApplicationIdentity_MBMSDataChannel',2), ('ERimApplicationIdentity_SONTransfer',3), ('ERimApplicationIdentity_UTRASI',4)]
class ERimSI3Cause(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERimSI3Cause_OtherUnspecifiedError',0), ('ERimSI3Cause_SyntaxErrorInApplicationContainer',1), ('ERimSI3Cause_ReportingCellDoesNotMatch',2), ('ERimSI3Cause_InconsistentLenghtofSI3Message',3)]
class ERimInformationRIMPDUIndication(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERimInformationRIMPDUIndication_Stop',0), ('ERimInformationRIMPDUIndication_SingleReport',1), ('ERimInformationRIMPDUIndication_InitialMultipleReport',2), ('ERimInformationRIMPDUIndication_MultipleReport',3), ('ERimInformationRIMPDUIndication_End',4)]
class ERimProtocolVersionNumber(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('ERimProtocolVersionNumber_Version1',0)]

class SRimLAC(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('st',prophy.bytes(size=RIM_RANGE_LAC))]
class SRimCI(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('st',prophy.bytes(size=RIM_RANGE_CI))]
class SRimRAC(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('st',prophy.bytes(size=RIM_RANGE_RAC))]
class SRimCellIdentifier(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('pLMNidentity',SPlmnId), ('lAC',SRimLAC), ('rAC',SRimRAC), ('cI',SRimCI)]
class SRimUTRANCellIdentifier(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('pLMNidentity',SPlmnId), ('lAC',SRimLAC), ('rAC',SRimRAC), ('rNCID',TRimRNCID)]
class SRimTAC(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('st',prophy.bytes(size=RIM_RANGE_TAC))]
class SRimMacroENBID(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('st',prophy.bytes(size=RIM_RANGE_MACRO_ENB_ID))]
class SRimHomeENBID(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('st',prophy.bytes(size=RIM_RANGE_HOME_ENB_ID))]
class SRimGlobalENBID(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('pLMNidentity',SPlmnId), ('eNBID',URimENBID)]
class SRimEUTRANCellIdentifier(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('pLMNidentity',SPlmnId), ('tAC',SRimTAC), ('globalEnbId',SRimGlobalENBID)]
class SRimSequenceNumber(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('st',prophy.bytes(size=RIM_RANGE_SEQUENCE_NUMBER))]
class SRimPDUIndications(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('ack',TAsnBoole), ('extension',URimPDUIndicationExtension)]
class SRimEUTRANCGI(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('pLMNidentity',SPlmnId), ('cellID',TOaMEutraCelId)]
class SRimUTRANSourceCellID(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('pLMNidentity',SPlmnId), ('sourceCellID',prophy.u32)]
class SRimApplicationRequestContainer(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('reportingCellId',URimReportingCellIdentifier), ('sONTransferRequestContainer',TRimSONTransferRequestContainer)]
class SRimSONTransferApplicationIdentity(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sONTransferApplicationContainer',TRimSONTransferApplicationContainer)]
class SRimApplicationContainer(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('reportingCellId',URimReportingCellIdentifier), ('application',URimApplication)]
class SRimSI(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('st',prophy.bytes(size=RIM_RANGE_SI))]
class SRimPSI(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('st',prophy.bytes(size=RIM_RANGE_PSI))]
class SRimSIorPSI(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('numerOfSIorPSI',u8), ('elem',prophy.array(URimSIorPSI,bound='numerOfSIorPSI'))]
class SRimNACC(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sIorPSI',SRimSIorPSI)]
class SRimSI3(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('st',prophy.bytes(size=RIM_RANGE_SI3))]
class SRimInformationRequestContainer(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('applicationId',ERimApplicationIdentity), ('sequenceNumber',SRimSequenceNumber), ('pDUIndications',SRimPDUIndications), ('version',ERimProtocolVersionNumber), ('container',URimApplicationContainer), ('sONTransferId',SRimSONTransferApplicationIdentity)]
class SRimApplicationErrorContainer(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('cause',URimApplicationErrorContainerCause), ('erroneousContainer',URimApplicationContainer)]
class SRimInformationContainer(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('applicationId',ERimApplicationIdentity), ('sequenceNumber',SRimSequenceNumber), ('pDUIndications',SRimPDUIndications), ('version',ERimProtocolVersionNumber), ('container',URimApplicationContainer), ('applicatonErrorContainer',SRimApplicationErrorContainer), ('sONTransferId',SRimSONTransferApplicationIdentity)]
class SRimInformationAckContainer(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('applicationId',ERimApplicationIdentity), ('sequenceNumber',SRimSequenceNumber), ('version',ERimProtocolVersionNumber), ('sONTransferId',SRimSONTransferApplicationIdentity)]
class SRimInformationErrorContainer(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('applicationId',ERimApplicationIdentity), ('cause',ERimCause), ('version',ERimProtocolVersionNumber), ('errorPDU',TRimErrorPDU), ('sONTransferId',SRimSONTransferApplicationIdentity)]
class SRimInformationApplicationErrorContainer(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('applicationId',ERimApplicationIdentity), ('sequenceNumber',SRimSequenceNumber), ('pDUIndications',SRimPDUIndications), ('version',ERimProtocolVersionNumber), ('applicatonErrorContainer',SRimApplicationErrorContainer), ('sONTransferId',SRimSONTransferApplicationIdentity)]
class SRimRanInformationRequest(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('destinationCellId',URimRoutingInformation), ('sourceCellId',URimRoutingInformation), ('rIMRequestContainer',SRimInformationRequestContainer)]
class SRimRanInformation(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('destinationCellId',URimRoutingInformation), ('sourceCellId',URimRoutingInformation), ('rIMContainer',SRimInformationContainer)]
class SRimRanInformationAck(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('destinationCellId',URimRoutingInformation), ('sourceCellId',URimRoutingInformation), ('rIMAckContainer',SRimInformationAckContainer)]
class SRimRanInformationError(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('destinationCellId',URimRoutingInformation), ('sourceCellId',URimRoutingInformation), ('rIMErrorContainer',SRimInformationErrorContainer)]
class SRimRanInformationApplicationError(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('destinationCellId',URimRoutingInformation), ('sourceCellId',URimRoutingInformation), ('rIMApplicationErrorContainer',SRimInformationApplicationErrorContainer)]
