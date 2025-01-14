from socket import *
from despachante import Despachante

despachante = Despachante()

class TcpServer:
    def __init__(self):
        self.serverPort = 12000
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind(('', self.serverPort))
        self.serverSocket.listen(100)
        print(f'Server running on port {self.serverPort}')
    
    def acceptConnection(self):
        connectionSocket, clientAddr = self.serverSocket.accept()
        return connectionSocket

    def getRequest(self, connectionSocket):
        request = connectionSocket.recv(1024)
        return request
    
    def sendResponse(self, connectionSocket, response):
        connectionSocket.send(response)
        connectionSocket.close()

    def handleClient(self, connectionSocket):
        request = self.getRequest(connectionSocket)

        response = despachante.invoke(request)
        self.sendResponse(connectionSocket, response)

    def close(self):
        self.serverSocket.close()


server = TcpServer()

while True:
    connectionSocket = server.acceptConnection()
    server.handleClient(connectionSocket)
