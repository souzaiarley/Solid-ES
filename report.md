# Princípios SOLID

Os princípios **SOLID** são um conjunto de diretrizes para o desenvolvimento de software que visam criar sistemas mais flexíveis, robustos e fáceis de manter. Criados por Robert C. Martin, esses princípios ajudam a estruturar o código de forma que ele seja menos propenso a erros e mais adaptável a mudanças futuras. Ao aplicar esses conceitos, os desenvolvedores conseguem criar sistemas mais modulares e reutilizáveis, favorecendo boas práticas de programação.

O intuito deste trabalho é apresentar aplicações simples dos princípios SOLID em código.

## Single Responsibility Principle (SRP)

Esse princípio busca garantir que cada classe ou módulo no código tenha uma única responsabilidade claramente definida, o que torna o software mais fácil de entender, manter e modificar. Quando uma classe possui múltiplas responsabilidades, qualquer mudança em uma delas pode afetar as outras, aumentando a complexidade e o risco de introduzir erros no sistema. Nesse caso, a abordagem ideal é indentificar e separar as diferentes responsabilidades que a classe possui e distribuí-las em classes menores.

### Exemplo de aplicação do SRP (cliente)

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

### Exemplo de aplicação do SRP (servidor)

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

## Open-Closed Principle (OCP)

> "Objetos ou entidades devem estar abertos para extensão, mas fechados para modificação".

Isto é o que o princípio Aberto-Fechado prega. Em outras palavras, quando novos comportamentos e recursos precisam ser adicionados no software, devemos estender e não alterar o código fonte original.

Se um código existente precisa ser modificado sempre que novas funcionalidades são adicionadas, há um risco maior de introduzir bugs acidentais. Alterar uma funcionalidade já implementada pode afetar outras partes do sistema, especialmente em projetos grandes.

Uma abordagem ideal para contornar esses riscos é adotar práticas e padrões de design que promovam a extensibilidade do sistema sem modificar o código existente, como o uso de abstrações ou interfaces.

### Exemplo de aplicação do OCP

Como podemos notar, o nosso serviço de calculadora oferece apenas as operações de adição e subtração:

```python
class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b
```

Para adicionarmos a operação de multiplicação, por exemplo, seria necessário modificar o código da classe, adicionando uma função adicional.

O mesmo ocorreria para a classe `Esqueleto`, que deve chamar os métodos da calculadora:

```python
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

Por fim, também seria necessário expandir a lógica da estrutura condicional da classe `Despachante`:

```python
class Despachante:
    def invoke(self, request):
        request = request.decode('utf-8')
        params = request.split(' ')

        if params[0] == 'ADD':
            return esqueleto.sum(params[1], params[2])
        
        elif params[0] == 'SUB':
            return esqueleto.sub(params[1], params[2])
```

Todas essas alterações ferem o princípio Aberto-Fechado, pois estaríamos modificando as classes já implementadas. Devemos adotar uma abordagem que contorne essa violação aplicando técnicas de POO.

#### Abstração da calculadora

Para permitir a adição de novas operações da calculadora, devemos remover a implementação das operações matemáticas de dentro da classe. A estratégia é permitir que a classe `Calculator` receba operações de forma genérica e calcule o resultado para os operandos, sem precisar se preocupar com qual operação específica está sendo realizada.

Para isso, criaremos uma classe abstrada `Operation`, que possui seu único método abstrato `execute`.

Para criar as operações específicas, devemos criar uma classe para cada operação, sendo que as classes criadas devem ser descendentes da classe abstrata (herança). Dessa forma, ao criarmos as classes específicas, será necessário implementar o método específico de execução da operação matemática.

Por fim, para realizar operações matemáticas, basta apenas chamar o método `calculate` da classe `Calculator`, passando os operandos e uma instância de alguma classe de operação. Perceba que o parâmetro é do tipo `Operator`, aceitando qualquer objeto que seja do tipo da classe abstrata, o que permite que a calculadora realize operações de forma genérica.

Abaixo temos o resultado dessa refatoração:

```python
# Classe abstrata para operações
class Operation(ABC):
    @abstractmethod
    def execute(self, a, b):
        pass

# Classes concretas para operações
class AddOperation(Operation):
    def execute(self, a, b):
        return a + b

class SubOperation(Operation):
    def execute(self, a, b):
        return a - b

# Classe que utiliza as operações
class Calculator:
    def calculate(self, operation: Operation, a, b):
        return operation.execute(a, b)
```

#### Abstração do Esqueleto

Podemos realizar um processo semelhante para a classe do Esqueleto, devemos apenas transformar a classe `Esqueleto` em uma classe abstrata, que possui um método abstrato `callCalculator` e os métodos de conversão, codificação e manuseamento dos parâmetros.

O método `callCalculator` é o responsável por chamar o método `calculate` da classe `Calculator`, passando apenas os operandos e a instância do tipo `Operation` referente ao tipo da operação desejada. Cada implementação específica da classe abstrata possui sua implementação específica para este método.

Código refatorado:

```python
# Abstração para esqueletos
class Esqueleto(ABC):
    @abstractmethod
    def callCalculator(self, a, b):
        pass

    def convert(self, a: str, b: str):
        return float(a), float(b)

    def encode(self, response):
        return str(response).encode('utf-8')
    
    def handleOperation(self, a, b):
        a, b = self.convert(a, b)
        result = self.callCalculator(a, b)
        response = self.encode(result)
        return response

# Implementações de esqueletos para cada operação:

# Esqueleto para adição
class AddEsqueleto(Esqueleto):
    def callCalculator(self, a, b):
        result = calc.calculate(AddOperation(), a, b)
        return result

# Esqueleto para subtração
class SubEsqueleto(Esqueleto):
    def callCalculator(self, a, b):
        result = calc.calculate(SubOperation(), a, b)
        return result
```

#### Mudanças no despachante

A classe despachante, como citado anteriormente, é responsável por receber a requisição, decodificar e invocar o método correspondente da classe Esqueleto.

Para que não seja necessário expandir a lógica de condicional da classe despachante, é interessante que ela tenha a capacidade de chamar de forma genérica o método `handleOperation` do esqueleto, sem se preocupar em saber qual o tipo específico de esqueleto está sendo chamado.

Podemos fazer isso mapeando os parâmetros de operação para os tipos de esqueleto a serem chamados. Faremos isso com o auxílio de um dicionário. Dessa maneira, o despachante decodifica a requisição, obtém o primeiro parâmetro (de operação), consulta no dicionário e chama o método do esqueleto correspondente.

Para adicionarmos operações no despachante, bastaria apenas adicionarmos o elemento chave:valor no dicionário, sem precisar modificar o funcionamento da classe.

Abaixo temos o código refatorado:

```python
# Dicionário para armazenar as operações possíveis
operations = {
    'ADD': AddEsqueleto(),
    'SUB': SubEsqueleto(),
}

class Despachante:
    def invoke(self, request):
        request = request.decode('utf-8')
        params = request.split(' ')
        operation = params[0]

        return operations[operation].handleOperation(params[1], params[2])
```

Com essas modificações realizadas, torna-se mais fácil adicionar ou remover operações possíveis do serviço.

Para adicionar, devemos:

- Adicionar mais uma implementação da classe `Operation`
- Adicionar mais uma implementação da classe `Esqueleto`
- Registrar a nova operação no dicionário de operações.

## Liskov Substitution Principle (LSP) e Interface Segregation Principle (ISP)

O Princípio de Substituição de Liskov (LSP) e o Princípio de Segregação de Interfaces (ISP) são dois dos cinco princípios SOLID que visam garantir que as classes sejam fáceis de usar e de estender.

O LSP estabelece que objetos de uma superclasse devem ser substituíveis por objetos de suas subclasses sem que a funcionalidade do programa seja alterada. Em outras palavras, uma classe derivada deve ser capaz de substituir sua classe base sem quebrar o comportamento do programa.

O ISP, por sua vez, prega que uma classe não deve ser forçada a implementar interfaces que ela não utiliza. Em vez disso, as interfaces devem ser segregadas em interfaces menores e mais específicas, de modo que as classes possam implementar apenas o que precisam.

### Exemplo de aplicação do LSP e ISP

Desejamos adicionar uma nova funcionalidade ao nosso serviço de calculadora: a impressão de operações e seus resultados, tentando simular uma calculadora de impressão.

Para isso criaremos um método `printResult`, que imprime na tela a operação realizada e o resultado obtido.
Para representar essa impressão, o método deve retornar uma `string`.

Aplicando essas alterações, obtemos o seguinte resultado:
```python
class Calculator:
    def calculate(self, operation: Operation, a, b):
        operationType = operation.__class__.__name__
        result = operation.execute(a, b)
        return self.printResult(result, operationType, a, b)

    def printResult(self, result, operationType, a, b):
        return f"{operationType}({a}, {b}) = {result}"
```

Desejamos também especificar tipos de calculadora (como calculadora simples, calculadora científica, calculadora financeira, etc.).

Para isso, criaremos a classe `SimpleCalculator`.

```python
class SimpleCalculator(Calculator):
    def printResult(self, result, operationType, a, b):
        raise Exception("SimpleCalculator does not support printResult")
```

A `SimpleCalculator` é um tipo de calculadora criada para representar uma calculadora básica que implementa somente as operações básicas. Logo, ela não oferece suporte à impressão.
Para representar esse comportamento, o método `printResult` da classe `SimpleCalculator` foi sobrecarregado para lançar uma exceção, indicando que a operação não é suportada.

No entanto, essa abordagem viola o princípio de substituição de Liskov, pois a classe `SimpleCalculator` não é substituível pela classe `Calculator`: para as chamadas do método `printResult`, espera-se que o retorno seja a string da impressão, e não uma exceção.
Ademais, o princípio de segregação de interfaces também é violado, pois a classe `SimpleCalculator` é forçada a implementar um método que não é utilizado.

Para contornar essas violações, devemos refatorar o código de forma que a classe `SimpleCalculator` não seja forçada a implementar o método `printResult` e que a classe `Calculator` possa ser substituída por suas subclasses sem quebrar o comportamento do programa.

Para isso, criaremos a classe `PrintingCalculator`, que é uma subclasse de `Calculator` que implementa o método `printResult`:

#### Calculadora de Impressão

```python
class PrintingCalculator(Calculator):
    def printResult(self, result, operationType, a, b):
        return f"{operationType}({a}, {b}) = {result}"
```

#### Calculadora Genérica

```python
class Calculator:
    def calculate(self, operation: Operation, a, b):
        result = operation.execute(a, b)
        return result
```

#### Calculadora Simples
Simplesmente herda da classe `Calculator`.

```python
class SimpleCalculator(Calculator):
    pass
```
