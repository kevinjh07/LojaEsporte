import wpf

from System.Windows import Application, Window, MessageBox
from TelaCadastroProduto import TelaCadastroProduto
from Produto import Produto

class MyWindow(Window):

    def __init__(self):
        wpf.LoadComponent(self, 'LojaEsporte.xaml')


    def cadastro(self, sender, e):
        tela = TelaCadastroProduto()
        tela.ShowDialog()
        pass
    

    def atualizar(self, sender, e):
        self.listar()
        pass


if __name__ == '__main__':
    Application().Run(MyWindow())
