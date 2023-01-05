import socket
import sys
import os
import argparse


class Server_DFS:
    def __init__(self, directory, filePath, portNo):
        self.host = "localhost"
        self.port = portNo
        self.folder = directory
        self.filepath = filePath
        self.size = 2048

    def socket_conn(self):
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            conn.bind((self.host, self.port))
            conn.listen(20)
            self.sock = conn
            print("Server started on Port " + str(self.port) + "...")
            self.execution_process()
        except socket.error as msg:
            print("Connection not created" + str(msg))
            sys.exit(1)
        except KeyboardInterrupt:
            print("Connection Closed successfully.")
            sys.exit(0)

    def download_func(self, dir):
        try:
            print("Download Starting.")
            msg = "Searching"
            self.conn.sendall(msg.encode())
            fileName = self.conn.recv(self.size)

            if fileName != b'0':
                fileNames = fileName.decode().split("###")
                data_comp = b''
                for f in fileNames:
                    if dir != "":
                        dirPath = "./" + self.folder + "/" + self.filepath + "/" + self.username + "/" + dir + "/"
                    else:
                        dirPath = "./" + self.folder + "/" + self.filepath + "/" + self.username + "/"
                    if os.path.exists(dirPath):
                        dirPath += f
                        if os.path.isfile(dirPath):
                            fh = open(dirPath, "rb")
                            buffer = fh.read()
                            fh.close()
                            data_comp += f.encode() + b'-#####-' + buffer + b'-#####-'
                data_comp = data_comp.rstrip(b'-#####-')
                self.conn.sendall(data_comp)
            else:
                print("File already found on other server.")
                data_comp = b'0'
                self.conn.sendall(data_comp)
            print("Download function completed.")

        except Exception:
            print("Error in download_func.")

    def upload_func(self, directory):
        try:
            print("Upload Starting")
            msg = "Send Data"
            self.conn.sendall(msg.encode())

            data_buffer = b''
            while True:
                self.conn.settimeout(5)
                try:
                    content = self.conn.recv(self.size)
                    if content:
                        data_buffer += content
                    else:
                        break
                except socket.timeout:
                    break

            if data_buffer != b'':
                file1 = data_buffer.split(b'-#####-')[0]
                dir1 = data_buffer.split(b'-#####-')[1]
                if directory != "":
                    filePath = "./" + self.folder + "/" + self.filepath + "/" + self.username + "/" + directory + "/"
                    if not os.path.exists(filePath):
                        os.makedirs(filePath)
                    filePath += file1.decode()
                else:
                    filePath = "./" + self.folder + "/" + self.filepath + "/" + self.username + "/" + file1.decode()

                fh = open(filePath, "wb")
                fh.write(dir1)
                fh.close()

                file2 = data_buffer.split(b'-#####-')[2]
                dir2 = data_buffer.split(b'-#####-')[3]
                if directory != "":
                    filePath = "./" + self.folder + "/" + self.filepath + "/" + self.username + "/" + directory + "/"
                    if not os.path.exists(filePath):
                        os.makedirs(filePath)
                    filePath += file2.decode()
                else:
                    filePath = "./" + self.folder + "/" + self.filepath + "/" + self.username + "/" + file2.decode()

                fh = open(filePath, "wb")
                fh.write(dir2)
                fh.close()

                file3 = data_buffer.split(b'-#####-')[4]
                dir3 = data_buffer.split(b'-#####-')[5]
                if directory != "":
                    filePath = "./" + self.folder + "/" + self.filepath + "/" + self.username + "/" + directory + "/"
                    if not os.path.exists(filePath):
                        os.makedirs(filePath)
                    filePath += file3.decode()
                else:
                    filePath = "./" + self.folder + "/" + self.filepath + "/" + self.username + "/" + file3.decode()

                fh = open(filePath, "wb")
                fh.write(dir3)
                fh.close()

                file4 = data_buffer.split(b'-#####-')[6]
                dir4 = data_buffer.split(b'-#####-')[7]
                if directory != "":
                    filePath = "./" + self.folder + "/" + self.filepath + "/" + self.username + "/" + directory + "/"
                    if not os.path.exists(filePath):
                        os.makedirs(filePath)
                    filePath += file4.decode()
                else:
                    filePath = "./" + self.folder + "/" + self.filepath + "/" + self.username + "/" + file4.decode()
                    print(filePath)

                fh = open(filePath, "wb")
                fh.write(dir4)
                fh.close()

                print(file1.decode() + " uploaded.")
                print(file2.decode() + " uploaded.")
                print(file3.decode() + " uploaded.")
                print(file4.decode() + " uploaded.")
            else:
                print("Upload failed for file.")

            print("File uploaded successfully.")

        except Exception:
            print("Error in upload_func.")

    def show_files_func(self, directory):
        try:
            if directory != "":
                filePath = "./" + self.folder + "/" + self.filepath + "/" + self.username + "/" + directory + "/"
            else:
                filePath = "./" + self.folder + "/" + self.filepath + "/" + self.username + "/"

            if os.path.exists(filePath):
                show_files = os.listdir(filePath)
                fileList = ""
                for f in show_files:
                    fileList += f + "\n"
                fileList = fileList[:-1]

                if len(fileList) == 0:
                    fileList = "0"
            else:
                fileList = "0"
            self.conn.sendall(fileList.encode())
            print("All files displayed.")
        except Exception:
            print("Error in show_file_func.")

    def invalid_func(self):
        try:
            fileList = "Enter valid command."
            self.conn.sendall(fileList.encode())
            print("No operation performed.")
        except Exception:
            print("Error in invalid_func.")

    def execution_process(self):
        try:
            if not os.path.exists(self.folder):
                os.makedirs(self.folder)
            if not os.path.exists(self.folder + "/" + self.filepath):
                os.makedirs(self.folder + "/" + self.filepath)

            while True:
                connection, address = self.sock.accept()
                r1 = connection.recv(self.size)
                r1 = r1.decode()
                menu = str(r1.split(" ")[0]).lower()
                status = "0"

                if menu == "un-pwd":
                    username = str(r1.split(" ")[1])
                    password = str(r1.split(" ")[2])

                    fh = open("Server.conf", "r")
                    fileLines = fh.read().splitlines()

                    for l in fileLines:
                        if l.split()[0] == username and l.split()[1] == password:
                            status = "1"
                            self.username = username
                            break
                        else:
                            status = "0"
                    connection.sendall(status.encode())
                    fh.close()

                if status == "1":
                    filePath = self.folder + "/" + self.filepath + "/" + self.username + "/"
                    if not os.path.exists(filePath):
                        os.makedirs(filePath)
                    self.conn = connection
                    self.addr = address
                    if connection:
                        r1 = connection.recv(self.size)
                        if r1:
                            r1 = r1.decode()
                            command = r1.split(" ")
                            menu = str(command[0]).lower()
                            if menu == "download":
                                if len(command) == 3 and command[2] != "":
                                    dirr = str(command[2])
                                else:
                                    dirr = ""
                                serverDFS.download_func(dirr)
                            elif menu == "upload":
                                if len(command) == 3 and command[2] != "":
                                    dirr = str(command[2])
                                else:
                                    dirr = ""
                                serverDFS.upload_func(dirr)
                            elif menu == "show_files":
                                if len(command) == 2 and command[1] != "":
                                    dirr = str(command[1])
                                else:
                                    dirr = ""
                                serverDFS.show_files_func(dirr)
                            else:
                                serverDFS.invalid_func()
        except Exception:
            print("Error in execution_process.")


if __name__ == '__main__':
    try:
        argpar = argparse.ArgumentParser(description="** ShareIt: DFS Server **")
        argpar.add_argument("Directory", help="Enter Server Directory")
        argpar.add_argument("FilePath", help="Enter File Path")
        argpar.add_argument("PortNo", help="Enter Port No.")
        arguments = argpar.parse_args()
        dirr = str(arguments.Directory)
        filePath = str(arguments.FilePath)
        portNo = int(arguments.PortNo)

    except TypeError:
        print("Port number should be numeric.")
        sys.exit()

    if portNo < 8000 or portNo > 9000:
        print("Enter port number between 8000 and 9000 inclusive")
        sys.exit()

    serverDFS = Server_DFS(dirr, filePath, portNo)
    serverDFS.socket_conn()