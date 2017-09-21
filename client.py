# Client

import socket
import random
from time import sleep

IP = "localhost"

USED_PORTS = []


def print_msg(sender, msg):
    print '[{}] {}'.format(sender, msg)


def try_to_connect(client_socket, port):
    try:
        client_socket.connect((IP, port))
        return client_socket
    except Exception, e:
        print '[ERROR] {}'.format(e)
        sleep(0.01)
        return establish_client_connection(port)

def establish_client_connection(port):
    """Returns a connection for the received port"""
    print_msg('*', 'Trying to connect to {}:{}'.format(IP, port))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print_msg('*', 'Socket created for {}:{}'.format(IP, port))
    client_socket = try_to_connect(client_socket, port)
    print_msg('*', 'Socket connected for {}:{}'.format(IP, port))
    return client_socket


def establish_server_connection(server_socket, ip, port):
    print_msg('*', 'Trying to bind to {}:{}'.format(IP, port))
    server_socket.bind((ip, port))
    print_msg('*', 'Trying to listen to {}:{}'.format(IP, port))
    server_socket.listen(1)
    print_msg('*', 'Waiting for connection on {}:{}'.format(IP, port))
    return server_socket.accept()


def main():
    """Main method"""
    should_continue = True
    port = 8080
    count = 2
    while should_continue:
        client_socket = establish_client_connection(int(port))
        print_msg('*', 'Connected as client on {}:{}'.format(IP, port))
        msg_length = client_socket.recv(4)
        while not msg_length:
            msg_length = client_socket.recv(4)
        print_msg('*', 'Message length is {}'.format(msg_length))
        msg = client_socket.recv(int(msg_length))
        print '[HQ] {}'.format(msg)
        port = int(client_socket.recv(1000))
        USED_PORTS.append(port)
        if not port:
            should_continue = False
            print '[*] Stopping!'
            continue
        print "[*] NEW PORT: {}".format(port)
        
        count += 2
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket, address = establish_server_connection(server_socket, IP, port)
        print '[*] Found connection on {}:{}'.format(IP, port)
        msg = "Message from CLIENT #{}".format(count)
        port = random.randint(1000, 9999)
        
        client_socket.send(''.join((str(len(msg)).zfill(4), msg)))
        while port in USED_PORTS:
            port = random.randint(1000, 9999)
        if port < 1000 or msg == 'exit':
            print '[*] DISCONNECTING'
            should_continue = False
            client_socket.send(str(0))
            client_socket.close()
            server_socket.close()
            continue
        client_socket.send(str(port))
        client_socket.close()
        print "[*] NEW PORT: {}".format(port)
        USED_PORTS.append(port)


if __name__ == '__main__':
    main()
