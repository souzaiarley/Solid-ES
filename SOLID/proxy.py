from client import TcpClient

class Proxy:
    def __init__(self):
        self.client = TcpClient()

    def sendRequest(self, operation, a, b):
        expression = f'{operation} {a} {b}'
        req = expression.encode('utf-8')
        self.client.sendRequest(req)

    def getResponse(self):
        resp = self.client.getResponse()
        result = resp.decode('utf-8')
        return result
    
    def close(self):
        self.client.close()
