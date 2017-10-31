import pickle
from socket import *
from Constant import *
from _thread import *


class Server:
    def __init__(self, port=PORT):
        self.host = 'localhost'
        self.port = port
        self.setOfPeers = {}
        print("[*] Starts Listening on", self.host, ":", self.port)
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(MaxConnections)
        while True:
            (conn, addr) = self.sock.accept()
            print("[*] Got a connection from ", addr[0], ":", addr[1])
            conn.send(pickle.dumps("Hello welcome to P2P File sharing system.Choose the function do you need\n"
                                   "Press 1. to Register\nPress 2. to Share files\n"
                                   "Press 3. to Search for a file\nPress 5. to Exit\n"))
            start_new_thread(self.run,(conn,))

    def Register(self):
        ID = PeerIDs[0]
        PeerIDs.pop(0)
        Port = PeerPorts[ID-1]
        self.setOfPeers[ID - 1] = []
        return [ID, Port]

    def Share(self, ID, Data):
        self.setOfPeers[int(ID) - 1].append(Data)
        return OK

    def Search(self, FileName):
        Peers = []
        for i in range(0,len(self.setOfPeers)):
            if FileName in self.setOfPeers[i]:
                Peers.append((i + 1, PeerPorts[i]))
        return Peers

    def run(self,conn,):
        while True:

            try:
                data = conn.recv(1024)
                if not data:
                    break
                request = pickle.loads(data)
                print("[*] request after Unwrap", request)
                if request[0] == REGISTER:
                    conn.send(pickle.dumps(self.Register()))

                elif request[0] == SHARE:
                    ID = request[2]
                    data = request[1]
                    conn.send(pickle.dumps(self.Share(ID, data)))

                elif request[0] == SEARCH:
                    FileName = request[1]
                    conn.send(pickle.dumps(self.Search(FileName)))

                elif request[0] == STOP:
                    break

            except EOFError:
                break

        conn.close()


server = Server(PORT)
