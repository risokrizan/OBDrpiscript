import obdimport timeimport jsonimport serialfrom iothub_client import IoTHubClient, IoTHubTransportProvider, IoTHubMessage# Azure IoT HubCONNECTION_STRING = "HostName=OBDLOG.azure-devices.net;DeviceId=RPi1;SharedAccessKey=/uGkNvfJAs//p+57idGGWKGJOY+t8HmfuUQFvda8RhU="PROTOCOL = IoTHubTransportProvider.MQTT# confirmation callbackdef send_confirmation_callback(message, result, user_context):    print("Confirmation received for message with result = %s" % (result))client = IoTHubClient(CONNECTION_STRING, PROTOCOL)# OBD serial portdevices = obd.scan_serial()# GPS serial port# gps_ser = serial.Serial("/dev/ttyS0", 115200)# Object for JSON.stringify()prejsonValues = {}# connect to vehicletry:    connection = obd.OBD(devices[0])    pids = connection.supported_commands    print(str(devices[0]))except Exception as ELM_missing:    print("Chyba pripojenia k vozidlu: " + str(ELM_missing))    exit()# collect pidswhile True:    for pid in pids:        try:            decrypted_pid = connection.query(obd.commands[pid.name])            # print(str(decrypted_pid.value) + " " + str(pid.name))            prejsonValues[str(pid.name)] = str(decrypted_pid.value)            #print(str(pid.name) + " " + str(lastValues[pid.name]))        except Exception as Decryption_failed:            print("Chyba dekodovania hodnoty: " + str(pid.name) + " ,chyba: " + str(Decryption_failed))    # send obd data    message = IoTHubMessage(json.dumps(prejsonValues, separators=(',', ':')))    client.send_event_async(message, send_confirmation_callback, None)    print("Message transmitted to IoT Hub")    # time between data    time.sleep(5)