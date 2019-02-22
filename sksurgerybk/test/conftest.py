import pytest

import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

timeout = 10. # seconds
frames_per_second = 50

class TestingServer():
    def __init__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)
        conn, addr = s.accept()
        print 'Connection address:', addr
        while 1:
            data = conn.recv(BUFFER_SIZE)
            if not data: break
            print "received data:", data
            conn.send(data)  # echo
        conn.close()

@pytest.fixture
def socket_var():
    pytest.TCP_IP = TCP_IP
    pytest.TCP_PORT = TCP_PORT
    return pytest

@pytest.yield_fixture
def setup_server():
    return TestingServer()

@pytest.fixture
def bk_medical_data_source_worker():
    from sksurgerybk.interface.bk5000 import BKMedicalDataSourceWorker
    return BKMedicalDataSourceWorker(timeout=timeout,
                                     frames_per_second=frames_per_second)
