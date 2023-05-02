ShareIt Distributed File System



We have implemented a DFS for reliable and secure file storage.


Objective:
Our system's overall structure is rather straightforward; it consists of a client, and one or more file servers. We have implemented security in our DFS using hashing to achieve encrypted storage. Our main plan is to focus on performance, scalability, availability, data integrity and security.


Background:
Allow clients to store and retrieve files on multiple servers. Files are divided into pieces and stored on different servers.


Implementation:


Client : The appropriate server directories are set up at server startup to store the files. The client checks the username and password from the configuration file and confirms it with the server when it launches. If the credentials are correct, a message asking for the command to be entered and executed or a username/password message is shown. For listing, uploading files to servers, and getting files from servers, there are three options: ShowFiles, Upload, Download. 


When a file name is supplied along with the Upload command, the file is split into four pieces and uploaded to the server. Password and username are both in plain text. 


When the Download command is used with a file name, all servers that are active are queried for the file. If any of the file's components are missing, either no file is created or a download folder is used to store the file.


When the ShowFiles command is used, all the file portions are fetched from the server and checked to see if the entire file is present. If not, a notification that is incomplete is displayed next to the file name.


Server: The server responds to the client's request and takes appropriate action. It verifies the user each time the command is sent. In the DFS servers, a directory is created for each user to house their files. The guidelines are followed when renaming the files. Multiple clients can be handled by the code.


Data Encryption: Data is encrypted before transmission and decrypted upon receipt.


Traffic optimization: Instead of retrieving every file from every server, only those portions of the files that are missing from the first server are requested, and so on.


Subfolder on DFS Servers: If the user includes a subfolder as a command argument, that subfolder's contents will be listed, downloaded, and uploaded to the server.


Requirement:
Python v3.11
Server: Running on multiple ports
Client: Running with different user configurations
Files for testing in the TestFiles folder or any other path given by user


IDE for Development:
Pycharm Terminal window inside pycharm for running programs.


Commands for running program:


For multiple servers:
* python3 Server.py Servers Server1 8008
* python3 Server.py Servers Server2 8080
* python3 Server.py Servers Server3 8800
* python3 Server.py Servers Server4 8880


For multiple clients:
* python3 Client.py TestFiles User1.conf
* python3 Client.py TestFiles User2.conf
* python3 Client.py TestFiles User3.conf
