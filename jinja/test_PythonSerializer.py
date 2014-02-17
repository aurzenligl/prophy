# -*- coding: utf-8 -*-

import sys
import hashlib

import data_holder
import writer

linux_hashes = {
"test_of_PythonSerializer" : "5c2d6d350fdea2c825ed8e8fcd875f10",
"test_of_PythonSerializer_enum" : "26f524cefc1243e04e18bbee34eac884",
"test_of_PythonSerializer_import" : "da45c13ad54818957c1b932d8beb56f4"
}

windows_hashes = {
"test_of_PythonSerializer" : "af8c4ee390b6e906d2dfdf9336bf90c9",
"test_of_PythonSerializer_enum" : "275bf674a0c1025d10e929b39896213f",
"test_of_PythonSerializer_import" : "42b158e97a9e205de2178d6befaeed35"
}

hashes = linux_hashes if sys.platform == "linux2" else windows_hashes

def test_of_PythonSerializer():

    ih = data_holder.IncludeHolder()
    th = data_holder.TypeDefHolder()

    for x in range(20, 400, 60):
        ih.add_to_list("test_include_"+str(x))
        th.add_to_list("td_elem_name_"+str(x), "td_elem_val_"+str(x))
        th.add_to_list("td_elem_name_"+str(x), "i_td_elem_val_"+str(x))
        th.add_to_list("td_elem_name_"+str(x), "u_td_elem_val_"+str(x))

    enum = data_holder.EnumHolder()
    for x in range(1, 200, 30):
        enum.add_to_list("elem_" + str(x), "val_"+ str(x))

    const = data_holder.ConstantHolder()
    const.add_to_list("C_A","5")
    const.add_to_list("C_B","5")
    const.add_to_list("C_C", "C_B + C_A")


    msg_h = data_holder.MessageHolder()
    msg_h.name = "MAC_L2CallConfigResp"
    msg_h.add_to_list(data_holder.MemberHolder('messageResult','SMessageResult'))


    dh = data_holder.DataHolder( include = ih, typedef = th , constant = const, msgs_list = [msg_h])
    dh.enum_dict["test"] = enum

    ps = writer.PythonSerializer()
    o =  ps.serialize(dh)
    assert hashes["test_of_PythonSerializer"] == hashlib.md5( o ).hexdigest()


def test_of_PythonSerializer_enum():
    ps = writer.PythonSerializer()
    enum = data_holder.EnumHolder()
    for x in range(1, 200):
        enum.add_to_list("elem_" + str(x), "val_"+ str(x))
    o =  ps._serialize_enum( { "test" : enum } )
    assert hashes["test_of_PythonSerializer_enum"] ==  hashlib.md5(o).hexdigest()


def test_of_PythonSerializer_import():
    l = []
    for x in range(20, 400, 3):
        l.append("test_include_"+str(x))
    ps = writer.PythonSerializer()
    o = ps._serialize_include(l)
    assert hashes["test_of_PythonSerializer_import"] == hashlib.md5(o).hexdigest()

def test_of_error_in_SPuschReceiveReq():
    xml = """
         <struct comment="" name="SPuschReceiveReq">
            <member comment="" name="cqiRespDBuffer" type="SPhyDataBuffer"/>
            <member comment="" name="measRespBuffer" type="SPhyDataBuffer"/>
            <member comment="" name="measRespBuffer2" type="SPhyDataBuffer"/>
            <member comment="" name="cellMeasRespBuffer" type="SPhyDataBuffer"/>
            <member comment="" name="rfLoopFlag" type="TBoolean"/>
            <member comment="" name="numOfDelayedUe" rangeDescription="0..MAX_PUSCH_UES_PER_TTI_5MHZ, 0..MAX_PUSCH_UES_PER_TTI_10MHZ, 0..MAX_PUSCH_UES_PER_TTI_15MHZ, 0..MAX_PUSCH_UES_PER_TTI_20MHZ" type="TNumberOfItems"/>
            <member comment="" maxRange="MAX_UINT16" minRange="0" name="delayedUe" type="TCrntiU16">
               <dimension minSize="1" size="MAX_PUSCH_UES_PER_TTI_20MHZ"/>
            </member>
            <member comment="" name="numOfSCellAddressingInfo" rangeDescription="For FSMr3: 0… MAX_NUM_SCELLS; For FSMr2: 0." type="TNumberOfItems"/>
            <member comment="" maxRange="MAX_NUM_OF_PUSCH_RECEIVE_REQ" minRange="0" name="numOfUePuschReq" type="TNumberOfItems"/>
            <member name="uePuschReq" type="SPuschUeReceiveReq">
               <dimension size="THIS_IS_VARIABLE_SIZE_ARRAY"/>
            </member>
         </struct>
"""
    from xml.dom import minidom
    xml_dom_model = minidom.parseString(xml)
    import Parser
    dh =  Parser.Parser().parsing_xml_files(xml_dom_model)
    o = writer.PythonSerializer().serialize(dh)

def test_of_backward_compatibility_serialization():
    xml = """
         <struct comment="Structure contains PUSCH related measurements of one UE." name="SPuschUeReceiveMeasResp">
            <member comment="Since a CRNTI can appear only once per subframe, it can be used as a transaction id. Value is copied from PUCCH request." maxRange="MAX_UINT16" minRange="0" name="crnti" type="TCrntiU16"/>
            <member comment="UE Index." name="ueIndex" type="TUeIndex"/>
            <member comment="The status of response which can be Ok or NotOk. If status is NotOk results are not valid." maxRange="EStatusLte_NotOk" minRange="EStatusLte_Ok" name="status" type="EStatusLte"/>
            <member comment="If status is EStatusLte_NotOk, the cause field tell more detailed explanation about the error.&#13;&#10;The following cause fields are used.&#13;&#10;- ESpecificCauseLte_PHY_InvalidParam&#13;&#10;  Some parameter is erronous or not in the valid range.&#13;&#10;- ESpecificCauseLte_PHY_NotEnoughResources&#13;&#10;  There was not enough resources for UE processing&#13;&#10;- ESpecificCauseLte_PHY_DeadlineMissed&#13;&#10;  There was not enough time to process the UE" name="specificCause" type="ESpecificCauseLte"/>
            <member comment="RSSI measurement result as mW.&#13;&#10;RSSI is Ue's signal power normalized to one PRB  without interference and noise. This is the M1 measurement in the SFS.&#13;&#10;RSSI is sum over all diversity antennas.&#13;&#10;The number format is IEEE-754 32-bit Single Precision floating point." name="rssi" type="TRssi"/>
            <member comment="This is the K1  interference power measurement defined in the SFS.&#13;&#10;Interfence power is average over all diversity antennas.&#13;&#10;The number format is IEEE-754 32-bit Single Precision floating point." name="interferencePower" type="TInterferencePower"/>
            <member comment="PUSCH frequency offset information packed by PHY for storage in MAC.&#13;&#10;If frequencyOffsetPusch=FREQUENCY_OFFSET_NOT_VALID this value is invalid and shall not be stored by MAC. " name="frequencyOffsetPusch" type="TFrequencyOffset"/>
            <member comment="The real part of Phi estimate for Timing Advance (TA) measurements.&#13;&#10;PHY sets both phiImag and phiReal to 0 if the TA measurements are not reliable.&#13;&#10;" name="phiReal" type="TTimeEstPhi"/>
            <member comment="The imaginary part of Phi estimate for Timing Advance (TA) measurements.&#13;&#10;PHY sets both phiImag and phiReal to 0 if the TA measurements are not reliable." name="phiImag" type="TTimeEstPhi"/>
            <member comment="Ue's SINR in dB calculated after combining for UL PC purpose.&#13;&#10;In the defined range one integer digit corresponds to 0.1 dB. For example, if postCombSinr = 100, Ue’s SINR is 100*0.1 dB = 10 dB.&#13;&#10;&#13;&#10;The parameter is not used in TDD and DCM.&#13;&#10;" maxRange="400" minRange="-200" name="postCombSinr" type="i16"/>
            <member comment="0 – Only serving cell antennas are used for PUSCH reception in this TTI&#13;&#10;1 – Also neighbor cell antennas are used for PUSCH reception in this TTI" name="ulCompUsage" rangeDescription="0...1" type="u8"/>
            <member comment="This flag is used to indicate to the recipient if the UL PHY considered UL transmission as unreliable (GLO_FALSE) or reliable (GLO_TRUE)." name="ulReliabilty" type="TBooleanU8"/>
            <member comment="TDD specific parameter. Indicate the sub cell which the measurement is implemented." defaultValue="0" name="subCellId" type="TSubCellIdU8"/>
            <member name="explicitPadding1" type="u8"/>
            <member name="explicitPadding2" type="u16"/>
         </struct>
"""
    from xml.dom import minidom
    xml_dom_model = minidom.parseString(xml)
    import Parser
    dh =  Parser.Parser().parsing_xml_files(xml_dom_model)
    o = writer.PythonSerializer()._serialize_msgs(dh.struct_list)
    c = """class SPuschUeReceiveMeasResp(aprot.struct):
    __metaclass__ = aprot.struct_generator
    _descriptor = [('crnti',TCrntiU16), ('ueIndex',TUeIndex), ('status',EStatusLte), ('specificCause',ESpecificCauseLte), ('rssi',TRssi), ('interferencePower',TInterferencePower), ('frequencyOffsetPusch',TFrequencyOffset), ('phiReal',TTimeEstPhi), ('phiImag',TTimeEstPhi), ('postCombSinr',aprot.i16), ('ulCompUsage',aprot.u8), ('ulReliabilty',TBooleanU8), ('subCellId',TSubCellIdU8), ('explicitPadding1',aprot.u8), ('explicitPadding2',aprot.u16)]
"""
    assert c == o
