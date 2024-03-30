import socket

def ft_open(clientSocket, args):
	clientSocket.connect((args[0], int(args[1])))
	response = clientSocket.recv(1024).decode()
	print("Connected to test.rebex.net.")
	print(response)
	username = input("Name: ")
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


def	main():
	while (True):
		args = input("miniftp> ").strip().split()
		cmd = args[0]
		args = args[1:]
		clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		if (cmd == "quit"):
			break 

		if (cmd == "open"):
			ft_open(clientSocket, args)
		
		if (cmd == "disconnect"):
			ft_close(clientSocket)
			
main()
