class Produto(object):

    def __init__(self):
        pass

    def __init__(self, id, nome, preco, descricao, categoria):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.descricao = descricao
        self.categoria = categoria


    def to_csv(self):
        return '%s,%s,%s,%s' % (self.nome, self.preco, self.descricao, self.categoria)


         