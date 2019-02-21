
import socket
import logging

LOGGER = logging.getLogger(__name__)

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, world"


#TODO
class BKMedicalDataSoureActivator():

    def __init__(self):
        pass
    def load(self, context):
        pass


class BKMedicalDataSourceWorker():

    def __init__(self, timeout, frames_per_second):
        self.timeout = timeout
        self.frames_per_second = frames_per_second
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((TCP_IP, TCP_PORT))
        self.socket.send(MESSAGE)
        data = self.socket.recv(BUFFER_SIZE)
        self.socket.close()
        print "received data: ", data
        pass

    def request_stop(self):
        pass

    def disconnect_from_host(self):
        if(self.socket.recv(BUFFER_SIZE)): # If the receive is not empty, disconnect
            self.socket.close()
        pass

    def stop_streaming(self):
        pass

    def start_streaming(self):
        pass

    def connect_to_host(self, address, port):
        pass

    def parse_win_size_message(self, message):
        pass

    def generate_command_message(self, message):
        pass

    def send_command_message(self, message):
        pass


    def receive_response_message(self, expected_size):
        pass


    def receive_image(self, image):
        pass

    def find_first_a_not_preceded_by_b(self, start_position, buf, a, b):
        pass

if __name__ == '__main__':
    print "instantiate the class"
    bkworker = BKMedicalDataSourceWorker(10, 50)
