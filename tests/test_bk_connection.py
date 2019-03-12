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

@mock.patch('socket.socket.recv', return_value = b'\x01test\x04')
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

@mock.patch('socket.socket.send', return_value=27)
@mock.patch('socket.socket.recv', return_value='ACK')
def test_start_streaming(mocked_send, mocked_recv, bk_5000):
    bk_5000.start_streaming()
    assert bk_5000.is_streaming

def test_start_streaming_raises_error(bk_5000):
    with pytest.raises(IOError):
        bk_5000.start_streaming()

@mock.patch('socket.socket.send', return_value=28)
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

@mock.patch('socket.socket.send', return_value=20)
@mock.patch('socket.socket.recv', return_value=b'\x01DATA:US_WIN_SIZE 640,480;\x04')
def test_query_win_size(mocked_send, mocked_recv, bk_5000):
    bk_5000.query_win_size()
    assert bk_5000.image_size == [640, 480]

def test_query_win_size_raises_error(bk_5000):
    with pytest.raises(IOError):
        bk_5000.query_win_size()


