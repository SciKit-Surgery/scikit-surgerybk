"""This module sets the connection to the BK scanner"""

import socket
import logging

LOGGER = logging.getLogger(__name__)

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, world"


class BKMedicalDataSourceActivator():
    """A class"""

    def __init__(self):
        """The constructor"""

    def load(self, context):
        """Load method"""


class BKMedicalDataSourceWorker():
    """This class sets the TCP connection with the BK scanner"""

    def __init__(self, timeout, frames_per_second):
        """ The DataSourceWorker constructor.

        Sets a number of class members.

        Parameters:
        timeout(positive float): the timeout in seconds.
        frames_per_second(positive integer): the expected fps from the \
                                             BK scanner
        """
        self.data = None
        self.timeout = timeout
        self.frames_per_second = frames_per_second
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.timeout)

    def request_stop(self):
        """Method docstring"""

    def disconnect_from_host(self):
        """ Disconnects the client from the host.

        Check a receive, if not empty, disconnect
        """
        if not self.socket.recv(BUFFER_SIZE):
            self.socket.close()

    def stop_streaming(self):
        """Method docstring"""

    def start_streaming(self):
        """Method docstring"""

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

    def parse_win_size_message(self, message):
        """Method docstring"""

    def generate_command_message(self, message):
        """Method docstring"""

    def send_command_message(self, message):
        """Send a message through the socket.

        Implements a couple of checks to verify the
        message has been sent correctly.

        Parameters:
        message(bytes string in Python3): the message to be sent
        """
        bytes_sent = self.socket.send(message)
        # Check the sent went OK.
        if bytes_sent != len(message):
            print("Failed to send message: {:} due to size mismatch: {:} \
            different from {:} bytes sent.".format(message,
                                                   len(message),
                                                   bytes_sent))

    def receive_response_message(self, expected_size):
        """Receive a message"""
        self.data = self.socket.recv(expected_size)

    def receive_image(self, image):
        """Method docstring"""

    def find_first_a_not_preceded_by_b(self, start_position, buf,
                                       char_a, char_b):
        """Method docstring"""


# if __name__ == '__main__':
#     print("instantiate the class")
#     bkworker = BKMedicalDataSourceWorker(10, 50)
#     bkworker.connect_to_host(TCP_IP, TCP_PORT)
#     bkworker.send_command_message(MESSAGE)
#     bkworker.receive_response_message(BUFFER_SIZE)
#     bkworker.disconnect_from_host()
#     print("received data in client: {:}".format(bkworker.data))
