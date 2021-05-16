from socket import socket, AF_INET, SOCK_STREAM
import tkinter
from threading import Thread
import rsa


class Client:
    def __init__(self):
        self.public_key, self.private_key = rsa.newkeys(512)
        self.server_public_key = ''
        self.window = tkinter.Tk()
        self.window.title("Python Skype Clone")
        self.add_user_list()
        self.add_message_list()
        self.add_message_field()
        self.connect()
        tkinter.mainloop()

    def add_message_list(self):
        frame = tkinter.Frame(self.window)
        scrollbar = tkinter.Scrollbar(frame)
        self.message_list = tkinter.Listbox(frame, height=15, width=50, yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.message_list.pack(side=tkinter.RIGHT, expand=False)
        frame.pack()

    def add_user_list(self):
        frame = tkinter.Frame(self.window)
        scrollbar = tkinter.Scrollbar(frame)
        self.user_list = tkinter.Listbox(frame, height=15, width=15, yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.user_list.pack(side=tkinter.LEFT, expand=True)
        frame.pack()

    def add_message_field(self):
        self.message_field = tkinter.Entry(self.window)
        self.message_field.pack()
        self.send_button = tkinter.Button(self.window, text="Send", command=self.send)
        self.send_button.pack()

    def connect(self):
        host = '127.0.0.1'
        port = 21578
        self.buffer_size = 1024
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((host, port))

        # send public key to server
        pk_bytes = self.public_key.save_pkcs1()
        self.client_socket.send(pk_bytes)

        #recive public key from server
        public_data = self.client_socket.recv(self.buffer_size)
        print(public_data.decode("utf8"))
        self.server_public_key = rsa.PublicKey.load_pkcs1(public_data)
        print(self.server_public_key)

        #Start main Thread
        th = Thread(target=self.receive)
        th.start()

    def receive(self):
        while True:
            msg = rsa.decrypt(self.client_socket.recv(self.buffer_size), self.private_key).decode("utf8")
            addUserCode = "---AddUser---"
            removeUserCode = "---RemoveUser---"
            if msg.__contains__(addUserCode):
                name = msg.split(" ")
                self.user_list.insert(tkinter.END, name[1])
            #elif msg.__contains__(removeUserCode):
                #name = msg.split(" ")
                #self.user_list.insert(tkinter.END, name[1])
            else:
                self.message_list.insert(tkinter.END, msg)

    def send(self):
        msg = self.message_field.get()
        self.message_field.delete(0, "end")
        self.client_socket.send(rsa.encrypt(bytes(msg, "utf8"), self.server_public_key))
        if msg == "close":
            self.window.quit()


if __name__ == '__main__':
    client = Client()