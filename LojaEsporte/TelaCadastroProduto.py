import wpf
from Produto import Produto
from System.Windows import Window, MessageBox, MessageBoxButton, MessageBoxResult

class TelaCadastroProduto(Window):
    NOME_ARQUIVO = 'produtos.csv'
    APPEND_TO_FILE = 'a'
    READ_FILE = 'r'
    produtos_map = {
        0: 'Vestuario',
        1: 'Calcados',
        2: 'Acessorios',
        3: 'Equipamentos'
    }

    def __init__(self):
        wpf.LoadComponent(self, 'TelaCadastroProduto.xaml')
        self.listar()


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

    
    def excluir(self, sender, e):
        index = self.lvProdutos.SelectedIndex
        if (index == -1):
            MessageBox.Show('Selecione um produto!')
        elif(MessageBox.Show('Realmente deseja remover este produto?', '', MessageBoxButton.YesNo) == MessageBoxResult.Yes):
            del self.lvProdutos.ItemsSource[index]
            self.lvProdutos.Items.Refresh()
        pass
        
    def editar(self, sender, e):
        pass

