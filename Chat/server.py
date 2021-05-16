from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import rsa


class Connection:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.name = 'N/A'
        self.public_key = ""


class Server:
    def __init__(self):
        host = '127.0.0.1'
        port = 21578
        self.public_key, self.private_key = rsa.newkeys(512)
        self.buffer_size = 1024
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.clients = {}
        self.server_socket.listen()
        self.start()

    def start(self):
        main_thread = Thread(target=self.accept_connections)
        main_thread.start()
        main_thread.join()
        self.server_socket.close()

    def accept_connections(self):
        while True:
            print('waiting for connection...')
            conn, addr = self.server_socket.accept()
            print('...connected from:', addr)
            self.clients[conn] = Connection(conn, addr)


            #recive client_publicKey
            public_data = self.clients[conn].conn.recv(self.buffer_size)
            self.clients[conn].public_key = rsa.PublicKey.load_pkcs1(public_data)

            #send publickey
            pk_bytes = self.public_key.save_pkcs1()
            self.clients[conn].conn.send(pk_bytes)

            th = Thread(target=self.client_thread, args=(conn,))
            th.start()

    def client_thread(self, client):

        # get list of current users
        #for cl in self.clients:
        #    currentuser = (bytes("---AddUser--- " + self.clients[cl].name, "utf8"))
        #    client.send(rsa.encrypt(currentuser, self.clients[client].public_key))

        # welcome message specific for new user
        welcomeMessage = (bytes("Welcome, please type your name. (To close type leave)", "utf8"))
        client.send(rsa.encrypt(welcomeMessage, self.clients[client].public_key))

        name = rsa.decrypt(client.recv(self.buffer_size), self.private_key).decode("utf8")

        info = (bytes("Hi " + name + ", type close when you want to leave.", "utf8"))
        client.send(rsa.encrypt(info, self.clients[client].public_key))

        addName = (bytes("---AddUser--- " + name + "", "utf8"))
        self.broadcast(addName)
        # broadcast name
        self.clients[client].name = name
        while True:
            msg = rsa.decrypt(client.recv(self.buffer_size), self.private_key).decode("utf8")
            if msg == bytes("close", "utf8"):
                del self.clients[client]
                message = bytes(name, "utf8") + bytes(" leaving chat", "utf8")
                #removeName = (bytes("---RemoveUser--- " + name + "", "utf8"))
                self.broadcast(message)
                #self.broadcast(removeName)
                break
            else:
                message = bytes(name, "utf8") + bytes(": ", "utf8") + bytes(msg, "utf8")
                self.broadcast(message)

    def broadcast(self, msg):
        for client in self.clients:

            print(self.clients[client].public_key)
            client.send(rsa.encrypt(msg, self.clients[client].public_key))


if __name__ == '__main__':
    server = Server()