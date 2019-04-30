import wpf
from Produto import Produto
from System.Windows import Window, MessageBox

class TelaCadastroProduto(Window):
    NOME_ARQUIVO = 'produtos.csv'
    APPEND_TO_FILE = 'a'

    def __init__(self):
        wpf.LoadComponent(self, 'TelaCadastroProduto.xaml')


    def limpar(self, sender, e):
        self.txtNome.Text = '';
        self.txtPreco.Text = '';
        self.txtDescricao.Text = '';
        self.cbCategoria.SelectedIndex = -1
        self.txtNome.Focus()
        pass

    
    def salvar(self, sender, e):
        produto = Produto(self.txtNome.Text, self.txtPreco.Text, 
                          self.txtDescricao.Text, self.cbCategoria.SelectedIndex);
        try:
            self.validar_produto(produto)
            file = open(self.NOME_ARQUIVO, self.APPEND_TO_FILE)
            file.write(produto.to_csv() + '\n')
            file.flush()
            file.close()
            self.limpar(sender, e)
            MessageBox.Show('Produto salvo!')
        except Exception as error:
            MessageBox.Show(error.message)
            pass

        pass


    def validar_produto(self, produto):
        result = None
        if (len(produto.nome.strip()) == 0):
            raise Exception('Informe um nome!');

        if (len(produto.preco.strip()) == 0):
            raise Exception('Informe um preco!\n');

        if (len(produto.descricao.strip()) == 0):
            raise Exception('Informe uma descricao!');

        if (produto.categoria < 0):
            raise Exception('Informe uma categoria!');

        return result


