import pytest
import numpy as np
from sksurgerybk.interface.bk5000 import BK5000

""" Test image acqusition/decoding from BK5000 """
def test_first_a_not_preceded_by_b():
    
    timeout = 1
    fps = 30
    
    bk = BK5000(timeout, fps)

    bk.np_buffer = np.array([1, 2, 3, 4, 3, 2, 5, 2, 6])

    one_at_start = bk.find_first_a_not_preceded_by_b(0, 1, 2)
    assert one_at_start == 0

    two_not_one = bk.find_first_a_not_preceded_by_b(0, 2, 1)
    assert two_not_one == 5

    subsequent_two_not_one = bk.find_first_a_not_preceded_by_b(two_not_one + 1, 2, 1)
    assert subsequent_two_not_one == 7

    element_not_in_array = bk.find_first_a_not_preceded_by_b(0, 10, 1)
    assert element_not_in_array == -1

    no_match_found = bk.find_first_a_not_preceded_by_b(0, 6, 2)
    assert no_match_found == -1


def test_clear_bytes_in_buffer():

    timeout = 1
    fps = 30
    bk = BK5000(timeout, fps)

    byte_array = bytearray(range(10))

    bk.buffer = bytearray(byte_array)

    bk.clear_bytes_in_buffer(0, 5)
    assert bk.buffer == bytearray([5, 6, 7, 8, 9])

    bk.clear_bytes_in_buffer(3, 4)
    assert bk.buffer == bytearray([5, 6, 7, 9])

    bk.clear_bytes_in_buffer(0, 1000)
    assert bk.buffer == bytearray([])
    