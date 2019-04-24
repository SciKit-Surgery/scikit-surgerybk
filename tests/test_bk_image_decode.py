import pytest
import pickle
import sys
import numpy as np

""" Test image acqusition/decoding from BK5000 """
def test_first_a_not_preceded_by_b(bk_5000):
    
    timeout = 1
    fps = 30
    
    bk_5000.np_buffer = np.array([1, 2, 3, 4, 3, 2, 5, 2, 6])

    one_at_start = bk_5000.find_first_a_not_preceded_by_b(0, 1, 2)
    assert one_at_start == 0

    two_not_one = bk_5000.find_first_a_not_preceded_by_b(0, 2, 1)
    assert two_not_one == 5

    subsequent_two_not_one = bk_5000.find_first_a_not_preceded_by_b(two_not_one + 1, 2, 1)
    assert subsequent_two_not_one == 7

    element_not_in_array = bk_5000.find_first_a_not_preceded_by_b(0, 10, 1)
    assert element_not_in_array == -1

    no_match_found = bk_5000.find_first_a_not_preceded_by_b(0, 6, 2)
    assert no_match_found == -1


def test_clear_bytes_in_buffer(bk_5000):

    timeout = 1
    fps = 30

    byte_array = bytearray(range(10))

    bk_5000.buffer = bytearray(byte_array)

    bk_5000.clear_bytes_in_buffer(0, 5)
    assert bk_5000.buffer == bytearray([5, 6, 7, 8, 9])

    bk_5000.clear_bytes_in_buffer(3, 4)
    assert bk_5000.buffer == bytearray([5, 6, 7, 9])

    bk_5000.clear_bytes_in_buffer(0, 1000)
    assert bk_5000.buffer == bytearray([])
    
def test_decode_image(bk_5000):

    sequence =        [1, 2, 3, 27, 254, 3, 4, 27, 251, 6, 27, 228, 27, 1]
    expected_result = [1, 2, 3,     1,   3, 4,     4,   6,     27,  27, 1]

    bk_5000.np_buffer = np.array(sequence)
    result = bk_5000.decode_image()

    np.testing.assert_array_equal(result, expected_result)

def test_decode_image_no_removals(bk_5000):

    sequence = [1, 2, 3, 4, 5] # Should remain unchanged

    bk_5000.np_buffer = np.array(sequence)
    result = bk_5000.decode_image()

    np.testing.assert_array_equal(result, sequence)

def test_receive_image(bk_5000):
    """
    Test that image decoding is working as expected.
    buffer test data is real data acquired from BK5000, and
    the expected image is also a real image.

    """
    # Python 2.x can't by default read data that has been
    # pickled in Python 3, so don't run this test in Python 2
    if sys.version_info.major == 2:
        pytest.skip("Skipping in Python 2 as can't unpickle Python 3 data")
    
    buffer_file = 'tests/data/bk_image_data/bk_buffer.pickle'
    image_file = 'tests/data/bk_image_data/us_image.pickle'

    with open(buffer_file, 'rb') as f_buffer:
        buffer = pickle.load(f_buffer)

    with open(image_file, 'rb') as f_image:
        expected_image = pickle.load(f_image)
    
    # Set the correct image dimensions for decoding.
    # The test image has dimensions of 892 x 728
    bk_5000.parse_win_size_message("DATA:US_WIN_SIZE 892,728;")
    bk_5000.enable_rgb_output()
    bk_5000.buffer = buffer
    bk_5000.get_frame()
    
    np.testing.assert_array_equal(bk_5000.img, expected_image)

    expected_rgb_image = np.dstack([expected_image] * 3)
    np.testing.assert_array_equal(bk_5000.rgb_img, expected_rgb_image)