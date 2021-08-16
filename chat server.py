#importing libraries
import socket
import threading

#creating server socket for text transfer
server_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#creating server socket for file transfer
server_sock_file=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_sock_file.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#make the adress 127.0.0.1 to work on local machine
host='127.0.0.1'
port=5555
#bind text socket to address (ip,port)
server_sock.bind((host,port))
#bind file socket to same ip but another port
server_sock_file.bind((host,5556))
#listion to connections
server_sock.listen(50)
server_sock_file.listen(50)
#make a list to put in it worker sockets for clients to broadcast the messages
clients=[]
#names of clients
names={}
#put names and worker for clients who connect to file socket to broadcast file
clients_file={}
print('[+] tcp server is Running on address {}:{}'.format(host,port))

#handle connections on file socket
def handle_file(csock_file,caddr_file):
    while True:
        #recieve files at size 1Mb so we make the buffer size equal to 1000000 bytes
        try:

            file_msg=csock_file.recv(1000000)

            sendtoall(clients_file[csock_file] + ' sent file\n')
            for client in clients_file.keys():
                if client != csock_file:
            #we use sendall method to send all mesesage without limites on buffer size
                    client.sendall(file_msg)
            print(clients_file[csock_file]+' sent file')
        except socket.error as err:
            print(err)
            clients_file.pop(csock_file)
            csock_file.close()
            break

#handle connections on text socket
def handle_req(csock,caddr):
    while True:
        try:
            #recieve string values
            msg=csock.recv(1024).decode('utf-8')

        except:
            csock.close()
            clients.remove(csock)
            print(names[csock],' left room')
            sendtoall(names[csock]+' left the room\n')
            break
        #send string values to another clients
        for client in clients:

            if client != csock:
                msg_to_send=names[csock]+': '+msg
                client.send(msg_to_send.encode('utf-8'))
        
#broadcast method
def sendtoall(msg):
    for client in clients:
        client.send(msg.encode('utf-8'))

while True:
    try:
        #accept connections
        csock,caddr=server_sock.accept()
        #first of all the client will send user name to socket so we recieve user name at first and append it to list
        username=csock.recv(1024).decode('utf-8')
        csock_file,caddr_file=server_sock_file.accept()
        print('new connection by {}:{}'.format(username,caddr))
        sendtoall(username+' joined the Chat\n')

        names[csock]=username
        clients.append(csock)
        clients_file[csock_file]=username
        #make thread for texting
        th_text=threading.Thread(target=handle_req,args=(csock,caddr))
        #make thread for files transfer
        th_file=threading.Thread(target=handle_file,args=(csock_file,caddr_file))
      #start threades
        th_text.start()
        th_file.start()
    except socket.error as err:
        print(err)
        continue

#close sockests
for client in clients_file.keys():
    client.close()
    clients_file.pop(client)

for client in clients:
    client.close()
    clients.remove(client)
    names.pop(client)


server_sock.close()
server_sock_file.close()