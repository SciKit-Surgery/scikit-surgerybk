
import socket
import logging

LOGGER = logging.getLogger(__name__)

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, world"


#TODO
class BKMedicalDataSourceActivator():

    def __init__(self):
        pass

    def load(self, context):
        pass


class BKMedicalDataSourceWorker():

    def __init__(self, timeout, frames_per_second):
        """ The DataSourceWorker constructor.

        Sets a number of class members.

        Parameters:
        timeout(positive float): the timeout in seconds.
        frames_per_second(positive integer): the expected fps from the \
                                             BK scanner
        """
        self.timeout = timeout
        self.frames_per_second = frames_per_second
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        pass

    def request_stop(self):
        pass

    def disconnect_from_host(self):
        """ Disconnects the client from the host.

        Check a receive, if not empty, disconnect
        """
        if not self.socket.recv(BUFFER_SIZE):
            self.socket.close()
        pass

    def stop_streaming(self):
        pass

    def start_streaming(self):
        pass

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
        pass

    def parse_win_size_message(self, message):
        pass

    def generate_command_message(self, message):
        pass

    def send_command_message(self, message):
        """Send a message through the socket.

        Implements a couple of checks to verify the
        message has been sent correctly.

        Parameters:
        message(string): the message to be sent
        """
        bytes_sent = self.socket.send(message)
        # Check the sent went OK.
        if (bytes_sent != len(message)):
            print("Failed to send message: {:} due to size mismatch: {:} \
            different from {:} bytes sent.".format(message, len(message),
                                                   bytes_sent))
        pass

    def receive_response_message(self, expected_size):
        self.data = self.socket.recv(expected_size)
        pass

    def receive_image(self, image):
        pass

    def find_first_a_not_preceded_by_b(self, start_position, buf, a, b):
        pass


if __name__ == '__main__':
    print("instantiate the class")
    bkworker = BKMedicalDataSourceWorker(10, 50)
    bkworker.connect_to_host(TCP_IP, TCP_PORT)
    bkworker.send_command_message(MESSAGE)
    bkworker.receive_response_message(BUFFER_SIZE)
    bkworker.disconnect_from_host()
    print("received data in client: {:}".format(bkworker.data))
