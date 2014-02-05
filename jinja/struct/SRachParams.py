import aprot

class SRachParams(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('prachFreqOff',TPrachFreqOff),('prachConfIndex',TOaMPrachConfIndex),('raNondedPreamb',TRaNondedPreamb),('raPreambGrASize',ERaPreambGrASize),('raRespWinSize',ERaRespWinSize),('crntiParams',UCrntiParams),('raContResoT',ERaContResoT),('prachCS',TOaMPrachCS),('timerRaComp',TTimerRaComp),('raMsg3Thr',TRaMsg3Thr),('raMsg3ThrLowParameters',SRaMsg3ThrLowParameters),('raMsg3ThrCntParameters',SRaMsg3ThrCntParameters),('prachHsFlag',TBoolean)]
	
	