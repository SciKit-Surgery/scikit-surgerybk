import socket
import logging
import time
import numpy as np

logging.basicConfig(level=logging.INFO)

class BK:

    def __init__(self):
        logging.debug('Starting')

        self.s = socket.socket()

        host = '128.16.0.3'
        port = 7915

        # Connect to remote
        status = self.s.connect_ex((host, port))
        logging.debug("Status: {}".format(status))

        self.image_size = (892, 728)

    def connect(self):

        message = "QUERY:US_WIN_SIZE;"

        char_start = bytearray.fromhex("01").decode()
        char_end  = bytearray.fromhex("04").decode()
        message_to_send = char_start + message + char_end
        message_length = len(message_to_send)
        logging.debug("Message to send: {}  Size: {}".format(message_to_send, message_length))

        self.s.send(message_to_send.encode())

        ret = self.s.recv(27)
        logging.debug(ret)

        stream_message = "QUERY:GRAB_FRAME \"ON\",40;"
        message_to_send = char_start + stream_message + char_end
        logging.debug("Message to send: {}".format(message_to_send))

        self.s.send(message_to_send.encode())

        ret = self.s.recv(6)
        logging.debug(ret)

        self.minimum_size = 892 * 728 + 22
        self.packet_size = 4096

        self.buffer = bytearray()

    def find_first_a_not_preceded_by_b(self, start_pos, a, b):
        """
        Find the first instance of 'a' in an array that isn't preceded by 'b'
        
        :param start_pos: Index in array to begin search at
        :type start_pos: integer
        :param a: Value to find
        :type a: integer
        :param b: Value not to precede a
        :type b: integer
        :return: Index of first instance of a not preceded by b, -1 if none found
        :rtype: integer
        """

        found = -1
        
        trimmed_buffer = self.np_buffer[start_pos:]
        if trimmed_buffer[0] == a:
            found = 0
        
        else:
            a_idx = np.where(trimmed_buffer == a)[0]
            not_b_idx = np.where(trimmed_buffer[a_idx - 1] != b)[0]

            if len(not_b_idx):
                first_a_not_preceded_by_b_idx = a_idx[not_b_idx]
                found = start_pos + first_a_not_preceded_by_b_idx[0]

        return found


    def clear_bytes_in_buffer(self, start, end):
        """
        Clear a set of bytes in bytearray buffer
        
        :param start: Start index
        :type start: integer
        :param end: End integer
        :type end: integer
        """

        logging.debug("Start: {} End: {}".format(start,end))

        # Can't delete past the end of the buffer
        if end >= len(self.buffer):
            end = len(self.buffer)

        del self.buffer[start:end]

    def decode_image(self):
        """
        Process the stream of data received from the BK5000 and convert
        it into a numpy array which represents the ultrasound image.
        
        Control characters are removed, and any values that come immediately
        after a control character are bit flipped.

        """

        uc1 = 1
        uc4 = 4
        uc27 = 27
        ucN1 = uc1 ^ 0xFF
        ucN4 = uc4 ^ 0xFF
        ucN27 = uc27 ^ 0xFF

        uc27_idx = np.where(self.np_buffer == uc27)[0]

        ucN1_idx = np.where(self.np_buffer[uc27_idx + 1] == ucN1)[0]
        ucN4_idx = np.where(self.np_buffer[uc27_idx + 1] == ucN4)[0]
        ucN27_idx = np.where(self.np_buffer[uc27_idx + 1] == ucN27)[0]

        a = uc27_idx[ucN1_idx]
        b = uc27_idx[ucN4_idx]
        c = uc27_idx[ucN27_idx]

        x = np.union1d(a, b)
        idx_to_del = np.union1d(x, c)

        self.np_buffer[idx_to_del + 1] ^= 0xFF

        result = np.delete(self.np_buffer, idx_to_del)

        return result

    def receive_image(self):
        """
        Scan the incoming data stream to find the start and end of the image data.
        """
        
        # self.buffer contains the received TCP data
        # We also want a numpy representation of this.
        # Some operations are simpler to do on a bytearray than np array
        self.np_buffer = np.frombuffer(self.buffer, dtype=np.uint8)

        valid = False
        preceding_char_idx = self.find_first_a_not_preceded_by_b(0, 0x01, 0x27)

        if preceding_char_idx < 0:
            logging.warning("Failed to find start of message character. This suggetss there is junk in the buffer")
            buffer.clear()
            return valid, None

        else:
            terminating_char_idx = self.find_first_a_not_preceded_by_b(preceding_char_idx, 0x04, 0x27)

            if terminating_char_idx <= preceding_char_idx:
                logging.debug("Failed to find end of message character. This is OK if message is still incoming.")
                return valid, None

            else:
                # There isn't a standard way to do this operation on a numpy array e.g. find a sequence of
                # values, so we use the bytearray instead.

                img_msg = "DATA:GRAB_FRAME".encode('utf-8') # utf-8 to be compatible with buffer
                img_msg_index = self.buffer.find(img_msg, preceding_char_idx)

                if not (img_msg_index != -1 and # i.e. it was found 
                    img_msg_index > preceding_char_idx and
                    img_msg_index < terminating_char_idx):

                        logging.warning("Received a non-image message, which I wasn't expecting.")
                        
                        self.clear_bytes_in_buffer(0, terminating_char_idx + 1)
                        return valid, None

                else:

                        logging.debug("Starting decode step.")
                        hash_char = self.buffer.find('#'.encode('utf-8'), preceding_char_idx)
                        size_of_data_char = hash_char + 1

                        start_image_char = size_of_data_char + \
                                            1 + 4 + \
                                            self.buffer[size_of_data_char] - ord('0') # Dealing with ASCII

                        end_image_char = terminating_char_idx - 2
                        data_size = terminating_char_idx - preceding_char_idx + 1
                        image_size = end_image_char - start_image_char + 1

                        self.np_buffer = self.np_buffer[start_image_char:end_image_char + 1]
                        result = self.decode_image()

                        logging.debug("Image received")
                        self.clear_bytes_in_buffer(0, terminating_char_idx + 1)

                        valid = True
                        return valid, result


    def get_frame(self):
        while len(self.buffer) < self.minimum_size:
            self.buffer.extend(self.s.recv(self.minimum_size))


        valid, result = self.receive_image()
        if valid:
                        #TODO: Optimise this step

            self.result = result[:self.image_size[0] * self.image_size[1]]
            self.valid = True

        else:
            self.buffer.extend(self.s.recv(self.packet_size))
            self.valid = None



if __name__ == "__main__":
    import cv2

    bk = BK()
    bk.connect()
    
    while True:

        bk.get_frame()

        img_x, img_y = bk.image_size
        if bk.valid:
            cv2.imshow('a', bk.result)
            cv2.waitKey(1)

