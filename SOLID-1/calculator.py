from abc import ABC, abstractmethod

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
        result = operation.execute(a, b)
        return result

class scientificCalculator(Calculator):
    # Método para cálculos de operações trigonométricas
    def calculateTrigonometry(self, operation: TrigonometricOperation, a):
        result = operation.execute(a)
        return result

class PrintingCalculator(Calculator):
    def printResult(self, result, operationType, a, b):
        return f"{operationType}({a}, {b}) = {result}"