import wpf
import re

from Pessoa import Pessoa
from System.Windows import Window, MessageBox, MessageBoxButton, MessageBoxResult

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
        self.txtNome.Text = ''
        self.txtEmail.Text = ''
        self.txtCpf.Text = ''
        self.txtNome.Focus()
        self.id = None
        pass

    def salvar(self, sender, e):
        pessoa = Pessoa(self.txtNome.Text, self.txtEmail.Text, self.txtCpf.Text)
        try:
            self.validar_pessoa(pessoa)
            if (self.id == None):
                self.salvar_arquivo(self.NOME_ARQUIVO, self.APPEND_TO_FILE, pessoa)
                self.limpar(sender, e)
            else:
                self.lvPessoas.ItemsSource[self.id] = pessoa
                self.lvPessoas.Items.Refresh()
                itens = self.lvPessoas.Items
                self.editar_arquivo(self.NOME_ARQUIVO, self.WRITE, itens)
                self.limpar(sender, e)

            self.listar()
            MessageBox.Show('Pessoa salvo!')
        except Exception as error:
            MessageBox.Show(error.message)
            pass

        pass

    def salvar_arquivo(self, nome_arquivo, modo, pessoa):
        file = open(nome_arquivo, modo)
        file.write(pessoa.to_csv() + '\n')
        file.flush()
        file.close()


    def editar_arquivo(self, nome_arquivo, modo, itens):
        file = open(self.NOME_ARQUIVO, self.WRITE)
        for i in itens:
            file.write(i.to_csv() + '\n')

        file.flush()
        file.close()


    def validar_pessoa(self, pessoa):
        if (len(pessoa.nome.strip()) == 0):
            raise Exception('Informe um nome!')

        if (len(pessoa.email.strip()) == 0):
            raise Exception('Informe um e-mail!\n')

        regexStr = r'^([^@]+)@[^@]+$'
        matchobj = re.search(regexStr, pessoa.email)
        if  matchobj is None:
            raise Exception('E-mail invalido!')

        if (len(pessoa.cpf.strip()) == 0):
            raise Exception('Informe um cpf!')


    def listar(self):
        pessoas = []
        try:
            file = open(self.NOME_ARQUIVO, self.READ_FILE)
            for f in file:
                split = f.split(',')
                pessoa = Pessoa(split[0], split[1],  split[2].replace('\n', ''))
                pessoas.append(pessoa)
                
            
            file.close()
        except IOError as error:
            print(error)
            MessageBox.Show('Ocorreu um erro ao tentar ler o arquivo.\n{0}'.format(error.strerror))

        self.lvPessoas.ItemsSource = pessoas

    
    def excluir(self, sender, e):
        index = self.lvPessoas.SelectedIndex
        if (index == -1):
            MessageBox.Show('Selecione uma pessoa!')
        elif(MessageBox.Show('Realmente deseja remover esta pessoa?', '', MessageBoxButton.YesNo) == MessageBoxResult.Yes):
            del self.lvPessoas.ItemsSource[index]
            self.lvPessoas.Items.Refresh()
            self.id = None
            itens = self.lvPessoas.Items
            self.editar_arquivo(self.NOME_ARQUIVO, self.WRITE, itens)
            self.listar()
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
        self.txtNome.Text = pessoa.nome
        self.txtEmail.Text = pessoa.email
        self.txtCpf.Text = pessoa.cpf
        pass

