import math
import ssl

import select
import socket
import sys
import signal
import argparse
from datetime import datetime

from Utils import *

SERVER_HOST = 'localhost'


class ChatServer(object):
    """ An example chat server using select """

    def __init__(self, port, backlog=5):
        self.clients = 0
        self.clientmap = {}
        self.outputs = []  # list output sockets

        self.clients_list = []
        self.groups = 0
        self.groups_list = []


        self.context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        self.context.load_cert_chain('new.pem', 'private.key')
        self.context.set_ciphers('AES128-SHA')

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        self.server.listen(backlog)
        self.server = self.context.wrap_socket(self.server, server_side=True)
        # Catch keyboard interrupts
        signal.signal(signal.SIGINT, self.sighandler)

        print(f'Server listening to port: {port} ...')

    def sighandler(self, signum, frame):
        """ Clean up client outputs"""
        print('Shutting down server...')

        # Close existing client sockets
        for output in self.outputs:
            output.close()

        self.server.close()

    def get_client_name(self, client):
        """ Return the name of the client """
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        # print(info)
        return '@'.join((name, host))

    def run(self):
        # inputs = [self.server, sys.stdin]
        inputs = [self.server]
        self.outputs = []
        running = True
        while running:
            try:
                readable, writeable, exceptional = select.select(
                    inputs, self.outputs, [])
            except select.error as e:
                break

            for sock in readable:
                sys.stdout.flush()
                if sock == self.server:
                    # handle the server socket
                    client, address = self.server.accept()
                    print(
                        f'Chat server: got connection {client.fileno()} from {address}')
                    # Read the login name
                    received_data_initial = receive(client).split(' ; ')
                    cname = received_data_initial[0]
                    connection_time = received_data_initial[1]

                    # Compute client name and send back
                    self.clients += 1
                    send(client, f'CLIENT: {str(address[0])}')
                    inputs.append(client)

                    self.clientmap[client] = (address, cname, connection_time)


                    # last field is the 1 to 1 other client cname.
                    self.clients_list.append([cname, address, connection_time, "", ""])


                    print(self.clientmap[client])
                    # Send joining information to other clients
                    msg = f'\n(Connected: New client ({self.clients}) from {self.get_client_name(client)})'
                    for output in self.outputs:
                        send(output, msg)
                    self.outputs.append(client)

                # elif sock == sys.stdin:
                #     # didn't test sys.stdin on windows system
                #     # handle standard input
                #     cmd = sys.stdin.readline().strip()
                #     if cmd == 'list':
                #         print(self.clientmap.values())
                #     elif cmd == 'quit':
                #         running = False
                else:
                    # handle all other sockets
                    try:
                        data = receive(sock)
                        # print("-----------------------------")
                        # print(data)
                        if data:

                            if data == "special-command-get-c":
                                current_time = datetime.now().strftime("%H:%M")
                                time_format = "%H:%M"
                                datetime_now = datetime.strptime(current_time, time_format)
                                for client_record in self.clients_list:
                                    datetime_connection = datetime.strptime(client_record[2], time_format)
                                    time_difference = datetime_now - datetime_connection
                                    total_seconds = time_difference.total_seconds()
                                    if total_seconds < 60:
                                        client_record[4] = "(now)"
                                    elif total_seconds < 3600:
                                        client_record[4] = f"({math.floor(total_seconds/60)} min ago)"
                                    else:
                                        client_record[4] = f"({math.floor(total_seconds/3600)} hour ago)"
                                send(sock, [self.clients_list, self.groups_list])

                            elif data == "special-command-get-own-name":
                                own_name = self.get_client_name(sock).split("@")[0]
                                send(sock, own_name)

                            else:
                                # Send as new client's message...
                                current_time = datetime.now().strftime("%H:%M")
                                msg = f'\n{self.get_client_name(sock).split("@")[0]} ({current_time}) : {data}'
                                # print(msg)

                                # Send data to all except ourself
                                for output in self.outputs:
                                    # if output != sock:
                                    send(output, msg)
                        else:
                            print(f'Chat server: {sock.fileno()} hung up')
                            self.clients -= 1
                            sock.close()
                            inputs.remove(sock)
                            self.outputs.remove(sock)

                            # print("----------------------------------------------")
                            # print(self.get_client_name(sock))
                            # print(self.get_client_name(sock).split('@')[0])

                            for client_record in self.clients_list:
                                if self.get_client_name(sock).split('@')[0] == client_record[0]:
                                    self.clients_list.remove(client_record)

                            # Sending client leaving information to others
                            msg = f'\n(Now hung up: Client from {self.get_client_name(sock)})'

                            for output in self.outputs:
                                send(output, msg)
                    except socket.error as e:
                        # Remove
                        inputs.remove(sock)
                        self.outputs.remove(sock)

        self.server.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Socket Server Example with Select')
    parser.add_argument('--name', action="store", dest="name", required=True)
    parser.add_argument('--port', action="store",
                        dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    name = given_args.name

    server = ChatServer(port)
    server.run()
