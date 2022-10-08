import socket
import pickle
import struct

def send(channel, *args):
    buffer = pickle.dumps(args, pickle.HIGHEST_PROTOCOL)
    # print("-------------------------------")
    # print(buffer)
    value = socket.htonl(len(buffer))
    # print(value)
    size = struct.pack("Q", value)
    # print(size)
    channel.send(size)
    channel.send(buffer)

def receive(channel):
    size = struct.calcsize("Q")
    # print("-------------------------------")
    # print(size)
    size = channel.recv(size)
    # print(size)
    try:
        size = socket.ntohl(struct.unpack("Q", size)[0])
        # print(size)
    except struct.error as e:
        return ''
    buf = ""
    while len(buf) < size:
        buf = channel.recv(size - len(buf))
    # print(pickle.loads(buf)[0])
    return pickle.loads(buf)[0]

