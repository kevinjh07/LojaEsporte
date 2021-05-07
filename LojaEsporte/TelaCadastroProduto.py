import wpf
from Produto import Produto
from System.Windows import Window, MessageBox, MessageBoxButton, MessageBoxResult

class TelaCadastroProduto(Window):
    NOME_ARQUIVO = 'produtos.csv'
    APPEND_TO_FILE = 'a'
    READ_FILE = 'r'
    WRITE = 'w'


    def __init__(self):
        wpf.LoadComponent(self, 'TelaCadastroProduto.xaml')
        self.id = None
        self.create_file_if_not_exists(self.NOME_ARQUIVO)
        self.listar()

    
    def create_file_if_not_exists(self, path):
        try:
            f = open(path)
            f.close()
        except IOError:
            f = open(path, 'w')
            f.close()


    def limpar(self, sender, e):
        self.txtNome.Text = ''
        self.txtPreco.Text = ''
        self.txtDescricao.Text = ''
        self.cbCategoria.SelectedIndex = -1
        self.txtNome.Focus()
        self.id = None
        pass

    
    def salvar(self, sender, e):
        produto = Produto(self.txtNome.Text, self.txtPreco.Text, 
                          self.txtDescricao.Text, self.cbCategoria.SelectedIndex)
        try:
            self.validar_produto(produto)
            if (self.id == None):
                self.salvar_arquivo(self.NOME_ARQUIVO, self.APPEND_TO_FILE, produto)
                self.limpar(sender, e)
            else:
                self.lvProdutos.ItemsSource[self.id] = produto
                self.lvProdutos.Items.Refresh()
                itens = self.lvProdutos.Items
                self.editar_arquivo(self.NOME_ARQUIVO, self.WRITE, itens)
                self.limpar(sender, e)

            self.listar()
            MessageBox.Show('Produto salvo!')
        except Exception as error:
            MessageBox.Show(error.message)
            pass

        pass

    def salvar_arquivo(self, nome_arquivo, modo, produto):
        file = open(nome_arquivo, modo)
        file.write(produto.to_csv() + '\n')
        file.flush()
        file.close()


    def editar_arquivo(self, nome_arquivo, modo, itens):
        file = open(self.NOME_ARQUIVO, self.WRITE)
        for i in itens:
            file.write(i.to_csv() + '\n')

        file.flush()
        file.close()


    def validar_produto(self, produto):
        if (len(produto.nome.strip()) == 0):
            raise Exception('Informe um nome!')

        if (len(produto.preco.strip()) == 0):
            raise Exception('Informe um preco!\n')

        if (len(produto.descricao.strip()) == 0):
            raise Exception('Informe uma descricao!')

        if (produto.categoria < 0):
            raise Exception('Informe uma categoria!')


    def listar(self):
        produtos = []
        try:
            file = open(self.NOME_ARQUIVO, self.READ_FILE)
            for f in file:
                split = f.split(',')
                nome_produto = split[3].replace('\n', '')
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
            self.id = None
            itens = self.lvProdutos.Items
            self.editar_arquivo(self.NOME_ARQUIVO, self.WRITE, itens)
            self.listar()
        pass
    
    
    def editar(self, sender, e):
        index = self.lvProdutos.SelectedIndex
        if (index > -1):
            produto = self.lvProdutos.ItemsSource[index]
            self.id = index
            self.preencherCampos(produto)
        else:
            MessageBox.Show('Selecione um produto!')
        pass

    
    def preencherCampos(self, produto):
        self.txtNome.Text = produto.nome
        self.txtPreco.Text = produto.preco
        self.txtDescricao.Text = produto.descricao
        self.cbCategoria.SelectedIndex = int(produto.categoria)
        pass

