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

def test_of_message_with_dim():

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
    out = "class MAC_L2CallConfigResp(aprot.struct):\n    __metaclass__ = aprot.struct_generator\n    _descriptor = [('numSRbs',TNumberOfItems), ('sRbList', aprot.array(SSRbList,bound='numSRbs')]\n"
    assert out == a