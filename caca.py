class caca:
    def __init__(self, id, ataque, numeros):
        self.id = id
        self.sadsad = ataque
        self.numero = numeros

    @property
    def ataque(self):
        total = 0
        for i in self.numero:
            total += i
        return total + self.sadsad + self.id


a = caca(1,2,[1,2,3])
b = caca(1,3,[45,3,2])
c = caca(1000,1000,[1,1,1])

lista = [a,b,c]
lista.sort(key =lambda x: x.ataque)
print([x.ataque for x in lista])
