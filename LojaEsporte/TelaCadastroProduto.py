# -*- coding: utf-8 -*-
import wpf, clr
from Produto import Produto
from System.Windows import Window, MessageBox, MessageBoxButton, MessageBoxResult
clr.AddReference('System.Data')
from System.Data.SqlClient import SqlConnection, SqlParameter

class TelaCadastroProduto(Window):

    def __init__(self):
        wpf.LoadComponent(self, 'TelaCadastroProduto.xaml')
        self.id = None
        self.listar()


    def limpar(self, sender, e):
        self.txtId.Text = None
        self.txtNome.Text = ''
        self.txtPreco.Text = ''
        self.txtDescricao.Text = ''
        self.cbCategoria.SelectedIndex = -1
        self.txtNome.Focus()
        self.id = None
        pass

    
    def salvar(self, sender, e):
        produto = Produto(self.txtId.Text, self.txtNome.Text, self.txtPreco.Text, 
                          self.txtDescricao.Text, self.cbCategoria.SelectedIndex)
        if (produto.id == None or produto.id == ''):
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
                self.limpar(sender, e)
                MessageBox.Show('Produto salvo!')
            except Exception as error:
                MessageBox.Show(error.message)
            finally:
                connection.Close()
            pass
        else:
            self.salvar_edicao(produto, sender, e)
        pass


    def salvar_edicao(self, produto, sender, e):
        connection = SqlConnection("Data Source=(localdb)\MSSQLLocalDB;Initial Catalog=lojaesportes;Persist Security Info=True")
        try:
            connection.Open()
            command = connection.CreateCommand()
            command.CommandText = 'UPDATE produto SET nome=@nome, descricao=@descricao, preco=@preco, idCategoria=@categoria WHERE id=@id'
            command.Parameters.Add(SqlParameter('nome', produto.nome))
            command.Parameters.Add(SqlParameter('descricao', produto.descricao))
            command.Parameters.Add(SqlParameter('preco', produto.preco))
            command.Parameters.Add(SqlParameter('categoria', produto.categoria))
            command.Parameters.Add(SqlParameter('id', produto.id))

            resultado = command.ExecuteNonQuery()
            self.listar()
            self.limpar(sender, e)
            MessageBox.Show('Produto editado!')
        except Exception as error:
            MessageBox.Show('Não foi possivel editar o produto!')
        finally:
            connection.Close()
        pass


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
                produto = Produto(int(reader['id']), reader['nome'], 
                            float(reader['preco']), reader['descricao'],
                            int(reader['idCategoria']))
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
                self.listar()
                MessageBox.Show('Produto removido!')
            except Exception as error:
                MessageBox.Show('O produto não pode ser removido')
            finally:
                connection.Close()
        pass
    
    
    def editar(self, sender, e):
        index = self.lvProdutos.SelectedIndex
        if (index > -1):
            produto = self.lvProdutos.ItemsSource[index]
            self.preencherCampos(produto)
        else:
            MessageBox.Show('Selecione um produto!')
        pass

    
    def preencherCampos(self, produto):
        self.txtId.Text = str(produto.id)
        self.txtNome.Text = produto.nome
        self.txtPreco.Text = str(produto.preco)
        self.txtDescricao.Text = produto.descricao
        self.cbCategoria.SelectedIndex = produto.categoria
        pass

