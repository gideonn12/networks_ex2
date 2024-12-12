import socket,sys

TCP_IP = '127.0.0.1'
TCP_PORT = int(sys.argv[1])
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(0)

while True:
	conn, addr = s.accept()
	print('New connection from:', addr)
	while True:
		data = conn.recv(BUFFER_SIZE)
		if not data: break
		print("received:", data) 
	conn.close()