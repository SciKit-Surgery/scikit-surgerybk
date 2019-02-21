
import socket
import logging

LOGGER = logging.getLogger(__name__)

#TODO
class BKMedicalDataSoureActivator():

    def __init__(self):
        pass
    def load(self, context):
        pass


class BKMedicalDataSourceWorker():

    def __init__(timeout, frames_per_second):
        pass
        
    def request_stop(self):
        pass
    def disconnect_from_host(self):
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