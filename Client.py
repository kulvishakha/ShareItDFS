import socket
import sys
import time
import hashlib
import re
import os
import argparse
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class Client_DFS:
    def __init__(self, server1, server2, server3, server4, port_no1, port_no2, port_no3, port_no4):
        self.server1 = server1
        self.server2 = server2
        self.server3 = server3
        self.server4 = server4
        self.port_no1 = int(port_no1)
        self.port_no2 = int(port_no2)
        self.port_no3 = int(port_no3)
        self.port_no4 = int(port_no4)
        self.file_size = 2048

    def socket_conn(self):
        try:
            self.conn1 = "dn"
            self.conn2 = "dn"
            self.conn3 = "dn"
            self.conn4 = "dn"

            try:
                sock_conn1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock_conn1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock_conn1.connect((self.server1, self.port_no1))
                self.sock_conn1 = sock_conn1
                self.conn1 = "up"
            except socket.error:
                print("Server 1 is not running!")

            try:
                sock_conn2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock_conn2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock_conn2.connect((self.server2, self.port_no2))
                self.sock_conn2 = sock_conn2
                self.conn2 = "up"
            except socket.error:
                print("Server 2 is not running!")

            try:
                sock_conn3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock_conn3.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock_conn3.connect((self.server3, self.port_no3))
                self.sock_conn3 = sock_conn3
                self.conn3 = "up"
            except socket.error as msg:
                print("Server 3 is not running!")

            try:
                sock_conn4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock_conn4.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock_conn4.connect((self.server4, self.port_no4))
                self.sock_conn4 = sock_conn4
                self.conn4 = "up"
            except socket.error:
                print("Server 4 is not running!")

        except KeyboardInterrupt:
            print("Socket is closed successfully!")
            sys.exit(0)

    def processing_command(self, cmd):
        server_reply1 = b'2'
        server_reply2 = b'2'
        server_reply3 = b'2'
        server_reply4 = b'2'
        try:
            if self.conn1 == "up":
                self.sock_conn1.sendall(cmd.encode())
            if self.conn2 == "up":
                self.sock_conn2.sendall(cmd.encode())
            if self.conn3 == "up":
                self.sock_conn3.sendall(cmd.encode())
            if self.conn4 == "up":
                self.sock_conn4.sendall(cmd.encode())

            if self.conn1 == "up":
                server_reply1 = self.sock_conn1.recv(self.file_size)
            if self.conn2 == "up":
                server_reply2 = self.sock_conn2.recv(self.file_size)
            if self.conn3 == "up":
                server_reply3 = self.sock_conn3.recv(self.file_size)
            if self.conn4 == "up":
                server_reply4 = self.sock_conn4.recv(self.file_size)
        except Exception:
            print("Error in processing_command!")

        return server_reply1, server_reply2, server_reply3, server_reply4

    def downlaod(self, fileName):
        try:
            print("File Download starting:")

            chunk1 = b'.' + fileName.encode() + b'.1'
            chunk2 = b'.' + fileName.encode() + b'.2'
            chunk3 = b'.' + fileName.encode() + b'.3'
            chunk4 = b'.' + fileName.encode() + b'.4'

            chunk1_data = b''
            chunk2_data = b''
            chunk3_data = b''
            chunk4_data = b''

            for i in range(1, 5):
                chunk_files = b''

                if chunk1_data == b'':
                    chunk_files += chunk1 + b'###'
                if chunk2_data == b'':
                    chunk_files += chunk2 + b'###'
                if chunk3_data == b'':
                    chunk_files += chunk3 + b'###'
                if chunk4_data == b'':
                    chunk_files += chunk4 + b'###'

                if chunk_files != b'':
                    chunk_files = chunk_files.rstrip(b'###')

                if chunk_files == b'':
                    chunk_files = b'0'

                print("Chunk Files: " + str(chunk_files))

                if i == 1 and self.conn1 == "up":
                    self.sock_conn1.sendall(chunk_files)
                elif i == 2 and self.conn2 == "up":
                    self.sock_conn2.sendall(chunk_files)
                elif i == 3 and self.conn3 == "up":
                    self.sock_conn3.sendall(chunk_files)
                elif i == 4 and self.conn4 == "up":
                    self.sock_conn4.sendall(chunk_files)

                bufferData = b''
                while True:
                    try:
                        if i == 1 and self.conn1 == "up":
                            self.sock_conn1.settimeout(5)
                            data = self.sock_conn1.recv(self.file_size)
                            if data:
                                bufferData += data
                            else:
                                break
                        elif i == 2 and self.conn2 == "up":
                            self.sock_conn2.settimeout(5)
                            data = self.sock_conn2.recv(self.file_size)
                            if data:
                                bufferData += data
                            else:
                                break
                        elif i == 3 and self.conn3 == "up":
                            self.sock_conn3.settimeout(5)
                            data = self.sock_conn3.recv(self.file_size)
                            if data:
                                bufferData += data
                            else:
                                break
                        elif i == 4 and self.conn4 == "up":
                            self.sock_conn4.settimeout(5)
                            data = self.sock_conn4.recv(self.file_size)
                            if data:
                                bufferData += data
                            else:
                                break
                        else:
                            break

                    except socket.timeout:
                        break

                if bufferData != b'0':
                    bd = bufferData.split(b'-#####-')

                    while len(bd):
                        if chunk1 == bd[0]:
                            chunk1_data = bd[1]
                        elif chunk2 == bd[0]:
                            chunk2_data = bd[1]
                        elif chunk3 == bd[0]:
                            chunk3_data = bd[1]
                        elif chunk4 == bd[0]:
                            chunk4_data = bd[1]
                        del bd[0:1]

            if len(chunk1_data) != 0 and len(chunk2_data) != 0 and len(chunk3_data) != 0 and len(chunk4_data) != 0:
                decoded_chunk1_data = self.ck.decrypt(chunk1_data)
                decoded_chunk2_data = self.ck.decrypt(chunk2_data)
                decoded_chunk3_data = self.ck.decrypt(chunk3_data)
                decoded_chunk4_data = self.ck.decrypt(chunk4_data)
                fData = decoded_chunk1_data + decoded_chunk2_data + decoded_chunk3_data + decoded_chunk4_data

                if not os.path.exists("Downloads"):
                    os.makedirs("Downloads")
                fileHandle = open("./Downloads/" + self.username + "_" + fileName, "wb")
                fileHandle.write(fData)
                fileHandle.close()
                print("File saved in the Downloads directory.")
            elif len(chunk1_data) == 0 and len(chunk2_data) == 0 and len(chunk3_data) == 0 and len(chunk4_data) == 0:
                print("File not found.")
            else:
                print("Incomplete File.")
        except Exception:
            print("Error: File is not downloaded.")

    def upload(self, fileName):
        try:
            print("File upload starting.")
            filePath = self.directory + "/" + fileName
            if os.path.isfile(filePath):
                fileHandle = open(filePath, "rb")
                file_size = os.path.getsize(filePath)
                chunk_size = file_size // 4
                chunks = []
                for i in range(4):
                    data = fileHandle.read(chunk_size)
                    chunks.append(data)

                hashValue = hashlib.md5()
                hashValue.update(fileName.encode())
                filename = fileName.encode()
                chunks1_encoded = self.ck.encrypt(chunks[0])
                chunks2_encoded = self.ck.encrypt(chunks[1])
                chunks3_encoded = self.ck.encrypt(chunks[2])
                chunks4_encoded = self.ck.encrypt(chunks[3])

                server1 = b'.' + filename + b'.1' + b'-#####-' + chunks1_encoded + b'-#####-' + b'.' + filename + b'.2' + b'-#####-' + chunks2_encoded + b'-#####-' + b'.' + filename + b'.3' + b'-#####-' + chunks3_encoded + b'-#####-' + b'.' + filename + b'.4' + b'-#####-' + chunks4_encoded
                server2 = b'.' + filename + b'.1' + b'-#####-' + chunks1_encoded + b'-#####-' + b'.' + filename + b'.2' + b'-#####-' + chunks2_encoded + b'-#####-' + b'.' + filename + b'.3' + b'-#####-' + chunks3_encoded + b'-#####-' + b'.' + filename + b'.4' + b'-#####-' + chunks4_encoded
                server3 = b'.' + filename + b'.1' + b'-#####-' + chunks1_encoded + b'-#####-' + b'.' + filename + b'.2' + b'-#####-' + chunks2_encoded + b'-#####-' + b'.' + filename + b'.3' + b'-#####-' + chunks3_encoded + b'-#####-' + b'.' + filename + b'.4' + b'-#####-' + chunks4_encoded
                server4 = b'.' + filename + b'.1' + b'-#####-' + chunks1_encoded + b'-#####-' + b'.' + filename + b'.2' + b'-#####-' + chunks2_encoded + b'-#####-' + b'.' + filename + b'.3' + b'-#####-' + chunks3_encoded + b'-#####-' + b'.' + filename + b'.4' + b'-#####-' + chunks4_encoded

                fileHandle.close()

                if self.conn1 == "up":
                    self.sock_conn1.sendall(server1)
                if self.conn2 == "up":
                    self.sock_conn2.sendall(server2)
                if self.conn3 == "up":
                    self.sock_conn3.sendall(server3)
                if self.conn4 == "up":
                    self.sock_conn4.sendall(server4)

                time.sleep(5)
                print("File is uploaded successfully.")
            else:
                print("File not Found.")
        except Exception:
            print("Upload resulted in error.")

    def show_files(self, listFiles):
        try:
            fileNames = []
            listFiles = listFiles
            fileFN = re.findall('.(.*).([1-4])', listFiles)
            fileFN.sort(key=lambda x: (x[0], int(x[1])))

            fileN_list = re.findall('.(.*).[1-4]', listFiles)
            for i in fileN_list:
                if i not in fileNames:
                    fileNames.append(i)

            fc = {}  # count of files present
            for file in fileNames:
                chunk1 = 0
                chunk2 = 0
                chunk3 = 0
                chunk4 = 0
                for key, value in fileFN:
                    if file == key:
                        if value == "1":
                            chunk1 = 1
                        if value == "2":
                            chunk2 = 1
                        if value == "3":
                            chunk3 = 1
                        if value == "4":
                            chunk4 = 1

                chunks_count = chunk1 + chunk2 + chunk3 + chunk4
                if chunks_count == 4:
                    status = ""
                else:
                    status = "[Partial]"
                fc[file] = status

            for file, status in fc.items():
                print(file + " " + status)
        except Exception:
            print("Error in show files.")

    def menu_command(self, mc):
        try:
            commnd = mc.split(" ")
            menu = str(commnd[0]).lower()
            list_menu = [menu]

            if menu == "download" or menu == "upload":
                fn = str(commnd[1])
                if len(commnd) == 3 and commnd[2] != "":
                    filedir = str(commnd[2])
                else:
                    filedir = ""
                if fn != "":
                    fileName = fn
                    list_menu.append(fileName.lower())
                    if filedir != "":
                        filefolder = filedir
                        list_menu.append(filefolder.lower())
                else:
                    list_menu = 1
            elif menu == "show_files":
                if len(commnd) == 2 and commnd[1] != "":
                    filedir = str(commnd[1])
                    list_menu.append(filedir.lower())
                else:
                    list_menu = [menu]
            else:
                list_menu = 1
            return list_menu
        except IndexError:
            return 0
        except Exception:
            return 0

    def sndrcv_command(self, command, directory, userName, password):
        try:
            self.directory = directory
            self.username = userName
            self.password = password
            setD = hashes.Hash(hashes.SHA256(), backend=default_backend())
            setD.update(str(self.password).encode())
            k = base64.urlsafe_b64encode(setD.finalize())
            self.ck = Fernet(k)

            p, q, r, s = c.processing_command("un-pwd " + self.username + " " + self.password)
            if (p.decode() == "1" or p.decode() == "2") and (q.decode() == "1" or q.decode() == "2") and (r.decode() == "1" or r.decode() == "2") and (s.decode() == "1" or s.decode() == "2"):
                if command != 0 and command != 1:
                    if command[0] == "download":
                        if len(command) == 3 and command[2] != "":
                            complete_cmd = command[0] + " " + command[1] + " " + command[2]
                        else:
                            complete_cmd = command[0] + " " + command[1]
                        c.processing_command(complete_cmd)
                        fileName = str(command[1])
                        c.downlaod(fileName)

                    elif command[0] == "upload":
                        if len(command) == 3 and command[2] != "":
                            complete_cmd = command[0] + " " + command[1] + " " + command[2]
                        else:
                            complete_cmd = command[0] + " " + command[1]
                        c.processing_command(complete_cmd)
                        fileName = str(command[1])
                        c.upload(fileName)

                    elif command[0] == "show_files":
                        if len(command) == 2 and command[1] != "":
                            complete_cmd = command[0] + " " + command[1]
                        else:
                            complete_cmd = command[0]
                        p, q, r, s = c.processing_command(complete_cmd)
                        p = p.decode()
                        q = q.decode()
                        r = r.decode()
                        s = s.decode()
                        print("Files available in the servers are: ")
                        if (p == "0" or p == "2") and (q == "0" or q == "2") and (r == "0" or r == "2") and (s == "0" or s == "2"):
                            print("No file Found")
                        else:
                            generatedList = p + "\n" + q + "\n" + r + "\n" + s + "\n"
                            c.show_files(generatedList)

                elif command == 1:
                    print("Enter your choice:")
                else:
                    print("Enter proper arguments.")
            else:
                print("Wrong Username or Password. Retry.")
        except Exception:
            print("Error in sndrcv_command.")


if __name__ == '__main__':
    try:
        argpar = argparse.ArgumentParser(description="** ShareIt: DFS Client **")
        argpar.add_argument("dir", help="Enter directory of files")
        argpar.add_argument("conf", help="Enter conf file of users")
        arguments = argpar.parse_args()
        dirr = str(arguments.dir)
        config = str(arguments.conf)

        filePath = "./" + config
        fileHandle = open(filePath, "r")
        fileLines = fileHandle.read().splitlines()

        username = ""
        password = ""

        serverIP1 = ""
        serverIP2 = ""
        serverIP3 = ""
        serverIP4 = ""
        serverPort_no1 = 0
        serverPort_no2 = 0
        serverPort_no3 = 0
        serverPort_no4 = 0

        for l in fileLines:
            if l == "" or l.split()[0] == "###":
                continue
            elif l.split()[0] == "Server1":
                serverIP1 = l.split()[1].split(":")[0]
                serverPort_no1 = l.split()[1].split(":")[1]
            elif l.split()[0] == "Server2":
                serverIP2 = l.split()[1].split(":")[0]
                serverPort_no2 = l.split()[1].split(":")[1]
            elif l.split()[0] == "Server3":
                serverIP3 = l.split()[1].split(":")[0]
                serverPort_no3 = l.split()[1].split(":")[1]
            elif l.split()[0] == "Server4":
                serverIP4 = l.split()[1].split(":")[0]
                serverPort_no4 = l.split()[1].split(":")[1]
            elif l.split()[0] == "Username":
                username = l.split()[1]
            elif l.split()[0] == "Password":
                password = l.split()[1]
            else:
                continue
        fileHandle.close()

        if serverIP1 == "" or serverIP2 == "" or serverIP3 == "" or serverIP4 == "":
            print("Check the configuration file for server IPs.")

        if serverPort_no1 == 0 or serverPort_no2 == 0 or serverPort_no3 == 0 or serverPort_no4 == 0:
            print("Check the configuration file for server ports.")
            sys.exit()

        while True:

            command = input("\n *** Enter your choice: ***"
                            "\n Upload [fileName] "
                            "\n Download [fileName] "
                            "\n Show_files "
                            "\n >> : ")

            filePath = "./" + config
            fileHandle = open(filePath, "r")
            fileLines = fileHandle.read().splitlines()
            for l in fileLines:
                if l.split()[0] == "Username":
                    username = l.split()[1]
                elif l.split()[0] == "Password":
                    password = l.split()[1]

            c = Client_DFS(serverIP1, serverIP2, serverIP3, serverIP4, serverPort_no1, serverPort_no2, serverPort_no3, serverPort_no4)
            c.socket_conn()
            cmd = c.menu_command(command)
            c.sndrcv_command(cmd, dirr, username, password)
    except Exception:
        print("Error in Main.")
