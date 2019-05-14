class Pessoa(object):

    def __init__(self):
        pass

    def __init__(self, nome, email, cpf):
        self.nome = nome
        self.email = email
        self.cpf = cpf


    def to_csv(self):
        return '%s,%s,%s' % (self.nome, self.email, self.cpf)


         