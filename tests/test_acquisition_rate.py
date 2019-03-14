import pytest
import time
from sksurgerybk.interface.bk5000 import BK5000

def test_framerate():

    bk = BK5000(timeout = 5, frames_per_second = 25)

    TCP_IP = '128.16.0.3' # Default IP of BK5000
    TCP_PORT = 7915       # Default port of BK5000

   

    try:
        bk.connect_to_host(TCP_IP, TCP_PORT)
    
    except:
        pytest.skip("No BK Available")
        
    bk.query_win_size()
    bk.start_streaming()

    # get 100 frames
    n_frames = 100

    start = time.time()
    for i in range(n_frames):
        bk.get_frame() 

    end = time.time()
    acqusition_time = end - start

    print("Time to get 100 frames: {}".format(acqusition_time))
    
    bk.stop_streaming()
    bk.disconnect_from_host()

    expected_time = n_frames / bk.frames_per_second

    acceptable_difference = 0.1
    assert abs(expected_time - acqusition_time) < acceptable_difference

    

