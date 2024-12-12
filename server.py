import os
from os import close
import socket,sys

TCP_IP = '127.0.0.1'
TCP_PORT = int(sys.argv[1])
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(0)


# a function to search for the file
# if the file exists, ret true, else ret false
def search_file(file_name):
    try:
        f = open(file_name, 'r')
        f.close()
        return True
    except:
        return False

def read_file(file_name):
    # Construct the full path to the file
    file_path = os.path.join('files', file_name)

    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"File {file_name} not found."
    except Exception as e:
        return str(e)



def return_message():
    return

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

def print_message(msg):

    return

while True:
    conn, addr = s.accept()
    print('New connection from:', addr)
    while True:
        message_from_client = read_message(conn)
        if not message_from_client:
            break
        file,connection = decipher_message(message_from_client)

    conn.close()