import pytest

import socket

from threading import Thread

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

timeout = 10.  # Seconds
frames_per_second = 50


class TestingServer():
    """The class to define a test server"""

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((TCP_IP, TCP_PORT))

    def run(self):
        self.s.listen(1)
        conn, addr = self.s.accept()
        self.conn = conn
        print("Connection address: {:} \n".format(addr))
        self.done = False
        while not self.done:
            try:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                print("Received data in server: {:} \n".format(data))
                conn.send(data)  # echo
            except Exception:
                self.done = True

    def close(self):
        self.done = True
        self.conn.close()


@pytest.fixture
def socket_var():
    """A bunch of socket related variables"""
    pytest.TCP_IP = TCP_IP
    pytest.TCP_PORT = TCP_PORT
    pytest.BUFFER_SIZE = BUFFER_SIZE
    return pytest


@pytest.yield_fixture
def setup_server():
    """Setting up the server in a thread"""
    print("Setting up the server \n")
    test_server = TestingServer()
    thread = Thread(target=test_server.run)
    thread.start()
    yield thread
    test_server.close()


@pytest.fixture
def bk_medical_data_source_worker():
    """Instantiate the BKMedicalDataSourceWorker"""
    from sksurgerybk.interface.bk5000 import BKMedicalDataSourceWorker
    return BKMedicalDataSourceWorker(timeout=timeout,
                                     frames_per_second=frames_per_second)
