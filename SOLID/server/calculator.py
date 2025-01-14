from abc import ABC, abstractmethod
from math import sin

# Classe abstrata para operações matemáticas simples entre dois operandos
class Operation(ABC):
    @abstractmethod
    def execute(self, a, b):
        pass

# Classes concretas para operações matemáticas simples
class AddOperation(Operation):
    def execute(self, a, b):
        return a + b

class SubOperation(Operation):
    def execute(self, a, b):
        return a - b

# Classe abstrata para operações trigonométricas
class TrigonometricOperation(ABC):
    @abstractmethod
    def execute(self, a):
        pass

# Classes concretas para operações trigonométricas
class SinOperation(TrigonometricOperation):
    def execute(self, a):
        return sin(a)

# Classe genérica que utiliza as operações
class Calculator:
    def calculate(self, operation: Operation, a, b):
        result = operation.execute(a, b)
        return result

# Classe para calculadora científica
class scientificCalculator(Calculator):
    # Método para cálculos de operações trigonométricas
    def calculateTrigonometry(self, operation: TrigonometricOperation, a):
        result = operation.execute(a)
        return result

# Classe para calculadora de impressão
class PrintingCalculator(Calculator):
    def printResult(self, result, operationType, a, b):
        return f"{operationType}({a}, {b}) = {result}" 
