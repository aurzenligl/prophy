import prophy 
from externals import *
from globals import *
from OAM_MERGED import *



1
TCdmaReferenceCellID = SOaMRttPreregRefCellId


class SCdmaFpcFch(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('initSetptRC11',TOaMFpcFchInitSetptRC11), ('initSetptRC12',TOaMFpcFchInitSetptRC12), ('initSetptRC3',TOaMFpcFchInitSetptRC3), ('initSetptRC4',TOaMFpcFchInitSetptRC4), ('initSetptRC5',TOaMFpcFchInitSetptRC5)]
class SCdmaMobilityParametersCDMA2000(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('sid',TOaMSid), ('nid',TOaMNid), ('multiSid',TOaMMultiSid), ('multiNid',TOaMMultiNid), ('regZone',TOaMRegZone), ('totalZones',TOaMTotalZone), ('zoneTimer',EOaMZoneTimer), ('prev',TOaMPRev), ('minPrev',TOaMMinPRev), ('auth',TOaMAuth), ('maxNumAltSo',TOaMMaxNumAltSo), ('bandClass',EOaMXparamBandClass), ('homeReg',TOaMHomeReg), ('foreignSigReg',TOaMForeignSidReg), ('foreignNidReg',TOaMForeignNidReg), ('powerUpReg',TOaMPowerUpReg), ('powerdownReg',TOaMPowerDownReg), ('parameterReg',TOaMParamReg), ('regPeriod',TOaMRegPeriod), ('prefMSIDType',EOaMPrefMSIDType), ('mcc',TOaMMccXrtt), ('imsi11and12',TOaMImsi11and12), ('imsiTSupported',TOaMImsiTSupported), ('fpcFch',SCdmaFpcFch), ('pilotInc',TOaMPilotInc), ('lpSec',TOaMLeapSecond), ('ltmOff',TOaMLocalTimeOff), ('dayLt',TOaMDayLt), ('gcsnaL2AckTimer',TOaMGcsnaL2AckTimer), ('gcsnaSeqCtxtTimer',TOaMGcsnaSequenceContextTimer)]
