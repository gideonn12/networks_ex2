import socket
import sys

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
BUFFER_SIZE = 1024


def format_msg(path):
    return "GET " + path + " HTTP/1.1\nConnection: keep-alive\r\n\r\n"


def read_message(s):
    msg = ''
    while True:
        data = s.recv(BUFFER_SIZE)
        if not data:
            break
        msg += data.decode('utf-8')
    return msg


def message_to_file(message, file_name):
    lines = message.splitlines()
    # print the first line
    # print(lines[0])
    print(lines)
    if "200 OK" in lines[0]:
        empty_line_index = lines.index("")
        data = "\n".join(lines[empty_line_index + 1:])
        try:
            data.encode('utf-8')
            with open(file_name, "w") as f:
                f.write(data)
        except UnicodeEncodeError:
            with open(file_name, "wb") as f:
                f.write(data.encode('utf-8'))
    return


# if the response


while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    print("connected to:", TCP_IP, ":", TCP_PORT)
    while True:
        # get path from the CLI
        path = input()
        # something going to break here
        print("the path is:", path)
        print("the msg is: ", format_msg(path))
        print("the encode msd is: ", format_msg(path).encode())
        s.send(format_msg(path).encode())
        print("passed the sending")
        message = read_message(s)
        file_name = path.split("/")[-1] or "index.html"
        message_to_file(message, file_name)
        break
    break
s.close()
