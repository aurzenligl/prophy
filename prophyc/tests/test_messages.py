import DataHolder
import PythonSerializer
import reader

def generate_python_msg(msg_holder):
    return PythonSerializer.PythonSerializer()._serialize_msgs([msg_holder])

def test_of_message_simple():
    msg_h = DataHolder.MessageHolder()
    msg_h.name = "MAC_L2CallConfigResp"
    msg_h.add_to_list(DataHolder.MemberHolder('messageResult', 'SMessageResult'))
    msg_h.add_to_list(DataHolder.MemberHolder('lnCelId', 'TCellId'))
    msg_h.add_to_list(DataHolder.MemberHolder('crnti', 'TCrnti'))

    assert ("class MAC_L2CallConfigResp(prophy.struct):\n"
            "    __metaclass__ = prophy.struct_generator\n"
            "    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti)]\n") == generate_python_msg(msg_h)

def test_of_message_with_four_dim_without_field_type():
    member_h = DataHolder.MemberHolder('sRbList', 'SSRbList')
    member_h.add_to_list("isVariableSize", "true")
    member_h.add_to_list("minSize", "1")
    member_h.add_to_list("size", "MAX_NUM_SRB_PER_USER")
    member_h.add_to_list("variableSizeFieldName", "numSRbs")

    msg_h = DataHolder.MessageHolder()
    msg_h.name = "MAC_L2CallConfigResp"
    msg_h.add_to_list(member_h)

    assert ("class MAC_L2CallConfigResp(prophy.struct):\n"
            "    __metaclass__ = prophy.struct_generator\n"
            "    _descriptor = [('numSRbs',TNumberOfItems), ('sRbList',prophy.array(SSRbList,bound='numSRbs'))]\n") == generate_python_msg(msg_h)

def test_of_message_with_five_dim():
    member_h = DataHolder.MemberHolder('msg3Info', 'SMsg3Info')
    member_h.add_to_list("isVariableSize", "true")
    member_h.add_to_list("minSize", "1")
    member_h.add_to_list("size", "MAX_MSG3_PER_TTI")
    member_h.add_to_list("variableSizeFieldName", "maxNumOfUes")
    member_h.add_to_list("variableSizeFieldType", "u32")

    msg_h = DataHolder.MessageHolder()
    msg_h.name = "MAC_CcchDataReceiveInd"
    msg_h.add_to_list(member_h)

    assert ("class MAC_CcchDataReceiveInd(prophy.struct):\n"
            "    __metaclass__ = prophy.struct_generator\n"
            "    _descriptor = [('maxNumOfUes',u32), ('msg3Info',prophy.array(SMsg3Info,bound='maxNumOfUes'))]\n") == generate_python_msg(msg_h)

def test_of_message_with_four_dim_without_min_size():
    member_h = DataHolder.MemberHolder('data', 'u8')
    member_h.add_to_list("isVariableSize", "true")
    member_h.add_to_list("size", "MAX_SI_DATA")
    member_h.add_to_list("variableSizeFieldName", "size")
    member_h.add_to_list("variableSizeFieldType", "TL3MsgSize")

    msg_h = DataHolder.MessageHolder()
    msg_h.name = "SSiList"
    msg_h.add_to_list(member_h)

    assert ("class SSiList(prophy.struct):\n"
            "    __metaclass__ = prophy.struct_generator\n"
            "    _descriptor = [('size',TL3MsgSize), ('data',prophy.array(u8,bound='size'))]\n") == generate_python_msg(msg_h)

def test_of_message_with_three_fields_without_variable_name_and_variable_type():
    member_h = DataHolder.MemberHolder('rlcDlLcpInfo', 'SRlcLcpInfo')
    member_h.add_to_list("isVariableSize", "true")
    member_h.add_to_list("size", "MAX_SI_DATA")
    member_h.add_to_list("minSize", "1")

    msg_h = DataHolder.MessageHolder()
    msg_h.name = "MAC_CellSetupReq"
    msg_h.add_to_list(member_h)

    assert ("class MAC_CellSetupReq(prophy.struct):\n"
            "    __metaclass__ = prophy.struct_generator\n"
            "    _descriptor = [('tmpName',TNumberOfItems), ('rlcDlLcpInfo',prophy.array(SRlcLcpInfo,bound='tmpName'))]\n") == generate_python_msg(msg_h)

def test_of_message_with_two_fields_size_and_isVariable():
    member_h = DataHolder.MemberHolder('measurementGroupTypeList', 'EMeasurementGroupType')
    member_h.add_to_list("isVariableSize", "true")
    member_h.add_to_list("size", "MAX_MEAS_GROUP_TYPE_ID_MAC")

    msg_h = DataHolder.MessageHolder()
    msg_h.name = "MAC_MeasurementReportInd"
    msg_h.add_to_list(member_h)

    assert ("class MAC_MeasurementReportInd(prophy.struct):\n"
            "    __metaclass__ = prophy.struct_generator\n"
            "    _descriptor = [('tmpName',TNumberOfItems), ('measurementGroupTypeList',prophy.array(EMeasurementGroupType,bound='tmpName'))]\n") == generate_python_msg(msg_h)

def test_of_message_with_one_dim_size():
    member_h = DataHolder.MemberHolder('iRi', 'TIRi')
    member_h.add_to_list("size", "MAX_NUM_OF_RI_PMI_INFORMATION")

    msg_h = DataHolder.MessageHolder()
    msg_h.name = "SCqiParams"
    msg_h.add_to_list(member_h)

    assert ("class SCqiParams(prophy.struct):\n"
            "    __metaclass__ = prophy.struct_generator\n"
            "    _descriptor = [('iRi',prophy.bytes(size=MAX_NUM_OF_RI_PMI_INFORMATION))]\n") == generate_python_msg(msg_h)
