from pyModbusTCP.server import ModbusServer, DataBank
import time

server = ModbusServer("", 1500, no_block=True)

try:
    server.start()
    print("Server is online!")
    while True:
        state = DataBank.get_words(1)
        #print(f'O valor do registrador é ' + str(state), end='\r')
        time.sleep(0.5)
        continue
except:
    print("Shutdown server ...")
    server.stop()
    print("Server is offline")
