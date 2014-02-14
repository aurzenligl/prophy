import messages
import data_holder
import writer
from reader import XmlReader
import xml.dom

def test_create_of_parser():
    parser = messages.Parser()


def test_of_opening_files():
    reader =XmlReader(".")
    reader.read_files()

def test_of_message_simple():

    msg_h = data_holder.MessageHolder()
    msg_h.name = "MAC_L2CallConfigResp"
    msg_h.add_to_list(data_holder.MemberHolder('messageResult','SMessageResult'))

    a = writer.PythonSerializer()._serialize_msgs([msg_h])

    out = "class MAC_L2CallConfigResp(aprot.struct):\n    __metaclass__ = aprot.struct_generator\n    _descriptor = [('messageResult',SMessageResult)]\n"
    assert out == a

def test_of_message_complex():

    msg_h = data_holder.MessageHolder()
    msg_h.name = "MAC_L2CallConfigResp"
    msg_h.add_to_list(data_holder.MemberHolder('messageResult','SMessageResult'))
    msg_h.add_to_list(data_holder.MemberHolder('lnCelId','TCellId'))
    msg_h.add_to_list(data_holder.MemberHolder('crnti','TCrnti'))
    msg_h.add_to_list(data_holder.MemberHolder('ueId','TUeId'))
    msg_h.add_to_list(data_holder.MemberHolder('ueGroup','TUeGroup'))
    msg_h.add_to_list(data_holder.MemberHolder('transactionId','TTransactionID'))
    msg_h.add_to_list(data_holder.MemberHolder('spsCrnti','TCrnti'))
    msg_h.add_to_list(data_holder.MemberHolder('macUserAddress','TAaSysComSicad'))
    msg_h.add_to_list(data_holder.MemberHolder('raPreambleIndex','TRaPreambleIndex'))
    msg_h.add_to_list(data_holder.MemberHolder('prachMaskIndex','TPrachMaskIndex'))
    msg_h.add_to_list(data_holder.MemberHolder('sRbList','SSRbList'))
    msg_h.add_to_list(data_holder.MemberHolder('dRbList','SDRbList'))

    a = writer.PythonSerializer()._serialize_msgs([msg_h])
    out = "class MAC_L2CallConfigResp(aprot.struct):\n    __metaclass__ = aprot.struct_generator\n    _descriptor = [('messageResult',SMessageResult), ('lnCelId',TCellId), ('crnti',TCrnti), ('ueId',TUeId), ('ueGroup',TUeGroup), ('transactionId',TTransactionID), ('spsCrnti',TCrnti), ('macUserAddress',TAaSysComSicad), ('raPreambleIndex',TRaPreambleIndex), ('prachMaskIndex',TPrachMaskIndex), ('sRbList',SSRbList), ('dRbList',SDRbList)]\n"
    assert out == a

def test_of_message_with_four_dim_without_field_type():

    msg_h = data_holder.MessageHolder()
    msg_h.name = "MAC_L2CallConfigResp"
    member_h = data_holder.MemberHolder('sRbList','SSRbList')
    member_h.add_to_list("isVariableSize", "true")
    member_h.add_to_list("minSize", "1")
    member_h.add_to_list("size", "MAX_NUM_SRB_PER_USER")
    member_h.add_to_list("variableSizeFieldName", "numSRbs")
    msg_h.add_to_list(member_h)

    a = writer.PythonSerializer()._serialize_msgs([msg_h])
    print a
    out = "class MAC_L2CallConfigResp(aprot.struct):\n    __metaclass__ = aprot.struct_generator\n    _descriptor = [('numSRbs',TNumberOfItems), ('sRbList',aprot.array(SSRbList,bound='numSRbs'))]\n"
    assert out == a

def test_of_message_with_five_dim():

    msg_h = data_holder.MessageHolder()
    msg_h.name = "MAC_CcchDataReceiveInd"
    member_h = data_holder.MemberHolder('msg3Info','SMsg3Info')
    member_h.add_to_list("isVariableSize", "true")
    member_h.add_to_list("minSize", "1")
    member_h.add_to_list("size", "MAX_MSG3_PER_TTI")
    member_h.add_to_list("variableSizeFieldName", "maxNumOfUes")
    member_h.add_to_list("variableSizeFieldType", "u32")
    msg_h.add_to_list(member_h)

    a = writer.PythonSerializer()._serialize_msgs([msg_h])
    print a
    out = "class MAC_CcchDataReceiveInd(aprot.struct):\n    __metaclass__ = aprot.struct_generator\n    _descriptor = [('maxNumOfUes',u32), ('msg3Info',aprot.array(SMsg3Info,bound='maxNumOfUes'))]\n"
    assert out == a

def test_of_message_with_four_dim_without_min_size():

    msg_h = data_holder.MessageHolder()
    msg_h.name = "SSiList"
    member_h = data_holder.MemberHolder('data','u8')
    member_h.add_to_list("isVariableSize", "true")
    member_h.add_to_list("size", "MAX_SI_DATA")
    member_h.add_to_list("variableSizeFieldName", "size")
    member_h.add_to_list("variableSizeFieldType", "TL3MsgSize")
    msg_h.add_to_list(member_h)

    a = writer.PythonSerializer()._serialize_msgs([msg_h])
    print a
    out = "class SSiList(aprot.struct):\n    __metaclass__ = aprot.struct_generator\n    _descriptor = [('size',TL3MsgSize), ('data',aprot.array(u8,bound='size'))]\n"
    assert out == a

def test_of_message_with_three_fields_without_variable_name_and_variable_type():

    msg_h = data_holder.MessageHolder()
    msg_h.name = "MAC_CellSetupReq"
    member_h = data_holder.MemberHolder('rlcDlLcpInfo','SRlcLcpInfo')
    member_h.add_to_list("isVariableSize", "true")
    member_h.add_to_list("size", "MAX_SI_DATA")
    member_h.add_to_list("minSize", "1")
    msg_h.add_to_list(member_h)

    a = writer.PythonSerializer()._serialize_msgs([msg_h])
    print a
    out = "class MAC_CellSetupReq(aprot.struct):\n    __metaclass__ = aprot.struct_generator\n    _descriptor = [('tmpName',TNumberOfItems), ('rlcDlLcpInfo',aprot.array(SRlcLcpInfo,bound='tmpName'))]\n"

def test_of_message_with_two_fields_size_and_isVariable():

    msg_h = data_holder.MessageHolder()
    msg_h.name = "MAC_MeasurementReportInd"
    member_h = data_holder.MemberHolder('measurementGroupTypeList','EMeasurementGroupType')
    member_h.add_to_list("isVariableSize", "true")
    member_h.add_to_list("size", "MAX_MEAS_GROUP_TYPE_ID_MAC")

    msg_h.add_to_list(member_h)

    a = writer.PythonSerializer()._serialize_msgs([msg_h])
    print a
    out = "class MAC_CellSetupReq(aprot.struct):\n    __metaclass__ = aprot.struct_generator\n    _descriptor = [('tmpName',TNumberOfItems), ('measurementGroupTypeList',aprot.array(EMeasurementGroupType,bound='tmpName'))]\n"