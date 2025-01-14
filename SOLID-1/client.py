from socket import *

serverPort = 12000

class TcpClient:
    def __init__(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect(('localhost', serverPort))

    def sendRequest(self, req):
        self.clientSocket.send(req)

    def getResponse(self):
        resp = self.clientSocket.recv(1024)
        return resp
    
    def close(self):
        self.clientSocket.close()
