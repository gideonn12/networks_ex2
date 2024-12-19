import os
import socket
import sys

TCP_PORT = int(sys.argv[1])
BUFFER_SIZE = 1024

# Set up the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', TCP_PORT))
s.listen(0)

# A function to search if the file exists
def search_file(file_name):
    if file_name.startswith('/'):
        file_name = file_name[1:]
    file_path = os.path.join('files', file_name)
    return os.path.exists(file_path)

# Function to read file contents
def read_file(file_name):
    if file_name.startswith('/'):
        file_name = file_name[1:]
    file_path = os.path.join('files', file_name)
    return file_path

# Function to decipher the client's message
def decipher_message(message):
    lines = message.split('\n')
    get_line = None
    connection_line = None
    for line in lines:
        if line.startswith('GET'):
            get_line = line.split(' ')[1]  # Extract the file path
        elif line.startswith('Connection'):
            connection_line = line.split(': ')[1].strip()  # Extract connection type
    return get_line, connection_line

# Function to read the message from the client
def read_message(connection):
    data = ''
    terminate = 0
    connection.settimeout(5)
    while True:
        try:
            chunk = connection.recv(BUFFER_SIZE).decode()
            if not chunk:
                return None
            data += chunk
            if data.__contains__('\r\n\r\n'):
                terminate += 2
            elif data.__contains__('\r\n'):
                terminate += 1
            if terminate >= 2:
                return data
        except socket.timeout:
            return None

# Function to send all data reliably
def send_all(connection, data):
    total_sent = 0
    while total_sent < len(data):
        sent = connection.send(data[total_sent:])
        if sent == 0:
            raise RuntimeError("Socket connection broken")
        total_sent += sent

# Function to send a file in chunks
def send_file_in_chunks(connection, file_path):
    with open(file_path, 'rb') as f:
        while chunk := f.read(BUFFER_SIZE):
            send_all(connection, chunk)

# Function to create and send the HTTP response
def return_message(connection, connection_type, file):
    http_response = 'HTTP/1.1'
    conn_response = 'Connection: '
    length_response = 'Content-Length: '
    location_response = 'Location: '

    if file == "/redirect":
        http_response += ' 301 Moved Permanently\n'
        conn_response += 'close\n'
        location_response += "/result.html\n"
        response = http_response + conn_response + location_response + '\n'
        send_all(connection, response.encode())
        return False

    if search_file(file):
        http_response += ' 200 OK\n'
        conn_response += connection_type + '\n'
        file_path = read_file(file)
        file_size = os.path.getsize(file_path)
        length_response += str(file_size) + '\n\n'
        response = http_response + conn_response + length_response
        send_all(connection, response.encode())
        send_file_in_chunks(connection, file_path)
        return True
    else:
        http_response += ' 404 Not Found\n'
        conn_response += 'close\n'
        response = http_response + conn_response + '\n'
        send_all(connection, response.encode())
        connection.close()
        return False

# Main loop to handle client connections
while True:
    conn, addr = s.accept()
    print(f"Connection from {addr}")
    while True:
        message_from_client = read_message(conn)
        if not message_from_client:
            break
        print(message_from_client)
        file, connection_type = decipher_message(message_from_client)
        if file == "/":
            file = "/index.html"
        if not return_message(conn, connection_type, file):
            break
    conn.close()
