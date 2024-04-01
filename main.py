import socket
import random


def ft_open(clientSocket, args):
	clientSocket.connect((args[0], int(args[1])))
	response = clientSocket.recv(1024).decode()
	print(f"Connected to {args[0]}.")
	print(response)
	username = input("Name: ").strip()
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
	print(ipaddr)	
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
		while True:
			data = data_socket.recv(4096)
			if not data:
				break
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


def	main():
	clientSocket = None
	while (True):
		args = input("miniftp> ").strip().split()
		cmd = args[0]
		args = args[1:]
		if (cmd == "quit"):
			break 
		if (cmd == "open"):
			clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			ft_open(clientSocket, args)
		if (cmd == "disconnect" or cmd == "bye"):
			ft_close(clientSocket)
		if (cmd == "ascii"):
			ft_ascii(clientSocket)
		if (cmd == "binary"):
			ft_binary(clientSocket)
		if (cmd == "cd"):
			ft_cd(clientSocket, args)
		if (cmd == "pwd"):
			ft_pwd(clientSocket)
		if (cmd == "ls"):
			ft_ls(clientSocket)
			
main()
