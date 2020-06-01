cont = 0

def incrementarContador():
    global cont
    cont +=1
    return "%d" %cont

class Nodo():
    pass

class Null(Nodo):
    def __init__(self):
        self.type = 'void'

    def imprimir(self, ident):
        print(id + "nodo nulo")

