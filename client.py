import socket, sys

from server import BUFFER_SIZE

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
BUFFER_SIZE = 1024


def format_msg(path):
    return f"GET" + {path} + "HTTP/1.1\nConnection: keep-alive\r\n\r\n"

def read_message(socket):
    return

# if the response


while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    while True:
    # get path from the CLI
    path = input("\n")
    # something going to break here
    s.send(format_msg(path).encode())
    data = s.recv(BUFFER_SIZE)
s.close()
