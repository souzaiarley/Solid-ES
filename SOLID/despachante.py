from esqueleto import *

esqueleto = Esqueleto()

class Despachante:
    def invoke(self, request):
        request = request.decode('utf-8')
        params = request.split(' ')

        if params[0] == 'ADD':
            return esqueleto.sum(params[1], params[2])
        
        elif params[0] == 'SUB':
            return esqueleto.sub(params[1], params[2])
