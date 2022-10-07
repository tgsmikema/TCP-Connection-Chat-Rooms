import ssl
from datetime import datetime

import select
import socket
import sys
import signal
import argparse
import threading

from Utils import *

SERVER_HOST = 'localhost'

stop_thread = False


def get_and_send(client):
    while not stop_thread:
        data = sys.stdin.readline().strip()
        print(data)
        if data:
            send(client.sock, data)


class ChatClient():
    """ A command line chat client using select """

    def __init__(self, name, port, host=SERVER_HOST):
        self.name = name
        self.connected = False
        self.host = host
        self.port = port

        self.context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

        # Initial prompt
        self.prompt = f'[{name}@{socket.gethostname()}]> '
        # print(f"host name: {socket.gethostname()}")

        # Connect to server at port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock = self.context.wrap_socket(self.sock, server_hostname=host)

            self.sock.connect((host, self.port))
            print(f'Now connected to chat server@ port {self.port}')
            self.connected = True

            # Send my name...
            current_time = datetime.now().strftime("%H:%M")
            send(self.sock,  self.name + ' ; ' + current_time)
            # print(self.sock)
            # print('NAME: ' + self.name)
            data = receive(self.sock)
            # print(data)

            # Contains client address, set it
            addr = data.split('CLIENT: ')[1]
            self.prompt = '[' + '@'.join((self.name, addr)) + ']> '

            threading.Thread(args=(self,)).start()

        except socket.error as e:
            print(f'Failed to connect to chat server @ port {self.port}')
            sys.exit(1)

    def cleanup(self):
        """Close the connection and wait for the thread to terminate."""
        self.sock.close()

    def run(self):
        """ Chat client main loop """
        while self.connected:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()

                # Wait for input from stdin and socket
                # readable, writeable, exceptional = select.select([0, self.sock], [], [])
                readable, writeable, exceptional = select.select(
                    [self.sock], [], [])

                for sock in readable:
                    # if sock == 0:
                    #     data = sys.stdin.readline().strip()
                    #     if data:
                    #         send(self.sock, data)
                    if sock == self.sock:
                        data = receive(self.sock)
                        if not data:
                            print('Client shutting down.')
                            self.connected = False
                            break
                        else:
                            print(data)
                            sys.stdout.flush()

            except KeyboardInterrupt:
                print(" Client interrupted. " "")
                stop_thread = True
                self.cleanup()
                break

    def get_client_and_group_list(self):
        send(self.sock, "special-command-get-c")
        data = receive(self.sock)
        # print(data)
        return data

    def get_own_name(self):
        send(self.sock, "special-command-get-own-name")
        data = receive(self.sock)
        print(data)
        return data

    def create_new_room(self):
        send(self.sock, "special-command-create-new-room")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', action="store", dest="name", required=True)
    parser.add_argument('--port', action="store",
                        dest="port", type=int, required=True)
    given_args = parser.parse_args()

    port = given_args.port
    name = given_args.name

    client = ChatClient(name=name, port=port)
    client.run()