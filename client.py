import socket, sys

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
BUFFER_SIZE = 1024


def format_msg(path):
    return f"GET" + {path} + "HTTP/1.1\nConnection: keep-alive\r\n\r\n"


def read_message(s):
    msg = ''
    while True:
        data = s.recv(BUFFER_SIZE)
        if not data:
            break
        msg += data.decode()
    return msg


def message_to_file(message, file_name):
    lines = message.splitlines()
    if "200 OK" in lines[0]:
        empty_line_index = lines.index("")
        data = "\n".join(lines[empty_line_index + 1:])
        try:
            data.encode('utf-8')
            with open(file_name, "w") as f:
                f.write(data)
        except UnicodeEncodeError:
            with open(file_name, "wb") as f:
                f.write(message.encode('utf-8'))
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
        read_message(s)

        break
    break
s.close()
