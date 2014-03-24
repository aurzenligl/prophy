from prophyc import Parser
import data_holder
from prophyc import Serializers
from reader import XmlReader

def test_create_of_parser():
    Parser.get_parser()

def test_of_opening_files():
    reader = XmlReader(".")
    reader.read_files()

def test_of_message_simple():
    msg_h = data_holder.MessageHolder()
    msg_h.name = "MAC_L2CallConfigResp"
    msg_h.add_to_list(data_holder.MemberHolder('messageResult', 'SMessageResult'))
    msg_h.add_to_list(data_holder.MemberHolder('lnCelId', 'TCellId'))
    msg_h.add_to_list(data_holder.MemberHolder('crnti', 'TCrnti'))

    ps = Serializers.get_serializer()
    output = ps._serialize_msgs([msg_h])

    assert output == ("class MAC_L2CallConfigResp(prophy.struct):\n"
                      "    __metaclass__ = prophy.struct_generator\n"
                      "    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti)]\n")

def test_of_message_with_four_dim_without_field_type():
    member_h = data_holder.MemberHolder('sRbList', 'SSRbList')
    member_h.add_to_list("isVariableSize", "true")
    member_h.add_to_list("minSize", "1")
    member_h.add_to_list("size", "MAX_NUM_SRB_PER_USER")
    member_h.add_to_list("variableSizeFieldName", "numSRbs")

    msg_h = data_holder.MessageHolder()
    msg_h.name = "MAC_L2CallConfigResp"
    msg_h.add_to_list(member_h)

    ps = Serializers.get_serializer()
    output = ps._serialize_msgs([msg_h])

    assert output == ("class MAC_L2CallConfigResp(prophy.struct):\n"
                      "    __metaclass__ = prophy.struct_generator\n"
                      "    _descriptor = [('numSRbs',TNumberOfItems), ('sRbList',prophy.array(SSRbList,bound='numSRbs'))]\n")

def test_of_message_with_five_dim():

    msg_h = data_holder.MessageHolder()
    msg_h.name = "MAC_CcchDataReceiveInd"
    member_h = data_holder.MemberHolder('msg3Info', 'SMsg3Info')
    member_h.add_to_list("isVariableSize", "true")
    member_h.add_to_list("minSize", "1")
    member_h.add_to_list("size", "MAX_MSG3_PER_TTI")
    member_h.add_to_list("variableSizeFieldName", "maxNumOfUes")
    member_h.add_to_list("variableSizeFieldType", "u32")
    msg_h.add_to_list(member_h)

    ps = Serializers.get_serializer()
    o = ps._serialize_msgs([msg_h])
    print o
    out = "class MAC_CcchDataReceiveInd(prophy.struct):\n    __metaclass__ = prophy.struct_generator\n    _descriptor = [('maxNumOfUes',u32), ('msg3Info',prophy.array(SMsg3Info,bound='maxNumOfUes'))]\n"
    assert out == o

def test_of_message_with_four_dim_without_min_size():

    msg_h = data_holder.MessageHolder()
    msg_h.name = "SSiList"
    member_h = data_holder.MemberHolder('data', 'u8')
    member_h.add_to_list("isVariableSize", "true")
    member_h.add_to_list("size", "MAX_SI_DATA")
    member_h.add_to_list("variableSizeFieldName", "size")
    member_h.add_to_list("variableSizeFieldType", "TL3MsgSize")
    msg_h.add_to_list(member_h)

    ps = Serializers.get_serializer()
    o = ps._serialize_msgs([msg_h])
    print o
    out = "class SSiList(prophy.struct):\n    __metaclass__ = prophy.struct_generator\n    _descriptor = [('size',TL3MsgSize), ('data',prophy.array(u8,bound='size'))]\n"


def test_of_message_with_three_fields_without_variable_name_and_variable_type():

    msg_h = data_holder.MessageHolder()
    msg_h.name = "MAC_CellSetupReq"
    member_h = data_holder.MemberHolder('rlcDlLcpInfo', 'SRlcLcpInfo')
    member_h.add_to_list("isVariableSize", "true")
    member_h.add_to_list("size", "MAX_SI_DATA")
    member_h.add_to_list("minSize", "1")
    msg_h.add_to_list(member_h)

    ps = Serializers.get_serializer()
    o = ps._serialize_msgs([msg_h])
    print o
    out = "class MAC_CellSetupReq(prophy.struct):\n    __metaclass__ = prophy.struct_generator\n    _descriptor = [('tmpName',TNumberOfItems), ('rlcDlLcpInfo',prophy.array(SRlcLcpInfo,bound='tmpName'))]\n"

def test_of_message_with_two_fields_size_and_isVariable():

    msg_h = data_holder.MessageHolder()
    msg_h.name = "MAC_MeasurementReportInd"
    member_h = data_holder.MemberHolder('measurementGroupTypeList', 'EMeasurementGroupType')
    member_h.add_to_list("isVariableSize", "true")
    member_h.add_to_list("size", "MAX_MEAS_GROUP_TYPE_ID_MAC")

    msg_h.add_to_list(member_h)

    ps = Serializers.get_serializer()
    o = ps._serialize_msgs([msg_h])
    print o
    out = "class MAC_CellSetupReq(prophy.struct):\n    __metaclass__ = prophy.struct_generator\n    _descriptor = [('tmpName',TNumberOfItems), ('measurementGroupTypeList',prophy.array(EMeasurementGroupType,bound='tmpName'))]\n"

def test_of_message_with_one_dim_size():

    msg_h = data_holder.MessageHolder()
    msg_h.name = "SCqiParams"
    member_h = data_holder.MemberHolder('iRi', 'TIRi')
    member_h.add_to_list("size", "MAX_NUM_OF_RI_PMI_INFORMATION")
    msg_h.add_to_list(member_h)

    ps = Serializers.get_serializer()
    o = ps._serialize_msgs([msg_h])
    print o
    out = "class SCqiParams(prophy.struct):\n    __metaclass__ = prophy.struct_generator\n    _descriptor = [('tmpName',TNumberOfItems), ('iRi',prophy.array(TIRi,bound='tmpName'))]\n"
