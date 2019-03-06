"""This module sets the connection to the BK scanner"""

import socket
import logging

LOGGER = logging.getLogger(__name__)

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, world"

class BK5000():
    """This class sets the TCP connection with the BK scanner"""

    def __init__(self, timeout, frames_per_second):
        """ The DataSourceWorker constructor.

        Sets a number of class members.

        Parameters:
        timeout(positive float): the connection timeout in seconds.
        frames_per_second(positive integer): the expected fps from the \
                                             BK scanner
        """
        self.data = None
        self.timeout = timeout
        self.frames_per_second = frames_per_second
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        self.request_stop_streaming = False
        self.is_streaming = False
        self.image_size = [0, 0]

    def request_stop(self):
        """Set the appropriate class member"""
        self.request_stop_streaming = True

    def disconnect_from_host(self):
        """ Disconnects the client from the host.

        Check a receive, if not empty, disconnect
        """
        if not self.socket.recv(BUFFER_SIZE):
            self.socket.close()

    def stop_streaming(self):
        """ Send a message to stop the streaming """
        stop_message = 'QUERY:GRAB_FRAME \"OFF\",{:};'.\
        format(self.frames_per_second)
        sent_ok = self.send_command_message(stop_message)
        if not sent_ok:
            print("Failed to send stop message: {:}.".format(stop_message))
        recv_ok = self.receive_response_message()
        if not recv_ok:
            print("Failed to receive acknowledgment for stop message: {:}.".\
            format(stop_message))
        self.is_streaming = False
        self.request_stop_streaming = False

    def start_streaming(self):
        """ Send a message to start the streaming """
        start_message = 'QUERY:GRAB_FRAME \"ON\",{:};'.\
        format(self.frames_per_second)
        sent_ok = self.send_command_message(start_message)
        if not sent_ok:
            print("Failed to send stop message: {:}.".format(start_message))
        recv_ok = self.receive_response_message()
        if not recv_ok:
            print("Failed to receive acknowledgment for start message: {:}.".\
            format(start_message))
        self.is_streaming = True

    def connect_to_host(self, address, port):
        """ Connects the client to the host/serverself.

        Implements a try/except block to catch potential errors.

        Parameters:
        address(string): the IP address
        port(integer): the port
        """
        try:
            self.socket.connect((address, port))
        except socket.error as error_msg:
            print("An error: {:} has occured while trying to connect to: {:} \
            with port: {:}".format(error_msg, address, port))
            self.socket.close()

    def query_win_size(self):
        """ Query the BK5000 for the window/image size """
        query_win_size_message = "QUERY:US_WIN_SIZE;"
        is_ok = self.send_command_message(query_win_size_message)
        if is_ok:
            response = self.receive_response_message(expected_size=25)
            if response:
                self.parse_win_size_message(self.data.decode())
            else:
                print("An error occurred getting the WIN_SIZE response")
        else:
            print("An error occured when querying window size")
        return is_ok

    def parse_win_size_message(self, message):
        """Extrack the size of the US window from the response message

        Message has format "DATA: US_WIN_SIZE 124,455;"

        Parameters:
        message(string): the received message """

        # Split on spaces, get the final token, strip the ; and split into
        # the two integers.
        print("parse {}".format(message))
        dim_part_of_message = message.split()[-1].strip(';').split(',')
        self.image_size = [int(s) for s in dim_part_of_message]

    def generate_command_message(self, message):
        #pylint:disable=no-self-use
        """ Append 0x01 and 0x04 to start/end of message before sending

        Parameters:
        message(string): the message to be sent"""
        char_start = bytearray.fromhex("01").decode()
        char_end = bytearray.fromhex("04").decode()

        message_to_send = char_start + message + char_end

        message_length = len(message_to_send)
        logging.debug("Message to send: %s Size: %s", \
             message_to_send, message_length)

        return message_to_send

    def send_command_message(self, message):
        """Send a message through the socket.

        Implements a couple of checks to verify the
        message has been sent correctly.

        Parameters:
        message(string): the message to be sent
        """

        message_to_send = self.generate_command_message(message)
        try:
            bytes_sent = self.socket.send(message_to_send.encode())
            is_ok = True
            # Check the sent went OK.
            if bytes_sent != len(message_to_send):
                print("Failed to send message: {:} due to size mismatch: {:} \
                different from {:} bytes sent.".format(message_to_send,
                                                       len(message_to_send),
                                                       bytes_sent))
                is_ok = False
            return is_ok
        except socket.error as error_msg:
            print("An error: {:} has occured while trying to send \
            the message: {:}.".format(error_msg, message))


    def receive_response_message(self, expected_size=BUFFER_SIZE):
        """Receive a message

        Stores it under the data class member

        Parameters:
        expected_size(int): the receive message size in bytes
        """
        actual_size = expected_size + 2 # Due to start/end terminator
        data_with_terminators = self.socket.recv(actual_size)
        self.data = data_with_terminators[1:-1]
        is_ok = True
        if len(self.data) > expected_size:
            print("Failed to receive message: {:} due to size mismatch: {:} \
            different from {:} bytes received.".format(self.data,
                                                       len(self.data),
                                                       expected_size))
            is_ok = False
        return is_ok

    def receive_image(self, image):
        """Method docstring"""

    def find_first_a_not_preceded_by_b(self, start_position, buf,
                                       char_a, char_b):
        """Method docstring"""
