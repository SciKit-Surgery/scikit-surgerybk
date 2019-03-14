import socket
import logging
import time
import numpy as np
import cv2

logging.basicConfig(level=logging.INFO)

def find_first_a_not_preceded_by_b(start_pos, buffer, a, b):
    #TODO: Start_pos

    np_buffer = np.frombuffer(buffer[start_pos:], dtype=np.uint8)

    if np_buffer[0] == a:
        return 0
    
    else:
        a_idx = np.where(np_buffer == a)[0]
        not_b_idx = np.where(np_buffer[a_idx - 1] != b)[0]

        if len(not_b_idx):
            first_a_not_preceded_by_b_idx = a_idx[not_b_idx]
            return start_pos + first_a_not_preceded_by_b_idx[0]

        else:
            return -1

def clear_bytes_in_buffer(buffer, start, end):
    logging.debug("Start: {} End: {}".format(start,end))

    if end >= len(buffer):
        end = len(buffer) - 1

    del buffer[start:end]
    # for i in range(end, start, -1):
    #     buffer.pop(i)

def decode_image(buffer, start, end):

    x = 892
    y = 728

    np_buffer = np.frombuffer(buffer[start:end+1], dtype=np.uint8)
    # result = np.zeros(892 * 728, dtype=np.uint8)

    uc1 = 1
    uc4 = 4
    uc27 = 27
    ucN1 = uc1 ^ 0xFF
    ucN4 = uc4 ^ 0xFF
    ucN27 = uc27 ^ 0xFF

    # i = start
    # j = 0

    uc27_idx = np.where(np_buffer == uc27)[0]

    ucN1_idx = np.where(np_buffer[uc27_idx + 1] == ucN1)[0]
    ucN4_idx = np.where(np_buffer[uc27_idx + 1] == ucN4)[0]
    ucN27_idx = np.where(np_buffer[uc27_idx + 1] == ucN27)[0]

    a = uc27_idx[ucN1_idx]
    b = uc27_idx[ucN4_idx]
    c = uc27_idx[ucN27_idx]

    x = np.union1d(a, b)
    idx_to_del = np.union1d(x, c)

    np_buffer[idx_to_del + 1] ^= 0xFF

    result = np.delete(np_buffer, idx_to_del)

    # while (i != end):
    #     uc = buffer[i]
    #     ucp1 = buffer[i+1]
    #     if (    (uc == uc27 and ucp1 == ucN1) or 
    #             (uc == uc27 and ucp1 == ucN4) or
    #             (uc == uc27 and ucp1 == ucN27) ):
    #         i += 1
    #         result[j] = buffer[i] ^ 0xFF

    #     else:
    #         result[j] = buffer[i]
        
    #     i += 1
    #     j += 1

    return result

def receive_image(buffer):

    # buffer is a bytearray object (utf-8 encoding)


    valid = False
    preceding_char = find_first_a_not_preceded_by_b(0, buffer, 0x01, 0x27)

    if preceding_char < 0:
        logging.warning("Failed to find start of message character. This suggetss there is junk in the buffer")
        buffer.clear()
        return valid, None

    else:
        terminating_char = find_first_a_not_preceded_by_b(preceding_char, buffer, 0x04, 0x27)

        if terminating_char <= preceding_char:
            logging.debug("Failed to find end of message character. This is OK if message is still incoming.")
            return valid, None

        else:
            img_msg = "DATA:GRAB_FRAME".encode('utf-8') # utf-8 to be compatible with buffer
            img_msg_index = buffer.find(img_msg, preceding_char)

            if not (img_msg_index != -1 and # i.e. it was found 
                img_msg_index > preceding_char and
                img_msg_index < terminating_char):

                    logging.warning("Received a non-image message, which I wasn't expecting.")
                    
                    clear_bytes_in_buffer(buffer, 0, terminating_char + 1)
                    return valid, None

            else:

                    logging.debug("Starting decode step.")
                    hash_char = buffer.find('#'.encode('utf-8'), preceding_char)
                    size_of_data_char = hash_char + 1

                    start_image_char = size_of_data_char + \
                                        1 + 4 + \
                                        buffer[size_of_data_char] - ord('0') # Dealing with ASCII

                    end_image_char = terminating_char - 2
                    data_size = terminating_char - preceding_char + 1
                    image_size = end_image_char - start_image_char + 1

                    #result = np.frombuffer(buffer, dtype=np.uint8)[0:892*728]
                    result = decode_image(buffer, start_image_char, end_image_char)

                    logging.debug("Image received")
                    clear_bytes_in_buffer(buffer, 0, terminating_char + 1)

                    valid = True
                    return valid, result



logging.debug('Starting')

s = socket.socket()

host = '128.16.0.3'
port = 7915

# Connect to remote
status = s.connect_ex((host, port))
logging.debug("Status: {}".format(status))

message = "QUERY:US_WIN_SIZE;"

char_start = bytearray.fromhex("01").decode()
char_end  = bytearray.fromhex("04").decode()
message_to_send = char_start + message + char_end
message_length = len(message_to_send)
logging.debug("Message to send: {}  Size: {}".format(message_to_send, message_length))

s.send(message_to_send.encode())

ret = s.recv(27)
logging.debug(ret)

stream_message = "QUERY:GRAB_FRAME \"ON\",30;"
message_to_send = char_start + stream_message + char_end
logging.debug("Message to send: {}".format(message_to_send))

s.send(message_to_send.encode())

ret = s.recv(6)
logging.debug(ret)

minimum_size = 892 * 728 + 22
packet_size = 4096

buffer = bytearray()

while True:

    while len(buffer) < minimum_size:
        buffer.extend(s.recv(minimum_size))


    valid, result = receive_image(buffer)
    if valid:
        result=result[:728*892].reshape(728, 892).T
        cv2.imshow('a', result)
        cv2.waitKey(1)


    else:
        buffer.extend(s.recv(packet_size))



   

 
    