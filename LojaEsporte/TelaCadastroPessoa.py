# -*- coding: utf-8 -*-
import wpf, clr, re

from Pessoa import Pessoa
from System.Windows import Window, MessageBox, MessageBoxButton, MessageBoxResult
clr.AddReference('System.Data')
from System.Data.SqlClient import SqlConnection, SqlParameter

class TelaCadastroPessoa(Window):
    NOME_ARQUIVO = 'pessoas.csv'
    APPEND_TO_FILE = 'a'
    READ_FILE = 'r'
    WRITE = 'w'

    def __init__(self):
        wpf.LoadComponent(self, 'TelaCadastroPessoa.xaml')
        self.id = None
        self.listar()

    
    def limpar(self, sender, e):
        self.txtId.Text = None
        self.txtNome.Text = ''
        self.txtEmail.Text = ''
        self.txtCpf.Text = ''
        self.txtNome.Focus()
        self.id = None
        pass

    def salvar(self, sender, e):
        pessoa = Pessoa(self.txtId.Text, self.txtNome.Text, self.txtEmail.Text, self.txtCpf.Text)
        if (pessoa.id == None or pessoa.id == ''):
            connection = SqlConnection("Data Source=(localdb)\MSSQLLocalDB;Initial Catalog=lojaesportes;Persist Security Info=True")
            try:
                connection.Open()
                command = connection.CreateCommand()
                command.CommandText = 'INSERT INTO pessoa (nome, email, cpf) VALUES (@nome, @email, @cpf)'
                command.Parameters.Add(SqlParameter('nome', pessoa.nome))
                command.Parameters.Add(SqlParameter('email', pessoa.email))
                command.Parameters.Add(SqlParameter('cpf', pessoa.cpf))

                resultado = command.ExecuteNonQuery()
                self.limpar(sender, e)
                self.listar()
                MessageBox.Show('Pessoa salva!')
            except Exception as error:
                MessageBox.Show('Erro ao salvar a pessoa!')
            finally:
                connection.Close()
            pass
        else:
            self.salvar_edicao(pessoa, sender, e)
        pass


    def salvar_edicao(self, pessoa, sender, e):
        connection = SqlConnection("Data Source=(localdb)\MSSQLLocalDB;Initial Catalog=lojaesportes;Persist Security Info=True")
        try:
            connection.Open()
            command = connection.CreateCommand()
            command.CommandText = 'UPDATE pessoa SET nome=@nome, email=@email, cpf=@cpf WHERE id=@id'
            command.Parameters.Add(SqlParameter('nome', pessoa.nome))
            command.Parameters.Add(SqlParameter('email', pessoa.email))
            command.Parameters.Add(SqlParameter('cpf', pessoa.cpf))
            command.Parameters.Add(SqlParameter('id', pessoa.id))

            resultado = command.ExecuteNonQuery()
            self.listar()
            self.limpar(sender, e)
            MessageBox.Show('Pessoa editada!')
        except Exception as error:
            MessageBox.Show('Não foi possivel editar a Pessoa!')
        finally:
            connection.Close()
        pass


    def validar_pessoa(self, pessoa):
        if (len(pessoa.nome.strip()) == 0):
            raise Exception('Informe um nome!')

        if (len(pessoa.email.strip()) == 0):
            raise Exception('Informe um e-mail!\n')

        regexStr = r'^([^@]+)@[^@]+$'
        matchobj = re.search(regexStr, pessoa.email)
        if  matchobj is None:
            raise Exception('E-mail invalido!')

        if  re.search(r'^[0-9]{11}$', pessoa.cpf) is None:
            raise Exception('CPF invalido!')


    def listar(self):
        pessoas = []
        connection = SqlConnection("Data Source=(localdb)\MSSQLLocalDB;Initial Catalog=lojaesportes;Persist Security Info=True")
        try:
            connection.Open()
            command = connection.CreateCommand()
            command.CommandText = 'SELECT id, nome, email, cpf FROM pessoa'
            
            reader = command.ExecuteReader()
            
            while reader.Read():
                pessoa = Pessoa(int(reader['id']), reader['nome'], 
                            reader['email'], reader['cpf'])
                pessoas.append(pessoa)
            self.lvPessoas.ItemsSource = pessoas
        except Exception as error:
            MessageBox.Show('Ocorreu um erro ao listar as pessoas!')
        finally:
            connection.Close()
        pass

    
    def excluir(self, sender, e):
        index = self.lvPessoas.SelectedIndex
        if (index == -1):
            MessageBox.Show('Selecione uma pessoa!')
        elif(MessageBox.Show('Realmente deseja remover esta pessoa?', '', MessageBoxButton.YesNo) == MessageBoxResult.Yes):
            connection = SqlConnection("Data Source=(localdb)\MSSQLLocalDB;Initial Catalog=lojaesportes;Persist Security Info=True")
            try:
                connection.Open()
                command = connection.CreateCommand()
                command.CommandText = 'DELETE FROM pessoa WHERE id = @id'
                pessoa = self.lvPessoas.ItemsSource[index]
                command.Parameters.Add(SqlParameter('id', pessoa.id))
                resultado = command.ExecuteNonQuery()
                self.listar()
                MessageBox.Show('Pessoa removida!')
            except Exception as error:
                MessageBox.Show('A pessoa não pode ser removida!')
            finally:
                connection.Close()
        pass
    
    
    def editar(self, sender, e):
        index = self.lvPessoas.SelectedIndex
        if (index > -1):
            pessoa = self.lvPessoas.ItemsSource[index]
            self.id = index
            self.preencherCampos(pessoa)
        else:
            MessageBox.Show('Selecione uma pessoa!')
        pass

    
    def preencherCampos(self, pessoa):
        self.txtId.Text = str(pessoa.id)
        self.txtNome.Text = pessoa.nome
        self.txtEmail.Text = pessoa.email
        self.txtCpf.Text = pessoa.cpf
        pass

