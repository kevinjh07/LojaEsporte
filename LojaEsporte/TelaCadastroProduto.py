# -*- coding: utf-8 -*-
import wpf, clr
from Produto import Produto
from System.Windows import Window, MessageBox, MessageBoxButton, MessageBoxResult
clr.AddReference('System.Data')
from System.Data.SqlClient import SqlConnection, SqlParameter

class TelaCadastroProduto(Window):
    NOME_ARQUIVO = 'produtos.csv'
    APPEND_TO_FILE = 'a'
    READ_FILE = 'r'
    WRITE = 'w'


    def __init__(self):
        wpf.LoadComponent(self, 'TelaCadastroProduto.xaml')
        self.id = None
        self.listar()


    def limpar(self, sender, e):
        self.txtNome.Text = ''
        self.txtPreco.Text = ''
        self.txtDescricao.Text = ''
        self.cbCategoria.SelectedIndex = -1
        self.txtNome.Focus()
        self.id = None
        pass

    
    def salvar(self, sender, e):
        produto = Produto(None, self.txtNome.Text, self.txtPreco.Text, 
                          self.txtDescricao.Text, self.cbCategoria.SelectedIndex)
        connection = SqlConnection("Data Source=(localdb)\MSSQLLocalDB;Initial Catalog=lojaesportes;Persist Security Info=True")
        try:
            connection.Open()
            command = connection.CreateCommand()
            command.CommandText = 'INSERT INTO produto (nome, descricao, preco, idCategoria) VALUES (@nome, @desc, @preco, @idCat)'
            command.Parameters.Add(SqlParameter('nome', produto.nome))
            command.Parameters.Add(SqlParameter('desc', produto.descricao))
            command.Parameters.Add(SqlParameter('preco', produto.preco))
            command.Parameters.Add(SqlParameter('idCat', produto.categoria))

            resultado = command.ExecuteNonQuery()
            self.listar()
            MessageBox.Show('Produto salvo!')
        except Exception as error:
            MessageBox.Show(error.message)
        finally:
            connection.Close()
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
        connection = SqlConnection("Data Source=(localdb)\MSSQLLocalDB;Initial Catalog=lojaesportes;Persist Security Info=True")
        try:
            connection.Open()
            command = connection.CreateCommand()
            command.CommandText = 'SELECT id, nome, descricao, preco, idCategoria FROM produto'
            
            reader = command.ExecuteReader()
            
            while reader.Read():
                produto = Produto(reader['id'], reader['nome'], 
                            reader['preco'], reader['descricao'],
                            reader['idCategoria'])
                produtos.append(produto)
            self.lvProdutos.ItemsSource = produtos
        except Exception as error:
            print(error)
            MessageBox.Show('Ocorreu um erro ao tentar ler os registros.\n{0}'.format(error.strerror))
        finally:
            connection.Close()
        pass

    
    def excluir(self, sender, e):
        index = self.lvProdutos.SelectedIndex
        if (index == -1):
            MessageBox.Show('Selecione um produto!')
        elif(MessageBox.Show('Realmente deseja remover este produto?', '', MessageBoxButton.YesNo) == MessageBoxResult.Yes):
            connection = SqlConnection("Data Source=(localdb)\MSSQLLocalDB;Initial Catalog=lojaesportes;Persist Security Info=True")
            try:
                connection.Open()
                command = connection.CreateCommand()
                command.CommandText = 'DELETE FROM produto WHERE id = @id'
                produto = self.lvProdutos.ItemsSource[index]
                command.Parameters.Add(SqlParameter('id', produto.id))
                resultado = command.ExecuteNonQuery()
                if (resultado > 0):
                    self.listar()
                    MessageBox.Show('Produto removido!')
                else:
                    MessageBox.Show('O produto não pode ser removido')

            except Exception as error:
                MessageBox.Show('Ocorreu um erro ao tentar excluir o produto.\n{0}'.format(error.strerror))
            finally:
                connection.Close()
            #old
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

