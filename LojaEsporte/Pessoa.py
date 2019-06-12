class Pessoa(object):

    def __init__(self):
        pass

    def __init__(self, id, nome, email, cpf):
        self.id = id
        self.nome = nome
        self.email = email
        self.cpf = cpf


    def to_csv(self):
        return '%s,%s,%s' % (self.nome, self.email, self.cpf)


         