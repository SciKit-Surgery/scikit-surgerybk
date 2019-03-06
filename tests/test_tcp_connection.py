
def test_TestServer(setup_server, bk_5000, socket_var):
    test_message = 'Test message'
    sent_message = bk_5000.generate_command_message(test_message)
    bk_5000.connect_to_host(address=socket_var["TCP_IP"],
                                                  port=socket_var["TCP_PORT"])
    sentOK = bk_5000.send_command_message(
                                           message=test_message)

    assert sentOK == True
    receiveOK = bk_5000.receive_response_message(
                                  expected_size=len(sent_message))
    assert receiveOK == True
    print("Received data in test: {:} \n".format(
             bk_5000.data))
    assert bk_5000.data.decode() == sent_message

def test_stop_streaming(setup_server, bk_5000, socket_var):
    bk_5000.connect_to_host(address=socket_var["TCP_IP"],
                                                  port=socket_var["TCP_PORT"])
    bk_5000.stop_streaming()
    assert bk_5000.is_streaming == False
    assert bk_5000.request_stop_streaming == False
    print("Received data in test: {:} \n".format(
             bk_5000.data))

def test_start_streaming(setup_server, bk_5000, socket_var):
    bk_5000.connect_to_host(address=socket_var["TCP_IP"],
                                                  port=socket_var["TCP_PORT"])
    bk_5000.start_streaming()
    assert bk_5000.is_streaming == True
    assert bk_5000.request_stop_streaming == False
    print("Received data in test: {:} \n".format(
             bk_5000.data))

def test_request_stop(setup_server, bk_5000, socket_var):
    bk_5000.connect_to_host(address=socket_var["TCP_IP"],
                                                  port=socket_var["TCP_PORT"])
    bk_5000.request_stop()
    assert bk_5000.request_stop_streaming == True
