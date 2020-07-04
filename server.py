'''
Name: Mohsen Mahmoodzadeh
Student ID: 9622762362
'''
import socket
import threading
import time
import datetime

# from pacekt import *


# BUFFER_SIZE = 13000
BUFFER_SIZE = 500
randomData_id_sep = '|'
id_X_sep = '@'
X_Y_sep = '#'

def handle_connection(address, data):
    pass
    # time.sleep(0.5)
    # start_time = time.time()
    # print("Request started at: " + str(datetime.datetime.utcnow()))
    # packet = Packet()
    # thread_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



server_ip = "localhost"
server_port = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (server_ip, server_port)
print('Starting up on %s port %s' % server_address)
server_socket.bind(server_address)

while True:
    try:

        msg_length = 0
        # print('Waiting to receive message...')
        data, address = server_socket.recvfrom(BUFFER_SIZE)
        
        data = data.decode(encoding='utf-8')
        
        # data = packet.data
        # length = packet.length
        # checksum = packet.checksum

        id = X = Y = None

        # data  = data.decode(encoding='utf-8')
        # msg_components = data.split(sep=seprator)
        # id = msg_components[1]
        # X = msg_components[2]
        # Y = msg_components[3]

        if randomData_id_sep in data:
            splitted_data = data.split(randomData_id_sep)
            random_data = splitted_data[0]
            target_data = splitted_data[1]
            if id_X_sep in target_data:
                splitted_target = target_data.split(id_X_sep)
                id = splitted_target[0]
                location_data = splitted_target[1]
                if X_Y_sep in location_data:
                    splitted_location = location_data.split(X_Y_sep)
                    X = splitted_location[0]
                    Y = splitted_location[1]


        if id == None and X == None and Y == None: # that means we received a packet with just random data
            # print('Received %s bytes' % (len(data)))
            msg_length += len(data)
            continue
        
        else:
            print('id of agent is= ', id)
            print('X of agent is= ', X)
            print('Y of agent is= ', Y)
            

        # connection_thread = threading.Thread(target=handle_connection, args=(address, data))
        # connection_thread.start()
            print('Received %s bytes' % (len(data)))
            print()
            msg_length += len(data)
            print('Total message length is=  %s bytes' % (len(data)))
            print()
    except:
        print("Closing socket...")
        server_socket.close()