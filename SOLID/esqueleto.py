from calculator import *

calc = Calculator()

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
