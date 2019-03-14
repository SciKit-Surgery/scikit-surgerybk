import pytest

import socket

from threading import Thread

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

timeout = 2.  # Seconds
frames_per_second = 50

@pytest.fixture
def bk_5000():
    """Instantiate the BK5000"""
    from sksurgerybk.interface.bk5000 import BK5000
    return BK5000(timeout=timeout, frames_per_second=frames_per_second)
