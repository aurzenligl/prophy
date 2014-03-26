# -*- coding: utf-8 -*-

import DataHolder
import IsarParser
import PythonSerializer

def parse(xml_string):
    return IsarParser.IsarParser().parse_string(xml_string)

def test_includes_parsing():
    xml = """\
<system xmlns:xi="http://www.nsn.com/2008/XInclude">
    <xi:include href="mydlo.xml"/>
    <xi:include href="szydlo.xml"/>
    <xi:include href="powidlo.xml"/>
</system>
"""

    holder = parse(xml)

    assert ["mydlo", "szydlo", "powidlo"] == holder.include

""" FIXME kl. don't test PythonSerializer together with IsarParser """

def test_of_error_in_SPuschReceiveReq():
    xml = ('<struct comment="" name="SPuschReceiveReq">\n'
           '   <member comment="" name="cqiRespDBuffer" type="SPhyDataBuffer"/>\n'
           '   <member comment="" name="measRespBuffer" type="SPhyDataBuffer"/>\n'
           '   <member comment="" name="measRespBuffer2" type="SPhyDataBuffer"/>\n'
           '   <member comment="" name="cellMeasRespBuffer" type="SPhyDataBuffer"/>\n'
           '   <member comment="" name="rfLoopFlag" type="TBoolean"/>\n'
           '   <member comment="" name="numOfDelayedUe" rangeDescription="0..MAX_PUSCH_UES_PER_TTI_5MHZ, 0..MAX_PUSCH_UES_PER_TTI_10MHZ, 0..MAX_PUSCH_UES_PER_TTI_15MHZ, 0..MAX_PUSCH_UES_PER_TTI_20MHZ" type="TNumberOfItems"/>\n'
           '   <member comment="" maxRange="MAX_UINT16" minRange="0" name="delayedUe" type="TCrntiU16">\n'
           '      <dimension minSize="1" size="MAX_PUSCH_UES_PER_TTI_20MHZ"/>\n'
           '   </member>\n'
           '   <member comment="" name="numOfSCellAddressingInfo" rangeDescription="For FSMr3: 0 MAX_NUM_SCELLS; For FSMr2: 0." type="TNumberOfItems"/>\n'
           '   <member comment="" maxRange="MAX_NUM_OF_PUSCH_RECEIVE_REQ" minRange="0" name="numOfUePuschReq" type="TNumberOfItems"/>\n'
           '   <member name="uePuschReq" type="SPuschUeReceiveReq">\n'
           '      <dimension size="THIS_IS_VARIABLE_SIZE_ARRAY"/>\n'
           '   </member>\n'
           '</struct>\n')

    dh = IsarParser.IsarParser().parse_string(xml)
    ps = PythonSerializer.PythonSerializer()
    """ FIXME kl. how does serialize relate to _serialize_msgs? These methods seem to do the same, but
    first one generates really weird formatting with abundance of newlines"""
    output = ps.serialize_string(dh)

    assert ("import prophy\n"
            "\n"
            "class SPuschReceiveReq(prophy.struct):\n"
            "    __metaclass__ = prophy.struct_generator\n"
            "    _descriptor = [('cqiRespDBuffer',SPhyDataBuffer), ('measRespBuffer',SPhyDataBuffer), ('measRespBuffer2',SPhyDataBuffer), ('cellMeasRespBuffer',SPhyDataBuffer), ('rfLoopFlag',TBoolean), ('numOfDelayedUe',TNumberOfItems), ('tmpName',TNumberOfItems), ('delayedUe',prophy.array(TCrntiU16,bound='tmpName')), ('numOfSCellAddressingInfo',TNumberOfItems), ('numOfUePuschReq',TNumberOfItems), ('uePuschReq',prophy.bytes(size=THIS_IS_VARIABLE_SIZE_ARRAY))]\n") == output

def test_of_backward_compatibility_serialization():
    xml = ('<struct comment="cmt0" name="SPuschUeReceiveMeasResp">\n'
           '    <member comment="cmt1" maxRange="MAX_UINT16" minRange="0" name="crnti" type="TCrntiU16"/>\n'
           '    <member comment="cmt2" name="ueIndex" type="TUeIndex"/>\n'
           '    <member comment="cmt3" maxRange="EStatusLte_NotOk" minRange="EStatusLte_Ok" name="status" type="EStatusLte"/>\n'
           '    <member comment="cmt4" name="specificCause" type="ESpecificCauseLte"/>\n'
           '    <member comment="cmt5" name="rssi" type="TRssi"/>\n'
           '    <member comment="cmt6" name="interferencePower" type="TInterferencePower"/>\n'
           '    <member comment="cmt7" name="frequencyOffsetPusch" type="TFrequencyOffset"/>\n'
           '    <member comment="cmt8" name="phiReal" type="TTimeEstPhi"/>\n'
           '    <member comment="cmt9" name="phiImag" type="TTimeEstPhi"/>\n'
           '    <member comment="cmt10" maxRange="400" minRange="-200" name="postCombSinr" type="i16"/>\n'
           '    <member comment="cmt11" name="ulCompUsage" rangeDescription="0...1" type="u8"/>\n'
           '    <member comment="cmt12" name="ulReliabilty" type="TBooleanU8"/>\n'
           '    <member comment="cmt13" defaultValue="0" name="subCellId" type="TSubCellIdU8"/>\n'
           '    <member name="explicitPadding1" type="u8"/>\n'
           '    <member name="explicitPadding2" type="u16"/>\n'
           '</struct>')

    dh = IsarParser.IsarParser().parse_string(xml)
    ps = PythonSerializer.PythonSerializer()
    output = ps._serialize_msgs(dh.struct_list)

    assert ("class SPuschUeReceiveMeasResp(prophy.struct):\n"
            "    __metaclass__ = prophy.struct_generator\n"
            "    _descriptor = [('crnti',TCrntiU16), ('ueIndex',TUeIndex), ('status',EStatusLte), ('specificCause',ESpecificCauseLte), ('rssi',TRssi), ('interferencePower',TInterferencePower), ('frequencyOffsetPusch',TFrequencyOffset), ('phiReal',TTimeEstPhi), ('phiImag',TTimeEstPhi), ('postCombSinr',prophy.i16), ('ulCompUsage',prophy.u8), ('ulReliabilty',TBooleanU8), ('subCellId',TSubCellIdU8), ('explicitPadding1',prophy.u8), ('explicitPadding2',prophy.u16)]\n") == output
