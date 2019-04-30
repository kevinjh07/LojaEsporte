class Produto(object):

    def __init__(self):
        pass

    def __init__(self, nome, preco, descricao, categoria):
        self.nome = nome
        self.preco = preco
        self.descricao = descricao
        self.categoria = categoria


    def to_csv(self):
        return '%s,%s,%s,%s' % (self.nome, self.preco, self.descricao, self.categoria)


         