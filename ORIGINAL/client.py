from socket import *

serverPort = 12000

class TcpClient:
    def __init__(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect(('localhost', serverPort))

    def sendRequest(self, operation, a, b):
        expression = f'{operation} {a} {b}'
        req = expression.encode('utf-8')
        self.clientSocket.send(req)

    def getResponse(self):
        resp = self.clientSocket.recv(1024)
        result = resp.decode('utf-8')
        return result
    
    def close(self):
        self.clientSocket.close()
