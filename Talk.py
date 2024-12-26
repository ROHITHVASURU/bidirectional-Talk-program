import sys
from TalkClient import TalkClient
from TalkServer import TalkServer

class Talk:
    def __init__(self):
        self.host = "localhost"
        self.port = 12987
        self.client = None
        self.server = None

    def run(self):
        if len(sys.argv) < 2 or sys.argv[1] == "-help":
            self.display_help()
            return

        mode = sys.argv[1]
        if mode == "-h":
            self.start_client_mode()
        elif mode == "-s":
            self.start_server_mode()
        elif mode == "-a":
            self.start_auto_mode()
        else:
            print("Unknown mode. Use -help for help.")

    def display_help(self):
        print("Usage:")
        print("Talk -h [hostname] [-p port]")
        print("Talk -s [-p port]")
        print("Talk -a [hostname] [-p port]")
        print("Talk --help")


    def start_client_mode(self):
        self.setup_host_port()
        try:
            self.client = TalkClient(self.host, self.port)
            self.client.connect()
        except ConnectionRefusedError:
            print("Unable to connect to the server at {}:{}.".format(self.host, self.port))
            print("Make sure the server is running and that you have the correct address and port.")

    def start_server_mode(self):
        self.setup_host_port()
        self.server = TalkServer(self.port)
        self.server.start()
        
    def start_auto_mode(self):
        self.setup_host_port()
        try:
            self.client = TalkClient(self.host, self.port)
            self.client.connect()
        except ConnectionRefusedError:
            print("Starting as server...")
            self.server = TalkServer(self.port)
            self.server.start()

    def setup_host_port(self):
        if len(sys.argv) > 2:
            if sys.argv[2].startswith('-p'):
                self.port = int(sys.argv[3])
            else:
                self.host = sys.argv[2]
                if len(sys.argv) > 3 and sys.argv[3] == "-p":
                    self.port = int(sys.argv[4])


if __name__ == "__main__":
    chat_app = Talk()
    chat_app.run()
