from socket import *

calc = Calculator()

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
        expression = request.decode('utf-8')
        return expression
    
    def sendResponse(self, connectionSocket, result):
        connectionSocket.send(str(result).encode('utf-8'))
        connectionSocket.close()

    def handleClient(self, connectionSocket):
        expression = self.getRequest(connectionSocket)

        args = expression.split()
        result = 0

        if args[0] == 'ADD':
            result = float(args[1]) + float(args[2])
        elif args[0] == 'SUB':
            result = float(args[1]) - float(args[2])

        self.sendResponse(connectionSocket, result)

    def close(self):
        self.serverSocket.close()


server = TcpServer()

while True:
    connectionSocket = server.acceptConnection()
    server.handleClient(connectionSocket)
