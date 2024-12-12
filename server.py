import os
from os import close

import socket, sys

#TCP_IP = '127.0.0.1'
TCP_PORT = int(sys.argv[1])
TCP_PORT = 12345
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', TCP_PORT))
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
            data += (connection.recv(BUFFER_SIZE)).decode()
            print("received:", data)
            if not data:
                connection.close()
                return None
            if data.__contains__('\r\n\r\n'):
                terminate += 2
            elif data.__contains__('\r\n'):
                terminate += 1
            if terminate == 2:
                return data
        except socket.timeout:
            connection.close()
            return None

def return_message(connection, connectionType, file):
    http_response = 'HTTP/1.1'
    conn_response = 'Connection: '
    length_response = 'Content-Length: '
    location_response = 'Location: '

    if file == "result.html":
        http_response += ' 301 Found\n'
        conn_response += 'close\n'
        location_response += "/result.html\n"
        response = http_response + conn_response + location_response + '\n'
        connection.send(response.encode())
        return  # Return early for this condition

    if search_file(file):
        print("file found")
        http_response += ' 200 OK\n'
        conn_response += connectionType + '\n'
        file_content = read_file(file)
        length_response += str(len(file_content)) + '\n\n'
        response = http_response + conn_response + length_response + file_content + '\n'
        connection.send(response.encode())
        print("res sent")
    else:
        http_response += ' 404 Not Found\n'
        conn_response += 'close\n'
        response = http_response + conn_response + '\n'
        connection.send(response.encode())



while True:
    conn, addr = s.accept()
    print('New connection from:', addr)
    while True:
        message_from_client = read_message(conn)
        if not message_from_client:
            break

        # print the msg from the client to the screen
        # print(message_from_client)

        file, connectionType = decipher_message(message_from_client)
        if file == "/":
            file = "index.html"
        elif file == "/redirect":
            file = "result.html"
        print("file:", file)
        return_message(conn,connectionType,file)
        if connectionType == 'close':
            break
    conn.close()
