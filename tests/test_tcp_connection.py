
def test_TestServer(setup_server, bk_medical_data_source_worker, socket_var):
    test_message = b'Test message'
    bk_medical_data_source_worker.connect_to_host(socket_var.TCP_IP,
                                                  socket_var.TCP_PORT)
    bk_medical_data_source_worker.send_command_message(test_message)
    bk_medical_data_source_worker.receive_response_message(
                                    socket_var.BUFFER_SIZE)
    print("Received data in test: {:} \n".format(
             bk_medical_data_source_worker.data))
    assert (bk_medical_data_source_worker.data == test_message)
