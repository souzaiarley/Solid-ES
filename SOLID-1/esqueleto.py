from calculator import *

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
        calc = Calculator()
        result = calc.calculate(AddOperation(), a, b)
        return result

# Esqueleto para subtração
class SubEsqueleto(Esqueleto):
    def callCalculator(self, a, b):
        calc = Calculator()
        result = calc.calculate(SubOperation(), a, b)
        return result

# Esqueleto para adição (com print)
class AddEsqueletoPrint(Esqueleto):
    def callCalculator(self, a, b):
        calc = PrintingCalculator()
        result = calc.calculate(AddOperation(), a, b)
        output = calc.printResult(result, AddOperation.__name__, a, b)
        return output
    
# Esqueleto para subtração (com print)
class SubEsqueletoPrint(Esqueleto):
    def callCalculator(self, a, b):
        calc = PrintingCalculator()
        result = calc.calculate(SubOperation(), a, b)
        output = calc.printResult(result, SubOperation.__name__, a, b)
        return output