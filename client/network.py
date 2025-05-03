import socket
import time
import json
import msgpack

def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip
server_ip = "195.94.145.91" #"127.0.0.1"#"82.145.118.35" 

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.setblocking(False)
        self.server = server_ip
        self.port = 5555
        self.addr = (self.server, self.port)
        #self.id = self.connect()
        self.pos = (0, 0)
    def start(self):
        print("bakaddd")
        #self.id = self.connect()
        #print("id: ", self.id)
    def stop(self):
        pass

    def connect(self):
        '''
        try:
            self.client.connect(self.addr)
            return msgpack.unpackb(self.client.recv(8192), raw=False) #self.client.recv(8192).decode()
        except:
            pass
        '''
    def setPos(self, x, y):
        self.pos = (x, y)

    def changePos(self, dx, dy):
        self.pos = (self.pos[0]+dx, self.pos[1]+dy)

    def send(self, data):
        """Send JSON data to the server and receive a response."""
        try:
            if isinstance(data, (dict, list)):  # Ensure it's JSON serializable
                data = msgpack.packb(data)#json.dumps(data)
            else:
                print("data isn't serializable")
                return
            #self.client.sendall(data)  # Send encoded data
            self.client.sendto(data, self.addr)
            data, _ = self.client.recvfrom(16384)
            response = msgpack.unpackb(data, raw=False) # Receive response
            return response  # Decode JSON response
        except (socket.error, msgpack.ExtraData, msgpack.UnpackException, msgpack.FormatError, ValueError) as e:
            print(f"Error: {e}")
            return None  # Return None if an error occurs



if __name__ == "__main__":
    network = Network()
    network.connect()
    print("starting")
    i = 0
    while True:
        res = network.send(f"baka yaroooooooo {i}")
        time.sleep(5.5)
        print(res)
        i += 1

