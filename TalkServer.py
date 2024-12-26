import socket
import threading
import sys

class TalkServer:
    def __init__(self, port):
        self.port = port
        self.socket = None
        self.clients = []
        self.running = True  # Flag to indicate if the server is running

    def start(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(("localhost", self.port))
            self.socket.listen()
            print(f"Chat server started on port {self.port}")

            threading.Thread(target=self.accept_clients).start()
            self.send_messages()
        except Exception as e:
            print(f"Server error: {e}")
            self.shutdown_server()

    def accept_clients(self):
        while self.running:
            try:
                client, address = self.socket.accept()
                print(f"New connection from {address}")
                self.clients.append(client)
                threading.Thread(target=self.handle_client, args=(client,)).start()
            except socket.error:
                break  # Break the loop if socket is closed


    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024).decode()
                if not message:
                    self.client_disconnected(client)
                    break
                print(f"Client {client.getpeername()} says: {message}")
            except ConnectionResetError:
                # This exception is raised when a client disconnects abruptly
                self.client_disconnected(client)
                break
            except OSError:
                # This catches the 'Bad file descriptor' OSError
                self.client_disconnected(client)
                break
            except Exception as e:
                print(f"Error with client {client.getpeername()}: {e}")
                break

    def send_messages(self):
        while True:
            msg = input("Server: ")
            if msg.lower() == "exit":
                print("Shutting down server...")
                self.shutdown_server()
            elif msg == "STATUS":
                self.print_status()
            else:
                self.send_to_client(msg)

            
    def send_to_client(self, message):
        for client in self.clients:
            try:
                client.sendall(message.encode())
            except Exception as e:
                print(f"Error sending message: {e}")

    def shutdown_server(self):
        self.running = False  # Set the running flag to False
        for client in self.clients:
            try:
                client.close()
            except Exception as e:
                print(f"Error closing client connection: {e}")
        self.socket.close()
        sys.exit()

    def get_local_ip(self):
        if self.socket:
            return f"{self.socket.getsockname()[0]}:{self.socket.getsockname()[1]}"
        return "Not Connected"

    def print_status(self):
        server_ip = self.get_local_ip()
        for client in self.clients:
            client_ip = f"{client.getpeername()[0]}:{client.getpeername()[1]}"
            print(f"[STATUS] Client: {client_ip}; Server: {server_ip}")

    def client_disconnected(self, client):
        try:
            client_ip = f"{client.getpeername()[0]}:{client.getpeername()[1]}"
            print(f"Client {client_ip} got disconnected.")
        except OSError:
            pass  # The client is already disconnected
        self.clients.remove(client)
        client.close()