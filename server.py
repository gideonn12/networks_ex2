import os
from os import close

import socket, sys

TCP_IP = '127.0.0.1'
TCP_PORT = int(sys.argv[1])
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(0)


# a function to search for the file
# if the file exists, ret true, else ret false
def search_file(file_name):
    file_path = os.path.join('files', file_name)
    return os.path.exists(file_path)


def read_file(file_name):
    # Construct the full path to the file
    file_path = os.path.join('files', file_name)
    if file_name.endswith('.jpg') or file_name.endswith('.ico'):
        with open(file_path, 'rb') as f:
            return f.read()
    else:
        with open(file_path, 'r') as f:
            return f.read()


def decipher_message(message):
    lines = message.split('\n')
    get_line = None
    connection_line = None
    for line in lines:
        if line.startswith('GET'):
            get_line = line.split(' ')[1]  # Extract text from GET till HTTP
        elif line.startswith('Connection'):
            connection_line = line.split(': ')[1]  # Extract text from Connection till the end
    return get_line, connection_line


def read_message(connection):
    data = ''
    terminate = 0
    connection.settimeout(1)
    while True:
        try:
            data += connection.recv(BUFFER_SIZE)
            print("received:", data)
            if not data:
                close(connection)
                return None
            if data.__contains__('\r\n'):
                terminate += 1
            if terminate == 2:
                return data
        except socket.timeout:
            close(connection)
            return None


def return_message(connection, file):
    http_response = 'HTTP/1.1'
    conn_response = 'Connection: '
    length_response = 'Content-Length: '
    location_response = 'Location: '

    if file == "result.html":
        http_response += ' 301 Found\n'
        conn_response += 'close\n'
        location_response += "/result.html\n"
        connection.send(http_response + conn_response + location_response + '\n')
    if search_file(file):
        http_response += ' 200 OK\n'
        conn_response += connection + '\n'
        # TODO: check if hello world is 11 as should be
        length_response += str(len(read_file(file))) + '\n\n'
        connection.send(http_response + conn_response + length_response + '\n' + read_file(file) + '\n')
    else:
        http_response += ' 404 Not Found\n'
        conn_response += 'close\n'
        connection.send(http_response + conn_response + '\n')
        return
    return


while True:
    conn, addr = s.accept()
    print('New connection from:', addr)
    while True:
        message_from_client = read_message(conn)
        if not message_from_client:
            break

        # print the msg from the client to the screen
        print(message_from_client)

        file, connection = decipher_message(message_from_client)
        if file == "/":
            file = "index.html"
        elif file == "/redirect":
            file = "result.html"
        return_message(conn, file)
        if connection == 'close':
            break
    conn.close()
