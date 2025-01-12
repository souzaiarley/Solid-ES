# Princípios SOLID

Os princípios **SOLID** são um conjunto de diretrizes para o desenvolvimento de software que visam criar sistemas mais flexíveis, robustos e fáceis de manter. Criados por Robert C. Martin, esses princípios ajudam a estruturar o código de forma que ele seja menos propenso a erros e mais adaptável a mudanças futuras. Ao aplicar esses conceitos, os desenvolvedores conseguem criar sistemas mais modulares e reutilizáveis, favorecendo boas práticas de programação.

O intuito deste trabalho é apresentar aplicações simples dos princípios SOLID em código.

## Single Responsibility Principle

Esse princípio busca garantir que cada classe ou módulo no código tenha uma única responsabilidade claramente definida, o que torna o software mais fácil de entender, manter e modificar. Quando uma classe possui múltiplas responsabilidades, qualquer mudança em uma delas pode afetar as outras, aumentando a complexidade e o risco de introduzir erros no sistema. Nesse caso, a abordagem ideal é indentificar e separar as diferentes responsabilidades que a classe possui e distribuí-las em classes menores.

### Exemplo de aplicação

O código python abaixo apresenta a implementação de uma classe `TcpClient` para um cliente TCP de um serviço de calculadora.

``` python
class TcpClient:
    def __init__(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect(('localhost', serverPort))

    def sendRequest(self, operation, a, b):
        # Monta a requisição com os parâmetros recebidos
        expression = f'{operation} {a} {b}'
        # Codifica
        req = expression.encode('utf-8')
        # Envia a requisição
        self.clientSocket.send(req)

    def getResponse(self):
        # Recebe a resposta
        resp = self.clientSocket.recv(1024)
        # Decodifica
        result = resp.decode('utf-8')
        # Retorna a resposta como string
        return result
    
    def close(self):
        self.clientSocket.close()
```

Perceba que a classe em questão possui mais responsabilidades do que apenas enviar requisições e receber respostas. Ela é também responsável por receber os parâmetros de operador e operandos, montar a requisição e codificá-la em bytes utilizando UTF-8 para então, enviar a requisição ao servidor.

No caminho oposto também há uma resposabilidade adicional: O cliente deve decodificar a resposta em bytes para então retorná-la.

Nesse contexto, seria interessante dividir as reponsabilidades de envio/resposta e codificação/decodificação entre as classes `TcpClient` e uma nova classe chamada `Proxy`. No contexto de sistemas distribuídos, um proxy é uma entidade que atua como intermediário entre o cliente e o serviço.  Ele encapsula a comunicação, delegando a responsabilidade de fazer as requisições (nesse caso o cliente) e processar as respostas para outro objeto ou componente.

Abaixo podemos ver o código refatorado:

#### Proxy

O proxy é responsável pela montagem da requisição, codificação e decodificação de requisições e respostas. Perceba que a classe `Proxy` faz a comunicação com a classe `TcpClient`.

``` python
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
```

#### Cliente TCP

Agora o cliente possui a responsabilidade única de fazer o envio e recepção das requisições e respostas.

``` python
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
```

### Lado Servidor

No lado do servidor a situação é semelhante:

``` python
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
```

A classe `TcpServer` preocupa-se em decodificar e codificar requisições e respostas, além de recebê-las e enviá-las. O servidor ainda é responsável por analisar os parâmetros da requisição (a fim de determinar a operação a ser feita), conversões de valores e realizar os cálculos necessários.

Essa abordagem mostra-se como uma grande violação do princípio de responsabilidade única, dificultando a manutenibilidade e flexibilidade do servidor.

Vamos dividir essas responsabilidades entre as seguintes classes:

- `TcpServer`: Recebe requisições e envia as respostas
- `Despachante`: Recebe a requisição, decodifica e invoca o método correspondente da classe Esqueleto, passando os parâmetros necessários. Recebe o retorno do esqueleto e o retorna para o Servidor TCP para ser
enviado ao cliente.
- `Esqueleto`: Recebe os parâmetros , faz as conversões necessárias e chama o método apropriado da classe Calculator. Recebe a resposta da calculadora, codifica e retorna para o despachante.
- `Calculator`: Realmente implementa as funções de calculadora.

Código refatorado:

#### Servidor

``` python
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
```

#### Despachante

``` python
class Despachante:
    def invoke(self, request):
        request = request.decode('utf-8')
        params = request.split(' ')

        if params[0] == 'ADD':
            return esqueleto.sum(params[1], params[2])
        
        elif params[0] == 'SUB':
            return esqueleto.sub(params[1], params[2])
```

#### Esqueleto

``` python
class Esqueleto:
    def sum(self, a, b):
        a = float(a)
        b = float(b)
        result = calc.add(a, b)
        response = str(result).encode('utf-8')
        return response
    
    def sub(self, a, b):
        a = float(a)
        b = float(b)
        result = calc.subtract(a, b)
        response = str(result).encode('utf-8')
        return response
```

#### Calculadora

``` python
class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b
```

Essa abordagem torna o sistema mais modular, permitindo que alterações em uma funcionalidade (como a lógica de cálculo ou o formato das mensagens) sejam feitas sem impactar outras partes do código. Além disso, facilita a expansão do sistema, como a adição de novos operadores ou mudanças no protocolo de comunicação.
