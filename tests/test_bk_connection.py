import pytest
import mock
from sksurgerybk.interface.bk5000 import BK5000

""" Test the TCP connection to BK5000 """

@mock.patch('socket.socket.connect')
def test_connect_to_host(mocked_connect, bk_5000):
    address = '127.0.0.1'
    port = 5005
    bk_5000.connect_to_host(address, port)
    mocked_connect.assert_called_with((address, port))

def test_connect_to_host_raises_error(bk_5000):
    invalid_ip = '1.2.3.4'
    invalid_port = 1234
    with pytest.raises(IOError):
        bk_5000.connect_to_host(invalid_ip, invalid_port)
        
test_msg = "Hello"
def test_command_message(bk_5000):
    
    expected = "\x01" + test_msg + "\x04"
    cmd_msg = bk_5000.generate_command_message(test_msg)

    assert cmd_msg == expected

@mock.patch('socket.socket.send', return_value=len(test_msg)+2)
def test_send_command_message(mocked_send, bk_5000):
    is_ok = bk_5000.send_command_message(test_msg)
    assert is_ok

    expected = "\x01" + test_msg + "\x04"
    mocked_send.assert_called_with(expected.encode())

    msg_wrong_size = "short_msg"
    with pytest.raises(IOError):
        is_ok = bk_5000.send_command_message(msg_wrong_size)
        assert is_ok == False

def test_fail_to_send_message_raises_error(bk_5000):
    with pytest.raises(IOError):
        bk_5000.send_command_message("Failing message")

def test_request_stop(bk_5000):
    bk_5000.request_stop()
    assert bk_5000.request_stop_streaming == True

return_message = b'\x01test\x04'
@mock.patch('socket.socket.recv', return_value = return_message)
def test_receive_response_message(mocked_recv, bk_5000):
    bk_5000.receive_response_message()
    assert bk_5000.data == b'test'

    with pytest.raises(IOError):
        is_ok = bk_5000.receive_response_message(expected_size=0)
        assert is_ok == False

def test_failed_to_receive_raises_error(bk_5000):
    with pytest.raises(IOError):
        bk_5000.receive_response_message() 
    
@mock.patch('socket.socket.recv', return_value = False)
@mock.patch('socket.socket.close')
def test_disconnect_from_host(mocked_recv, mocked_close, bk_5000):
    bk_5000.disconnect_from_host()
    mocked_recv.assert_called()
    mocked_close.assert_called()

start_message = b'QUERY:GRAB_FRAME \"ON\",50;'
@mock.patch('socket.socket.send', return_value=len(start_message) + 2)
@mock.patch('socket.socket.recv', return_value='ACK')
def test_start_streaming(mocked_send, mocked_recv, bk_5000):
    bk_5000.start_streaming()
    assert bk_5000.is_streaming

def test_start_streaming_raises_error(bk_5000):
    with pytest.raises(IOError):
        bk_5000.start_streaming()

stop_message = b'QUERY:GRAB_FRAME \"OFF\",50;'
@mock.patch('socket.socket.send', return_value=len(stop_message) + 2)
@mock.patch('socket.socket.recv', return_value='ACK')
def test_stop_streaming(mocked_send, mocked_recv, bk_5000):
    bk_5000.stop_streaming()
    mocked_recv.assert_called()
    mocked_send.assert_called()

    assert bk_5000.is_streaming == False
    assert bk_5000.request_stop_streaming == False

def test_stop_streaming_raises_error(bk_5000):
    with pytest.raises(IOError):
        bk_5000.stop_streaming()

query_size_message = b"QUERY:US_WIN_SIZE;"
@mock.patch('socket.socket.send', return_value=len(query_size_message) + 2)
@mock.patch('socket.socket.recv', return_value=b'\x01DATA:US_WIN_SIZE 640,480;\x04')
def test_query_win_size(mocked_send, mocked_recv, bk_5000):
    bk_5000.query_win_size()
    assert bk_5000.image_size == [640, 480]

def test_query_win_size_raises_error(bk_5000):
    with pytest.raises(IOError):
        bk_5000.query_win_size()

query_scanarea_message = b"QUERY:GEOMETRY_SCANAREA:A;"
@mock.patch('socket.socket.send', return_value=len(query_scanarea_message) + 2)
@mock.patch('socket.socket.recv', return_value= \
                b'\x01DATA:B_GEOMETRY_SCANAREA:A 0.0017218,-0.000171398, \
                1.37236,0,-0.00174855,-0.000176821,1.77236,0.0203479;\x04'
                )
def test_query_and_parse_scanarea(mocked_send, mocked_recv, bk_5000):
        bk_5000.query_scanarea()

        expected_values = [     0.0017218,
                                -0.000171398,
                                1.37236,
                                0,
                                -0.00174855,
                                -0.000176821,
                                1.77236,
                                0.0203479
                          ]
                          
        assert bk_5000.scan_geometry['StartLineX']      ==  expected_values[0]
        assert bk_5000.scan_geometry['StartLineY']      ==  expected_values[1]
        assert bk_5000.scan_geometry['StartLineAngle']  ==  expected_values[2]
        assert bk_5000.scan_geometry['StartDepth']      ==  expected_values[3]
        assert bk_5000.scan_geometry['StopLineX']       ==  expected_values[4]
        assert bk_5000.scan_geometry['StopLineY']       ==  expected_values[5]
        assert bk_5000.scan_geometry['StopDepthAngle']  ==  expected_values[6]
        assert bk_5000.scan_geometry['StopDepth']       ==  expected_values[7]
