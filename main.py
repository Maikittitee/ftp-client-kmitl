import socket

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

def ft_ls(clientSocket):
	clientSocket.send("PASV\r\n".encode())
	print(clientSocket.recv(1024).decode())
	clientSocket.send("LIST\r\n".encode())
	print(clientSocket.recv(1024).decode())

def ft_cd(client_socket, args):
        client_socket.send(f"CWD {args[0]}\r\n".encode("utf-8"))
        data = client_socket.recv(1024)
        print(data.decode())
        
def ft_pwd(client_socket):
        client_socket.send("XPWD\r\n".encode("utf-8"))
        data = client_socket.recv(1024)
        print(data.decode())

def ft_user(client_socket):
	user = input("(username) ")
	client_socket.send(f"USER {user}\r\n".encode("utf-8"))
	print(client_socket.recv(1024).decode())
	password = input("Password: ")
	client_socket.send(f"PASS {password}\r\n".encode("utf-8"))


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
		
		if (cmd == "disconnect"):
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
			# noooooo
			ft_ls(clientSocket)
			
main()
