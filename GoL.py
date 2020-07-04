'''
Name: Mohsen Mahmoodzadeh
Student ID: 9622762362
'''
# This code is
#   based on https://nostarch.com/download/samples/PythonPlayground_sampleCh3.pdf
#   prepared for Computer Networking Class: Ferdowsi University of Mashhad

import matplotlib; matplotlib.use("TkAgg")  # For pycharm IDE only
import numpy as np
import matplotlib.pyplot as plt;
import matplotlib.animation as animation

from agent import Agent
# from packet import Packet
import pickle
import uuid
import random
import socket
# from packet import *



PACKET_LENGTH = 500

N = 30  # Grid size is N*N
live = 255
dead = 0
state = [live, dead]

# Create random population (more dead than live):
grid = np.random.choice(state, N * N, p=[0.3, 0.7]).reshape(N, N)
# To learn more about not uniform random visit:
# https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.random.choice.html


def update(data):
    global grid
    temp = grid.copy()
    for i in range(N):
        for j in range(N):
            # Compute 8-neighbor sum
            total = (grid[i, (j - 1) % N] + grid[i, (j + 1) % N] +
                     grid[(i - 1) % N, j] + grid[(i + 1) % N, j] +
                     grid[(i - 1) % N, (j - 1) % N] + grid[(i - 1) % N, (j + 1) % N] +
                     grid[(i + 1) % N, (j - 1) % N] + grid[(i + 1) % N, (j + 1) % N]) / 255
            # Apply Conway's Rules:
            # 1- Any live cell with fewer than two live neighbours dies, as if by underpopulation.
            # 2- Any live cell with two or three live neighbours lives on to the next generation.
            # 3- Any live cell with more than three live neighbours dies, as if by overpopulation.
            # 4- Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
            if grid[i, j] == live:
                if (total < 2) or (total > 3):
                    temp[i, j] = dead
            else:
                if total == 3:
                    temp[i, j] = live
    mat.set_data(temp)
    grid = temp
    # dead_agent = random_select_dead_agent(grid)
    return mat

def random_select_dead_agent(board):
    dead_array = []
    height, width = board.shape
    for i in range(height):
        for j in range(width):
            if board[i, j] == dead:
                dead_array.append((i,j))
                
    candidate_dead = [dead_array[i] for i in np.random.choice(len(dead_array), 1, replace=False)] 
    random_selected_agent = Agent(id=uuid.uuid4(), X= candidate_dead[0][0], Y=candidate_dead[0][1], state=dead)
    return random_selected_agent
    # return candidate_dead[0] # returns a tuple
    
def byte_generator():
    bit = [0, 1]
    byte_sample = random.choices(bit, k=8)
    
    byte_str = ""
    for i in range(len(byte_sample)):
        byte_str += str(byte_sample[i])

    return byte_str

def random_byte_data(n):
    random_byte_data = ""

    for i in range(n):
        random_byte_data += byte_generator()
    
    return random_byte_data


def create_message(agent):
    message = ""
    randomData_id_sep = '|'
    id_X_sep = '@'
    X_Y_sep = '#'
    # seprator = '|'

    id = str(agent.id)
    X = str(agent.X)
    Y = str(agent.Y)
    n = random.randint(500, 1500)

    message += random_byte_data(n)
    # message += seprator
    message += randomData_id_sep
    message += id
    # message += seprator
    message += id_X_sep
    message += X
    # message += seprator
    message += X_Y_sep
    message += Y 

    return message 


# Animation
fig, ax = plt.subplots()
mat = ax.matshow(grid)
# ani = animation.FuncAnimation(fig, update, interval=500)
# random_selected_agent = random_select_dead_agent(grid)

server_ip = "localhost"
server_port = 8000
server_address = (server_ip, server_port)
seq_num = 0

while True:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(10)
    

    ani = animation.FuncAnimation(fig, update, interval=500)
    random_selected_agent = random_select_dead_agent(grid)
    message = create_message(random_selected_agent)
    print('id of agent is= ', str(random_selected_agent.id))
    print('X of agent is= ', str(random_selected_agent.X))
    print('Y of agent is= ', str(random_selected_agent.Y))
    print()

    msg_len = len(message)
    num_packets = msg_len // PACKET_LENGTH + 1
    packets = []
    data = None
    
    for i in range(num_packets):
        if i != (num_packets-1):
            data = message[i*PACKET_LENGTH: (i+1)*PACKET_LENGTH]
        else:
            data = message[i * PACKET_LENGTH:]
        
        packets.append(data)
        # packet = Packet(data)
        # obj = pickle.dumps(packet)
        # bytes(packet)
        # packet.make(data)
    
        
    try:
        for i in range(len(packets)):
            data = packets[i]
        # client_socket.sendto(message.encode(encoding='utf-8'), server_address)
            client_socket.sendto(data.encode(encoding='utf-8'), server_address)
            data = None

        # while True:
        #     print('Waiting to receive...')
        #     try:
        #         pass

    except:
        print("Closing socket")
        client_socket.close()
    


plt.show()


