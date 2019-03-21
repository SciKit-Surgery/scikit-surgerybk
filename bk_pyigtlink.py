from work_in_progress import BK
import logging
import numpy as np

from pyIGTLink import *

igtlink_server = PyIGTLink(localServer=True)

bk = BK()
bk.connect()

while True:
    if igtlink_server.is_connected():
        bk.get_frame()

        if bk.valid:
            img_x, img_y = bk.image_size
            image_message = ImageMessage(bk.img)
            igtlink_server.add_message_to_send_queue(image_message)
