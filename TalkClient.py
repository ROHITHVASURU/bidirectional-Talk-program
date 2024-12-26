import socket
import threading
import sys

class TalkClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print("Connected to the chat server.")
            threading.Thread(target=self.receive_messages).start()
            self.send_messages()
        except ConnectionRefusedError:
            print("Unable to connect to the server.")
            raise

    def send_messages(self):
        while self.connected:
            try:
                msg = input("You (client) : ")
                if msg.lower() == "quit":
                    self.connected = False
                    print("Exiting chat...")
                    self.socket.close()
                    break
                if msg == "STATUS":
                    print(f"[STATUS] Client: {self.get_local_ip()}; Server: {self.get_server_ip()}")
                elif self.connected:  # Check if still connected before sending
                    self.socket.sendall(msg.encode())
            except OSError:
                break  # Break if socket operation fails


    def receive_messages(self):
        while self.connected:
            try:
                incoming_msg = self.socket.recv(1024).decode()
                if not incoming_msg:
                    print("Server has closed the connection. Exiting...")
                    break
                print("Server:", incoming_msg)
            except OSError:
                print("Connection lost. Exiting...")
                break

        self.connected = False
        self.socket.close()
        sys.exit()

                
    def get_local_ip(self):
        if self.socket:
            return f"{self.socket.getsockname()[0]}:{self.socket.getsockname()[1]}"
        return "Not Connected"

    def get_server_ip(self):
        if self.socket:
            return f"{self.socket.getpeername()[0]}:{self.socket.getpeername()[1]}"
        return "Not Connected"
