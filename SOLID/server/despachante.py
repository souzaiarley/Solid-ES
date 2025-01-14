from esqueleto import *

# Dicionário para armazenar as operações possíveis
operations = {
    'ADD': AddEsqueleto(),
    'SUB': SubEsqueleto(),
    'PADD': AddEsqueletoPrint(),
    'PSUB': SubEsqueletoPrint(),
    'SIN': SinEsqueleto()
}

class Despachante:
    def invoke(self, request):
        request = request.decode('utf-8')
        params = request.split(' ')
        operation = params[0]
        args = params[1:]

        return operations[operation].handleOperation(args)