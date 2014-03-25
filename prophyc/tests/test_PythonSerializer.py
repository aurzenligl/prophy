# -*- coding: utf-8 -*-

import data_holder
import IsarParser
import PythonSerializer

""" FIXME kl. split Serializer and Parser tests"""

""" FIXME kl. this test is way too large. It needs to be split to multiple tests """
def test_of_PythonSerializer():
    ih = data_holder.IncludeHolder()
    th = data_holder.TypeDefHolder()
    for x in range(20, 200, 60):
        ih.add_to_list("test_include_" + str(x))
        th.add_to_list("td_elem_name_" + str(x), "td_elem_val_" + str(x))
        th.add_to_list("td_elem_name_" + str(x), "i_td_elem_val_" + str(x))
        th.add_to_list("td_elem_name_" + str(x), "u_td_elem_val_" + str(x))

    enum = data_holder.EnumHolder()
    for x in range(1, 100, 30):
        enum.add_to_list("elem_" + str(x), "val_" + str(x))

    const = data_holder.ConstantHolder()
    const.add_to_list("C_A", "5")
    const.add_to_list("C_B", "5")
    const.add_to_list("C_C", "C_B + C_A")

    msg_h = data_holder.MessageHolder()
    msg_h.name = "MAC_L2CallConfigResp"
    msg_h.add_to_list(data_holder.MemberHolder('messageResult', 'SMessageResult'))

    dh = data_holder.DataHolder(include = ih, typedef = th, constant = const, msgs_list = [msg_h])
    dh.enum_dict["test"] = enum

    ps = PythonSerializer.PythonSerializer()
    output = ps.serialize_to_string(dh)

    assert output == ("import prophy \n"
                      "from test_include_20 import *\n"
                      "from test_include_80 import *\n"
                      "from test_include_140 import *\n"
                      "\n"
                      "\n"
                      "C_B = 5\n"
                      "C_A = 5\n"
                      "C_C = C_B + C_A\n"
                      "\n"
                      "td_elem_name_20 = td_elem_val_20\n"
                      "td_elem_name_20 = prophy.i_td_elem_val_20\n"
                      "td_elem_name_20 = prophy.u_td_elem_val_20\n"
                      "td_elem_name_80 = td_elem_val_80\n"
                      "td_elem_name_80 = prophy.i_td_elem_val_80\n"
                      "td_elem_name_80 = prophy.u_td_elem_val_80\n"
                      "td_elem_name_140 = td_elem_val_140\n"
                      "td_elem_name_140 = prophy.i_td_elem_val_140\n"
                      "td_elem_name_140 = prophy.u_td_elem_val_140\n"
                      "\n"
                      "class test(prophy.enum):\n"
                      "    __metaclass__ = prophy.enum_generator\n"
                      "    _enumerators  = [('elem_1',val_1), ('elem_31',val_31), ('elem_61',val_61), ('elem_91',val_91)]\n"
                      "\n"
                      "class MAC_L2CallConfigResp(prophy.struct):\n"
                      "    __metaclass__ = prophy.struct_generator\n"
                      "    _descriptor = [('messageResult',SMessageResult)]\n")

def test_of_PythonSerializer_enum():
    enum = data_holder.EnumHolder()
    for x in range(1, 5):
        enum.add_to_list("elem_" + str(x), "val_" + str(x))

    ps = PythonSerializer.PythonSerializer()
    output = ps._serialize_enum({ "test" : enum })

    """ FIXME kl. it's better to list enumerators and fields from newlines, to make output human-readable """
    assert output == ("class test(prophy.enum):\n"
                      "    __metaclass__ = prophy.enum_generator\n"
                      "    _enumerators  = [('elem_1',val_1), ('elem_2',val_2), ('elem_3',val_3), ('elem_4',val_4)]\n")

def test_of_PythonSerializer_import():
    includes = ["test_include_" + str(x) for x in xrange(0, 15, 3)]

    ps = PythonSerializer.PythonSerializer()
    output = ps._serialize_include(includes)

    """ FIXME kl. there seems to be a surplus space character at the end of "import prophy" line"""
    assert output == ('import prophy \n'
                      'from test_include_0 import *\n'
                      'from test_include_3 import *\n'
                      'from test_include_6 import *\n'
                      'from test_include_9 import *\n'
                      'from test_include_12 import *\n')

""" FIXME kl. which error? this test doesn't assert anything, what are its expectations? """
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
    o = ps.serialize_to_string(dh)

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

    assert output == ("class SPuschUeReceiveMeasResp(prophy.struct):\n"
                      "    __metaclass__ = prophy.struct_generator\n"
                      "    _descriptor = [('crnti',TCrntiU16), ('ueIndex',TUeIndex), ('status',EStatusLte), ('specificCause',ESpecificCauseLte), ('rssi',TRssi), ('interferencePower',TInterferencePower), ('frequencyOffsetPusch',TFrequencyOffset), ('phiReal',TTimeEstPhi), ('phiImag',TTimeEstPhi), ('postCombSinr',prophy.i16), ('ulCompUsage',prophy.u8), ('ulReliabilty',TBooleanU8), ('subCellId',TSubCellIdU8), ('explicitPadding1',prophy.u8), ('explicitPadding2',prophy.u16)]\n")
