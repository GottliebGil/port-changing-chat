# Client

import socket
import random

IP = "localhost"

USED_PORTS = []

def establish_client_connection(port):
    """Returns a connection for the received port"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, port))
    return client_socket


def establish_server_connection(server_socket, ip, port):
    server_socket.bind((ip, port))
    server_socket.listen(1)
    return server_socket.accept()


def main():
    """Main method"""
    should_continue = True
    port = 8081
    while should_continue:
        client_socket = establish_client_connection(int(port))
        print '[*] Connected as client on {}:{}'.format(IP, port)
        msg_length = client_socket.recv(4)
        msg = client_socket.recv(int(msg_length))
        print '[HQ] {}'.format(msg)
        port = int(client_socket.recv(1000))
        USED_PORTS.append(port)
        if not port:
            should_continue = False
            print '[*] Stopping!'
            continue
        print "[*] NEW PORT: {}".format(port)

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket, address = establish_server_connection(server_socket, IP, port)
        print '[*] Connected as server on {}:{}'.format(IP, port)
        msg = raw_input("Enter your message: ")
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
