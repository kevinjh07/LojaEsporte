import wpf

from System.Windows import Application, Window, MessageBox
from TelaCadastroProduto import TelaCadastroProduto
from Produto import Produto

class MyWindow(Window):
    NOME_ARQUIVO = 'produtos.csv'
    READ_FILE = 'r'
    produtos_map = {
        0: 'Vestuario',
        1: 'Calcados',
        2: 'Acessorios',
        3: 'Equipamentos'
    }

    def __init__(self):
        wpf.LoadComponent(self, 'LojaEsporte.xaml')
        self.listar()


    def cadastro(self, sender, e):
        tela = TelaCadastroProduto()
        tela.ShowDialog()
        pass

    
    def listar(self):
        produtos = []
        try:
            file = open(self.NOME_ARQUIVO, self.READ_FILE)
            for f in file:
                split = f.split(',')
                nome_produto = self.produtos_map[int(split[3].replace('\n', ''))]
                produto = Produto(split[0], split[1], split[2], nome_produto)
                produtos.append(produto)
                
            
            file.close()
        except IOError as error:
            print(error)
            MessageBox.Show('Ocorreu um erro ao tentar ler o arquivo.\n{0}'.format(error.strerror))

        self.lvProdutos.ItemsSource = produtos

    
    def atualizar(self, sender, e):
        self.listar()
        pass


if __name__ == '__main__':
    Application().Run(MyWindow())
