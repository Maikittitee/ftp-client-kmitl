import socket
import random


def ft_open(clientSocket, args):
	host = args[0]
	port = int(args[1]) if len(args) > 1 else 21
	clientSocket.connect((host, port))
	# clientSocket.settimeout(1)
	response = clientSocket.recv(1024).decode()
	print(f"Connected to {host}.")
	print(response)
	clientSocket.send(f'OPTS UTF8 ON\r\n'.encode())
	print(clientSocket.recv(1024).decode())
	username = input(f'User ({host}:(none)): ')
	clientSocket.send(("USER " + username + "\r\n").encode())
	response = clientSocket.recv(1024).decode()
	password = input(response)
	clientSocket.send(("PASS " + password + "\r\n").encode())
	response = clientSocket.recv(1024).decode()
	print(response)

def	ft_close(clientSocket):
	clientSocket.send("QUIT\r\n".encode())
	print(clientSocket.recv(1024).decode())
	clientSocket.close()

def ft_ascii(clientSocket):
	clientSocket.send("TYPE A\r\n".encode())
	print(clientSocket.recv(1024).decode())

def ft_binary(clientSocket):
	clientSocket.send("TYPE I\r\n".encode())
	print(clientSocket.recv(1024).decode())

def parse_pasv_response(response):
	parts = response.split('(')[1].split(')')[0].split(',')
	host = '.'.join(parts[:4])
	port = int(parts[4])*256 + int(parts[5])
	return host, port

def ft_ls(clientSocket, file=''):
	number = random.randint(0,65535)
	ipaddr = socket.gethostbyname(socket.gethostname())+f".{number//256}.{number%256}"
	ipaddr = ipaddr.replace('.',',')
	
	clientSocket.send(f'PORT {ipaddr}\r\n'.encode())
	resp = clientSocket.recv(1024).decode()
	print(resp,end='')
	clientSocket.sendall(b'PASV\r\n')
	pasv_response = clientSocket.recv(1024).decode()
	data_host, data_port =  parse_pasv_response(pasv_response)
	with socket.create_connection((data_host, data_port)) as data_socket:
		clientSocket.sendall((f'NLST {file}\r\n').encode())
		dir_response = clientSocket.recv(1024).decode()
		print(dir_response, end='')
		if dir_response.startswith('5'):
			return
		data = True
		while data:
			data = data_socket.recv(4096)
			print(data.decode(), end='')
		control_response = clientSocket.recv(1024).decode()
		print(control_response, end='')

def ft_cd(client_socket, args):
		client_socket.send(f"CWD {args[0]}\r\n".encode())
		data = client_socket.recv(1024)
		print(data.decode())
		
def ft_pwd(client_socket):
		client_socket.send("XPWD\r\n".encode())
		data = client_socket.recv(1024)
		print(data.decode())

def ft_user(client_socket):
	user = input("(username) ")
	client_socket.send(f"USER {user}\r\n".encode())
	print(client_socket.recv(1024).decode())
	password = input("Password: ")
	client_socket.send(f"PASS {password}\r\n".encode())

def ft_get(client_socket, args):
	filename = args[0]
	number = random.randint(0,65535)
	ipaddr = socket.gethostbyname(socket.gethostname())+f".{number//256}.{number%256}"
	ipaddr = ipaddr.replace('.',',')
	client_socket.send(f'PORT {ipaddr}\r\n'.encode())
	print(client_socket.recv(1024).decode())
	
	client_socket.sendall(b'PASV\r\n')
	pasv_response = client_socket.recv(1024).decode()
	data_host, data_port = parse_pasv_response(pasv_response)

	client_socket.send(f"RETR {filename}\r\n".encode())
	print(client_socket.recv(1024).decode())

	data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	data_socket.settimeout(10)
	data_socket.connect((data_host, data_port))
	with open(filename, 'wb') as lf:
		while True:
			try:
				data = data_socket.recv(1024)
				if not data:
					break
				lf.write(data)
			except socket.timeout:
				print("Data connection timed out.")
				break
			except Exception as e:
				print("An error occurred:", e)
				break
	data_socket.close()
	resp = client_socket.recv(1024).decode()
	print(resp)

def ft_delete(client_socket, args):
	file = input('Remote file ') if len(args) == 0 else args[0]
	client_socket.send(f'DELE {file}\r\n'.encode())
	resp = client_socket.recv(1024)
	print(resp.decode())

def ft_rename(client_socket, args):
	from_name = input('(from name) ') if len(args) <= 0 else args[0]
	to_name = input('(to name) ') if len(args) <= 1 else args[1]
	client_socket.send(f'RNFR {from_name}\r\n'.encode())
	print(client_socket.recv(1024).decode())
	client_socket.send(f'RNTO {to_name}\r\n'.encode())
	print(client_socket.recv(1024).decode())

def ft_put(client_socket, args):
	if (len(args) < 1):
		file = input("Local file ")
		new = input("Remote file ")
	elif (len(args) < 2):
		file = args[0]
		new = file

	number = random.randint(0,65535)
	ipaddr = socket.gethostbyname(socket.gethostname())+f".{number//256}.{number%256}"
	ipaddr = ipaddr.replace('.',',')
	client_socket.send(f'PORT {ipaddr}\r\n'.encode())
	port_status = client_socket.recv(1024)
	print(port_status.decode(),end="")
	with open(file,'rb') as f:
		try:

			client_socket.sendall(b'PASV\r\n')
			response = client_socket.recv(1024).decode()
			port_start = response.find('(') + 1
			port_end = response.find(')')
			port_str = response[port_start:port_end].split(',')
			data_port = int(port_str[-2]) * 256 + int(port_str[-1])
			data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			data_socket.connect((socket.gethostbyname(self.name), data_port))
			client_socket.sendall((f'STOR {new}\r\n').encode())
			response = client_socket.recv(4096).decode()
			print(response,end='')
			if not response.startswith('150'):
				return
			data = f.read(4096)
			while data:
				data_socket.sendall(data)
				data = f.read(4096)
		finally:
			data_socket.close()
		response = client_socket.recv(1024)
		print(response.decode(),end='')


def	main():
	clientSocket = None
	while (True):
		args = input("ftp> ").strip().split()
		cmd = args[0]
		args = args[1:]
		# print(f"cmd is {cmd}")
		if (cmd == "quit" or cmd == "bye"):
			break 
		elif (cmd == "open"):
			clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			ft_open(clientSocket, args)
		elif (cmd == "disconnect" or cmd == "close"):
			ft_close(clientSocket)
		elif (cmd == "ascii"):
			ft_ascii(clientSocket)
		elif (cmd == "binary"):
			ft_binary(clientSocket)
		elif (cmd == "cd"):
			ft_cd(clientSocket, args)
		elif (cmd == "pwd"):
			ft_pwd(clientSocket)
		elif (cmd == "ls"):
			ft_ls(clientSocket, "" if len(args) == 0 else args[0])
		elif (cmd == "get"):
			ft_get(clientSocket, args)
		elif (cmd == "delete"):
			ft_delete(clientSocket, args)
		elif (cmd == "put"):
			ft_put(clientSocket, args)
		elif (cmd == "user"):
			ft_user(clientSocket)
		else:
			print("Invalid command.")

main()
