from client import TcpClient

class Proxy:
    def __init__(self):
        self.client = TcpClient()

    def sendRequest(self, operation, args: list):
        expression = f'{operation} {" ".join(map(str, args))}'
        req = expression.encode('utf-8')
        self.client.sendRequest(req)

    def getResponse(self):
        resp = self.client.getResponse()
        result = resp.decode('utf-8')
        return result
    
    def close(self):
        self.client.close()
