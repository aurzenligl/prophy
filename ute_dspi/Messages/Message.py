from templates.generated.MAC import *
import templates.header as Templates
import protophy
import binascii
import time

class MessageHandler(object):
    
    def __init__(self):
        pass
    
    def __open_message_with_header(self,Message,header = Templates.Header()):
        class Message(protophy.struct):
            __metaclass__ = protophy.struct_generator
            _descriptor = [('header',header),
                           ('payload',Message)]
        return Message()
    
    def send_message(p_connection,header,message,message_to_expect = None,p_noTimeoutException = False):
        message_with_header = __open_message_with_header(header,message)
        b_message = message_with_header.encode(">")
        p_connection.send_socket_data(b_message)
        if p_messageToExpect != None:
            p_messageToExpect = self.receive_message(p_connection, p_messageToExpect,p_noTimeoutException)
        return p_messageToExpect
    
    def receive_message(self, p_connection, p_messageToExpect, p_noTimeoutException = False):
        """
        TestMessageHandler: Tries to receive the message with id from the SysCom header

        All received messages are saved to the report's folder.
        If unexpected message is received then the message id is used to identify the message name. If message name
        matches to the expected message name then warning is printed that there is an inconsistency between
        message structure and message list file.
        Tassu header is automatically recognized and removed from the structure before it is logged.
        The socket buffer is emptied only by the received message length. If other message has been received to the buffer
        after the expected one then it is preserved in the socket buffer.
        Parameters:
         - p_connection: connection instance created by the BtsConnections class or by DspConnections class
         - p_messageToExpect: TestMessage class instance created, for example, with open_message method. If the expexted
           message (by the message id from the SysCom header) is not received within 5 seconds then timeout exception
           is called and test fails in this case
         - p_silentOperation (optional): messages are NOT LOGGED if True
         - p_wrongOrderIsFatal: p_messageToExpect can be a list of expected messages. If the messages will be received
           in different order than specified in the list error will be raised if p_wrongOrderIsFatal is true
        """
        v_entryTime = time.time()
        v_timeout = time.time() - v_entryTime
        
        
        v_mappedMessage = copy.deepcopy(p_messageToExpect)
        v_tassuMessage = self.open_message("Headers_Tassu")
        v_tassuHeaderSize = v_tassuMessage.get_message_length()
        v_receivedNumberOfFaults = 0
        if p_connection.is_virtual():
            print "*DEBUG* Virtual connection: need to set 'none' fields to zero"
            # Set zero values to fields with 'none' value to avoid exceptions
            v_fieldsList = v_mappedMessage.get_fields_list()
            for i_messageField in v_fieldsList:
                v_currentValue = v_mappedMessage.get_field_value(i_messageField)
                # First check if the field is enumeration and convert it to int if possible
                v_valueAsEnumeration = get_enumerated_value(self.knownEnumerations, v_currentValue)
                if v_valueAsEnumeration is not None:
                    v_mappedMessage.set_field_value(i_messageField, v_valueAsEnumeration)
                elif str(v_currentValue).upper() == "NONE":
                    v_mappedMessage.set_field_value(i_messageField, 0)
            # Save the message
            if self.__messageSave and not p_silentOperation:
                v_mappedMessage.set_time()
                v_mappedMessage.set_type("received")
                v_savedFileName = self.__save_message(v_mappedMessage)
                print "*HTML* Message <a href='" + v_savedFileName + "'>" + v_mappedMessage.get_message_name() + "</a> received from virtual socket connection"
            return v_mappedMessage

        v_expectedMessageIds = []
        if type(p_messageToExpect) is list:
            for v_subMessage in p_messageToExpect:
                v_expectedMessageIds.append(arg_to_int(v_subMessage.get_field_value("messageHeader.id")))
            v_expectedMessageCount = len(p_messageToExpect)
        else:
            v_expectedMessageIds.append(arg_to_int(p_messageToExpect.get_field_value("messageHeader.id")))
            v_expectedMessageCount = 1
        v_receivedMessageCount = 0
        while v_timeout < self.receiveTimeout:
#            if self.__connections.is_socket_data_available(p_connection) >= v_tassuHeaderSize:
            if p_connection.is_socket_data_available() >= v_tassuHeaderSize:
                # Touch the buffer by the tassu header length to detect if it is to be removed
#                v_receivedData = self.__connections.touch_socket_data(p_connection, v_tassuHeaderSize)
                v_receivedData = p_connection.touch_socket_data(v_tassuHeaderSize) 
                v_tassuMessage.map_data_to_message(v_receivedData, False, True)
                if v_tassuMessage.get_field_value("tassuHeader.protocol_id") == 0x7E and v_tassuMessage.get_field_value("tassuHeader.msg_type") == 0x04:
                    # Remove tassu header from the reception
                    if not p_silentOperation:
                        print "*DEBUG* Tassu header present, need to remove it"
#                    v_receivedData = self.__connections.receive_socket_data(p_connection, v_tassuHeaderSize)
                    v_receivedData = p_connection.receive_socket_data(v_tassuHeaderSize)
                v_headerMessage = self.open_message("Headers_SysCom")
                v_messageHeaderSize = v_headerMessage.get_message_length()
                # Touch the buffer by the SysCom header length to get received message id and length
#                v_receivedData = self.__connections.touch_socket_data(p_connection, v_messageHeaderSize)
                v_receivedData = p_connection.touch_socket_data(v_messageHeaderSize)
                if len(v_receivedData) < v_messageHeaderSize:
                    if not p_silentOperation:
                        print "*INFO* Message SysCom header was expected but not enough actual data in the socket"
                    raise BtsExceptions.MissingSocketData
                v_headerMessage.map_data_to_message(v_receivedData, False, True)
                v_receivedMessageId = v_headerMessage.get_field_value("messageHeader.id")
                v_receivedMessageSize = v_headerMessage.get_field_value("messageHeader.length")
                if not p_silentOperation:
                    print "*DEBUG* Message id from the header: " + hex(v_receivedMessageId)
                    print "*DEBUG* Message length from the header: " + str(v_receivedMessageSize)
                # Fetch complete message data
#                v_receivedData = self.__connections.receive_socket_data(p_connection, v_receivedMessageSize)
                v_receivedData = p_connection.receive_socket_data(v_receivedMessageSize)
                # If socket does not have enough data for the given length then exception is raised
                if len(v_receivedData) < v_receivedMessageSize:
                    if not p_silentOperation:
                        print "*INFO* Not enough data in the socket for given message length in the header:"
                        print "*INFO* messageHeader.id = %d, messageHeader.length = %d, available data length = %d" % \
                              (v_receivedMessageId, v_receivedMessageSize, len(v_receivedData))
                    raise BtsExceptions.MissingSocketData
                
                # Special handling of FaultTypeDataAck (id 0xf037) - LOM Fault Manager can send several ACKs for one FaultTypeDataReq
                if int(0xf037) == v_headerMessage.get_field_value("messageHeader.id"):
                    v_mappedMessage.map_data_to_message(v_receivedData, p_silentOperation = p_silentOperation, p_endianessSwapAllowed = True)
                    v_receivedNumberOfFaults = v_receivedNumberOfFaults + v_mappedMessage.get_field_value("numberOfFaultTypes") 
                    msgSave = globalVariables.get_env_variable("${MESSAGE_SAVE}")
                    if msgSave is not None:
                        self.__messageSave = msgSave
                    if self.__messageSave and not p_silentOperation:
                        v_mappedMessage.set_time()
                        v_mappedMessage.set_type("received")
                        v_savedFileName = self.__save_message(v_mappedMessage)
                        print "*HTML* Message <a href='" + v_savedFileName + "'>" + v_mappedMessage.get_message_name() + "</a> received from socket " + p_connection.get_connection_address() + ":" + str(p_connection.get_connection_port())
                    if v_receivedNumberOfFaults == v_mappedMessage.get_field_value("totalNumberOfFaultTypes"):
                        break
                # If received id does not match to expected ...
#                elif v_receivedMessageId != v_expectedMessageId:
                elif v_receivedMessageId not in v_expectedMessageIds:
                    v_correctMessageReceived = False
                    v_receivedMessageName = self.get_message_name_by_id(v_receivedMessageId)
                    if not p_silentOperation:
                        print "*HTML* <font color='#ff4500'>Warning: receved message id (%s) does not match to the one from the message structure (" % hex(v_receivedMessageId)
                        for msgId in v_expectedMessageIds:
                            print "*HTML* %s " % hex(msgId)
                        print "*HTML* ). Message list will be searched for the message with received id!</font>"
                    if v_receivedMessageName == "":
                        # If message is comletely unknown it is saved with 'unknown' fields only
                        v_unexpectedMessage = TestMessage("Unknown")
                        if not p_silentOperation:
                            print "*HTML* <font color='#ff4500'>Warning: no message found with given id!</font>"
                    else:
                        if not p_silentOperation:
                            print "*INFO* Message name '%s' matches the received message id %s" % (v_receivedMessageName, hex(v_receivedMessageId))
                        if v_receivedMessageName == p_messageToExpect.get_message_name():
                            if not p_silentOperation:
                                print "*HTML* <font color='#ff4500'>Warning: message name '%s' from the list matches the expected name, consider received message as correct</font>" % v_receivedMessageName
                                print "*HTML* <font color='#ff4500'>Warning: message id in the message list (%s" % hex(v_receivedMessageId)
                                for msgId in v_expectedMessageIds:
                                    print "*HTML* %s " % hex(msgId)
                                print "*HTML* ) DO NOT MATCH!</font>"
                            v_correctMessageReceived = True
                        # If message is recognized then it's structure is used to receive the data
                        v_unexpectedMessage = self.open_message(v_receivedMessageName)
                    v_unexpectedMessage.map_data_to_message(v_receivedData, p_silentOperation = p_silentOperation, p_endianessSwapAllowed = True)
                    msgSave = globalVariables.get_env_variable("${MESSAGE_SAVE}")
                    if msgSave is not None:
                        self.__messageSave = msgSave
                    if self.__messageSave and not p_silentOperation:
                        v_unexpectedMessage.set_time()
                        v_unexpectedMessage.set_type("received")
                        v_savedFileName = self.__save_message(v_unexpectedMessage)
                        if not p_silentOperation:
                            print "*HTML* Message <a href='" + v_savedFileName + "'>" + v_unexpectedMessage.get_message_name() + "</a> received from socket " + p_connection.get_connection_address() + ":" + str(p_connection.get_connection_port())
                    # If recognized message has target name then it is considered as correct
                    if v_correctMessageReceived:
                        break
                else:
                    v_receivedMessageCount = v_receivedMessageCount + 1
                    # Expected message is received - map the data and save it
                    if type(v_mappedMessage) is list:
                        for i in range(len(v_mappedMessage)):
                            if v_receivedMessageId == v_expectedMessageIds[i]:
                                v_mappedMessage[i].map_data_to_message(v_receivedData, p_silentOperation = p_silentOperation, p_endianessSwapAllowed = True)
                                if i != v_receivedMessageCount-1:
                                    if not p_silentOperation:
                                        print "*HTML* <font color='#ff4500'>Warning: message received in wrong order '%s' expected '%s' received, number %d</font>" % (hex(v_receivedMessageId), hex(v_expectedMessageIds[v_receivedMessageCount-1]), v_receivedMessageCount)
                                    if p_wrongOrderIsFatal:
                                        raise
                                    else:
                                        print "*WARN* message received in wrong order '%s' expected '%s' received, number %d" % (hex(v_receivedMessageId), hex(v_expectedMessageIds[v_receivedMessageCount-1]), v_receivedMessageCount)
                                msgSave = globalVariables.get_env_variable("${MESSAGE_SAVE}")
                                if msgSave is not None:
                                    self.__messageSave = msgSave
                                if self.__messageSave and not p_silentOperation:
                                    v_mappedMessage[i].set_time()
                                    v_mappedMessage[i].set_type("received")
                                    v_savedFileName = self.__save_message(v_mappedMessage[i])
                                    if not p_silentOperation:
                                        print "*HTML* Message <a href='" + v_savedFileName + "'>" + v_mappedMessage[i].get_message_name() + "</a> received from socket " + p_connection.get_connection_address() + ":" + str(p_connection.get_connection_port())
                    else:
                        v_mappedMessage.map_data_to_message(v_receivedData, p_silentOperation = p_silentOperation, p_endianessSwapAllowed = True)
                        msgSave = globalVariables.get_env_variable("${MESSAGE_SAVE}")
                        if msgSave is not None:
                            self.__messageSave = msgSave
                        if self.__messageSave and not p_silentOperation:
                            v_mappedMessage.set_time()
                            v_mappedMessage.set_type("received")
                            v_savedFileName = self.__save_message(v_mappedMessage)
                            if not p_silentOperation:
                                print "*HTML* Message <a href='" + v_savedFileName + "'>" + v_mappedMessage.get_message_name() + "</a> received from socket " + p_connection.get_connection_address() + ":" + str(p_connection.get_connection_port())
                    if v_receivedMessageCount == v_expectedMessageCount:
                        break
            v_timeout = time.time() - v_entryTime
        else:
            # Timeout happened
            if p_noTimeoutException:
                self.set_message_fields_to_zero(v_mappedMessage)
            else:
                raise BtsExceptions.ConnectionTimeout('No expected message received within given time (%d second(s))' % self.receiveTimeout)
        return v_mappedMessage