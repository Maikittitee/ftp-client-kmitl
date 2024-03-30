import socket

def	main():
	while (True):
		args = input("ftp> ").strip().split()
		cmd = args[0]
		args = args[1:]

		if (cmd == "quit"):
			# disconnect 
			exit (0)

		if (cmd == "open"):
			clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
		
		if (cmd == "disconnect"):
			clientSocket.close()
			
main()
