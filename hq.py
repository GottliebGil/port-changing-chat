# Headquarters

import socket
import random

IP = "localhost"

USED_PORTS = []


def establish_client_connection(port):
    """Returns a connection for the received port"""
    print 'trying to connect to {}:{}'.format(IP, port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'socket created for {}:{}'.format(IP, port)
    client_socket.connect((IP, port))
    print 'socket connected for {}:{}'.format(IP, port)
    return client_socket


def establish_server_connection(server_socket, ip, port):
    server_socket.bind((ip, port))
    server_socket.listen(1)
    return server_socket.accept()


def main():
    """Main method"""
    port = 8081
    should_continue = True
    while should_continue:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket, address = establish_server_connection(server_socket, IP, port)
        print '[*] Connected as server on {}:{}'.format(IP, port)
        msg = raw_input("Enter your message: ")
        port = random.randint(1000, 9999)
        client_socket.send(''.join((str(len(msg)).zfill(4), msg)))
        while port in USED_PORTS:
            port = random.randint(1000, 9999)
        if msg == 'exit':
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

        client_socket = establish_client_connection(int(port))
        print '[*] Connected as client on {}:{}'.format(IP, port)
        msg_length = client_socket.recv(4)
        msg = client_socket.recv(int(msg_length))
        print '[BASE] {}'.format(msg)
        port = int(client_socket.recv(1000))
        USED_PORTS.append(port)
        if not port:
            should_continue = False
            print '[*] Stopping!'
            continue
        print "[*] NEW PORT: {}".format(port)


if __name__ == '__main__':
    main()