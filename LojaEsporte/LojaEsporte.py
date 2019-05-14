import wpf

from System.Windows import Application, Window, MessageBox
from TelaCadastroProduto import TelaCadastroProduto
from TelaCadastroPessoa import TelaCadastroPessoa

class MyWindow(Window):

    def __init__(self):
        wpf.LoadComponent(self, 'LojaEsporte.xaml')


    def cadastro_produto(self, sender, e):
        tela = TelaCadastroProduto()
        tela.ShowDialog()
        pass


    def cadastro_pessoa(self, sender, e):
        tela = TelaCadastroPessoa()
        tela.ShowDialog()
        pass
    

    def atualizar(self, sender, e):
        self.listar()
        pass


if __name__ == '__main__':
    Application().Run(MyWindow())
