import socket
import random
import time
from getpass import getpass

class FTP:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_status = False
        self.buffer = self.client_socket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
        self.host = None
        
    def print_resp(self):
        resp = self.client_socket.recv(self.buffer).decode()
        print(resp, end="")
        return resp
    
    def open_data_connection(self):
        ip = self.client_socket.getsockname()[0]
        port = random.randint(1024, 65535)
        p1 = str(port // 256)
        p2 = str(port % 256)
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.bind((ip, port))
        data_socket.listen(1)
        
        ip = ip.split(".")
        self.client_socket.send(("PORT " + ",".join(ip) + "," + p1 + "," + p2 + "\r\n").encode())
        resp = self.client_socket.recv(self.buffer).decode()
        print(resp, end="")
        return data_socket, resp
        
    def ascii(self, *args):
        if self.connection_status:
            self.client_socket.send("TYPE A\r\n".encode())
            self.print_resp()
        else:
            print("Not connected.")

    def binary(self, *args):
        if self.connection_status:
            self.client_socket.send("TYPE I\r\n".encode())
            self.print_resp()
        else:
            print("Not connected.")

    def bye(self, *args):
        if self.connection_status:
            self.client_socket.send("QUIT\r\n".encode())
            self.print_resp()
        exit()
    
    def cd(self, directory=None, *args):
        if self.connection_status:
            if not directory:
                directory = input("Remote directory ")
            self.client_socket.send(f"CWD {directory}\r\n".encode())
            self.print_resp() 
        else:
            print("Not connected.")
    
    def close(self, *args):
        if self.connection_status:
            self.client_socket.send("QUIT\r\n".encode())
            print(self.client_socket.recv(self.buffer).decode(), end="")
            self.client_socket.close()
            self.connection_status = False
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            print("Not connected.")
        
    def delete(self, filename=None, *args):
        if self.connection_status:
            if not filename:
                filename = input("Remote file ")
            command = f"DELE {filename}\r\n"
            self.client_socket.send(command.encode())
            self.print_resp()
        else:
            print("Not connected.")
    
    def get(self, remote_file_name=None, local_file_name=None, *args):
        if self.connection_status:
            if not remote_file_name:
                remote_file_name = input("Remote file ")
            if not local_file_name:
                local_file_name = remote_file_name
            data_socket, resp = self.open_data_connection()
            if resp.startswith("200"):
                self.client_socket.send((f"RETR " + remote_file_name + "\r\n").encode())
                recvMessage = self.client_socket.recv(self.buffer).decode()
                print(recvMessage, end="")
                if recvMessage.startswith("150") or recvMessage.startswith("125"):
                    fl = open(local_file_name,"wb")
                    data_con = data_socket.accept()[0]
                    total_bytes = 0
                    start_time = time.perf_counter()
                    while True:
                        file_data = data_con.recv(self.buffer)
                        if not file_data:
                            end_time = time.perf_counter()
                            break
                        total_bytes += len(file_data)
                        fl.write(file_data)
                    fl.close()
                    data_con.close()
                    data_socket.close()
                    print(self.client_socket.recv(self.buffer).decode(),end="")
                    elapsed_time = end_time - start_time
                    if elapsed_time > 0:
                        speed = (total_bytes / elapsed_time) / 1024
                    else:
                        speed = float('inf')
                    print(f"ftp: {total_bytes} bytes received in {elapsed_time:.2f}Seconds {speed:.2f}Kbytes/sec.")
        else:
            print("Not connected.")
    
    def ls(self, folder_name="", local_file_name=None, *args):
        if self.connection_status:
            data_socket, resp = self.open_data_connection()
            if resp.startswith("200"):
                self.client_socket.send(f"NLST {folder_name}\r\n".encode())
                resp = self.print_resp()
                if resp.startswith("150") or resp.startswith("125"):
                    data_conn = data_socket.accept()[0]
                    total_bytes = 0
                    start_time = time.perf_counter()
                    ls_answer = b""
                    while True:
                        data = data_conn.recv(self.buffer)
                        if not data:
                            end_time = time.perf_counter()
                            break
                        total_bytes += len(data)
                        ls_answer += data
                    ls_answer = ls_answer.decode()
                    data_conn.close()
                    data_socket.close()
                    if local_file_name:
                        fo = open(local_file_name, "w")
                        fo.write(ls_answer)
                        fo.close()
                    else:
                        print(ls_answer,end="")
                
                    self.print_resp()   
                    elapsed_time = end_time - start_time
                    if elapsed_time > 0:
                        speed = (total_bytes / elapsed_time) / 1024
                    else:
                        speed = float('inf')
                    print(f"ftp: {total_bytes} bytes received in {elapsed_time:.2f}Seconds {speed:.2f}Kbytes/sec.") 
        else:
            print("Not connected.")

    def open(self, host=None, port=21, *args):
        if self.connection_status:
            print(f"Already connected to {host}, use disconnect first.")
        else:
            if not host:
                host = input("To ")
            
            self.client_socket.connect((host, int(port)))
            self.print_resp()
            self.connection_status = True
            self.host = host
            
            #UTF-8
            self.client_socket.send("OPTS UTF8 ON\r\n".encode())
            self.print_resp()
            
            #username
            username = input(f"User ({host}:(none)): ")
            self.client_socket.send(f"USER {username}\r\n".encode())
            self.print_resp()
            
            #password
            password = getpass(f"Password: ")
            self.client_socket.send(f"PASS {password}\r\n".encode())
            self.print_resp()
        
    def put(self, local_file=None, remote_file=None, *args):
        if self.connection_status:
            if not local_file:
                local_file = input("Local file ")
            data_socket, resp = self.open_data_connection()
            if resp.startswith("200"):
                self.client_socket.send(f"STOR {local_file}\r\n".encode())
                resp = self.print_resp()
                total_bytes = 0
                if resp.startswith("150"):                        
                    data_conn = data_socket.accept()[0]
                    start_time = time.perf_counter()
                    with open(local_file, "rb") as f:
                        while True:
                            data = f.read(self.buffer)
                            if not data:
                                end_time = time.perf_counter()
                                break
                            total_bytes += len(data)
                            data_conn.send(data)
                    data_conn.close()
                    data_socket.close()
                    self.print_resp()
                    elapsed_time = end_time - start_time
                    if elapsed_time > 0:
                        speed = (total_bytes / elapsed_time) / 1024
                    else:
                        speed = float('inf')
                    print(f"ftp: {total_bytes} bytes received in {elapsed_time:.2f}Seconds {speed:.2f}Kbytes/sec.") 
        else:
            print("Not connected.")
    
    def pwd(self, *args):
        if self.connection_status:
            self.client_socket.send("PWD\r\n".encode())
            self.print_resp()
        else:
            print("Not connected.")
    
    def rename(self, old_filename=None, new_filename=None, *args):
        if self.connection_status:
            if not old_filename:
                old_filename, new_filename = input("From name ").strip().split()
                if not old_filename:
                    print("rename from-name to-name.")
            if not new_filename:
                new_filename = input("To name ")
                if not new_filename:
                    print("rename from-name to-name.")
            self.client_socket.send(f"RNFR {old_filename}\r\n".encode())
            resp = self.print_resp()
            if resp.startswith("350"):
                command = f"RNTO {new_filename}\r\n"
                self.client_socket.send(command.encode())
                self.print_resp()
        else:
            print("Not connected.")
    
    def user(self, username=None, password=None, *args):
        if self.connection_status:
            if not username:
                username = input(f"Username ")
            self.client_socket.send(f"USER {username}\r\n".encode())
            resp = self.print_resp()
            if resp.startswith("331"):
                if not password: 
                    password = getpass(f"Password: ")
                self.client_socket.send(f"PASS {password}\r\n".encode())
                resp = self.print_resp()
                if not resp.startswith("230"):
                    print("Login Failed.")
            else:
                print("Login Failed")
        else:
            print("Not connected.")

ftp_instance = FTP()

while True:
    prompt = input("ftp> ")
    prompt = prompt.split()
    if prompt == []:
        continue

    if prompt[0].lower() == "open":
        ftp_instance.open(*prompt[1:])

    elif prompt[0].lower() == "disconnect":
        ftp_instance.close()

    elif prompt[0].lower() == "ascii":
        ftp_instance.ascii()

    elif prompt[0].lower() == "binary":
        ftp_instance.binary()

    elif prompt[0].lower() == "bye" or prompt[0].lower() == "quit":
        ftp_instance.bye()

    elif prompt[0].lower() == "close":
        ftp_instance.close()

    elif prompt[0].lower() == "user":
        ftp_instance.user(*prompt[1:])
    
    elif prompt[0].lower() == "pwd":
        ftp_instance.pwd()

    elif prompt[0].lower() == "delete":
        ftp_instance.delete(*prompt[1:])

    elif prompt[0].lower() == "cd":
        ftp_instance.cd(*prompt[1:])
    
    elif prompt[0].lower() == "rename":
        ftp_instance.rename(*prompt[1:])
    
    elif prompt[0].lower() == "get":
        ftp_instance.get(*prompt[1:])
    
    elif prompt[0].lower() == "put":
        ftp_instance.put(*prompt[1:])
    
    elif prompt[0].lower() == "ls":
        ftp_instance.ls(*prompt[1:])
    
    else:
        print("Invalid command.")