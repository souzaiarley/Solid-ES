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
        return operation.execute(a, b)