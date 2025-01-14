from calculator import *

# Abstração para esqueletos
class Esqueleto(ABC):
    @abstractmethod
    def callCalculator(self, args: list):
        pass

    def convert(self, x: str):
        return float(x)

    def encode(self, response):
        return str(response).encode('utf-8')
    
    @abstractmethod
    def handleOperation(self, args: list):
        pass

# Implementação de um esqueleto para operações simples (+, -) envolvendo dois operandos
class SimpleEsqueleto(Esqueleto):
    @ abstractmethod
    def callCalculator(self, args: list):
        pass

    def handleOperation(self, args:list):
        a = args[0]
        b = args[1]
        a = self.convert(a)
        b = self.convert(b)
        result = self.callCalculator([a, b])
        response = self.encode(result)
        return response

# Implementação de um esqueleto para operações trigonométricas envolvendo um operando
class TrigEsqueleto(Esqueleto):
    @ abstractmethod
    def callCalculator(self, args: list):
        pass

    def handleOperation(self, args:list):
        a = args[0]
        a = self.convert(a)
        result = self.callCalculator([a])
        response = self.encode(result)
        return response

# Implementações de esqueletos para cada operação:

# Esqueleto para adição
class AddEsqueleto(SimpleEsqueleto):
    def callCalculator(self, args: list):
        a = args[0]
        b = args[1]
        calc = Calculator()
        result = calc.calculate(AddOperation(), a, b)
        return result
    
# Esqueleto para subtração
class SubEsqueleto(SimpleEsqueleto):
    def callCalculator(self, args: list):
        a = args[0]
        b = args[1]
        calc = Calculator()
        result = calc.calculate(SubOperation(), a, b)
        return result

# Esqueleto para adição (print)
class AddEsqueletoPrint(SimpleEsqueleto):
    def callCalculator(self, args: list):
        a = args[0]
        b = args[1]
        calc = PrintingCalculator()
        result = calc.calculate(AddOperation(), a, b)
        output = calc.printResult(result, AddOperation.__name__, a, b)
        return output

# Esqueleto para subtração (print)
class SubEsqueletoPrint(SimpleEsqueleto):
    def callCalculator(self, args: list):
        a = args[0]
        b = args[1]
        calc = PrintingCalculator()
        result = calc.calculate(SubOperation(), a, b)
        output = calc.printResult(result, SubOperation.__name__, a, b)
        return output
    
class SinEsqueleto(TrigEsqueleto):
    def callCalculator(self, args: list):
        a = args[0]
        calc =  scientificCalculator()
        result = calc.calculateTrigonometry(SinOperation(), a)
        return result