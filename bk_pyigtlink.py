from sksurgerybk.interface.bk5000 import BK5000
import logging
import numpy as np

from pyIGTLink import *

igtlink_server = PyIGTLink(localServer=True)

TCP_IP = '128.16.0.3' # Default IP of BK5000
TCP_PORT = 7915       # Default port of BK5000
TIMEOUT = 5
FPS = 25

bk = BK5000(TIMEOUT, FPS)
bk.connect_to_host(TCP_IP, TCP_PORT)
bk.query_win_size()
bk.start_streaming()

while True:
    if igtlink_server.is_connected():
        bk.get_frame()

        image_message = ImageMessage(bk.img)
        igtlink_server.add_message_to_send_queue(image_message)
