from esqueleto import *

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