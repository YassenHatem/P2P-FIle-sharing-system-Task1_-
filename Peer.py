import pickle
from socket import *
from Constant import *
from threading import Thread


class Client:
    def __init__(self):
        self.sersoc = socket(AF_INET, SOCK_STREAM)
        self.sersoc.connect((HOST, PORT))
        self.Menu = pickle.loads(self.sersoc.recv(1024))
        print(self.Menu)

    def Listen(self,port):
        self.host = 'localhost'
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(MaxConnections - 1)
        while True:
            (conn, addr)=self.sock.accept()
            FileName = pickle.loads(conn.recv(1024))
            MyFile = open(FileName,'r').read()
            conn.send(pickle.dumps(MyFile))


    def ActC(self):
        while True:
            choice = input()
            if choice == REGISTER:
                ID = self.Register()
                print("You successfully registered your ID is ", ID[0], "and your port is ", ID[1])
                print(self.Menu)
                Thread(target=C.Listen, args=(ID[1],)).start()
                continue

            elif choice == SHARE:
                ID = input("Enter your ID please : ")
                FileName = input("Enter file name : ")
                Result = self.Share(ID, FileName)
                if (Result == OK):
                    print("You successfully shared this file ", FileName)
                else:
                    print(Result)
                    print("Sorry try again")
                print(self.Menu)
                continue
            elif choice == SEARCH:
                id = input("Enter your ID : ")
                FileName = input("Enter file name you need please : ")
                Peers = self.Search(FileName)
                if len(Peers)>0:
                    print("The Peers you can connect for him : \n")
                    print("ID\tPort\n")
                    for i in range(0, len(Peers)):
                        print(Peers[i])
                    PeerPort = input("Enter Port number you need to connect on it : ")
                    self.sersoc.shutdown(True)
                    self.sersoc = socket(AF_INET, SOCK_STREAM)
                    self.sersoc.connect((HOST, int(PeerPort)))
                    self.sersoc.send(pickle.dumps(FileName))
                    data = pickle.loads(self.sersoc.recv(1024))
                    print(data)
                    f = open('new_'+FileName, 'w')
                    f.write(data)
                    f.close()
                    self.sersoc.shutdown(True)
                    self.sersoc = socket(AF_INET, SOCK_STREAM)
                    self.sersoc.connect((HOST, PORT))
                    print(pickle.loads(C.sersoc.recv(1024)))
                else:
                    print("This file dosn't exist")
                continue
            else:
                self.sersoc.send(pickle.dumps([STOP]))
                break

    def Register(self):
        self.sersoc.send(pickle.dumps([REGISTER]))
        return pickle.loads(self.sersoc.recv(1024))
    def Share(self,ID,FileName):
        self.sersoc.send(pickle.dumps([SHARE,FileName,ID]))
        return pickle.loads(self.sersoc.recv(1024))
    def Search(self,FileName):
        self.sersoc.send(pickle.dumps([SEARCH,FileName]))
        return pickle.loads(self.sersoc.recv(1024))


C = Client()
Thread(target=C.ActC,args=()).start()
