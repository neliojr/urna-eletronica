import datetime  # Importa módulo para manipulação de datas
import tkinter as tk  # Importa Tkinter para criar interfaces gráficas
from tkinter import messagebox  # Importa messagebox para exibir mensagens popup
from tkcalendar import DateEntry  # Importa DateEntry para campo de calendário

from voter import VoterManager  # Importa a classe VoterManager do arquivo voter.py

class VoterWindow:
    # Método construtor da classe
    def __init__(self, root, action):
        self.voter_manager = VoterManager()  # Instancia o gerenciador de eleitores

        self.root = root  # Define a janela principal
        self.root.title("Eleitores")  # Define o título da janela

        # Decide qual janela abrir com base na ação fornecida
        if action == 'create':
            self.create()  # Chama método para criar eleitor
        elif action == 'remove':
            self.remove()  # Chama método para remover eleitor
        elif action == 'find':
            self.find()  # Chama método para buscar eleitor
        elif action == 'find_all':
            self.find_all()  # Chama método para listar todos os eleitores

    # Método para criar a janela de cadastro de eleitor
    def create(self):
        # Título da janela
        tk.Label(
            self.root,
            text="Cadastrar eleitor",
            font=("Arial", 14)
        ).pack(pady=20, anchor='w')  # pady=20 adiciona espaçamento vertical, anchor='w' alinha à esquerda

        # Campo para entrada do nome
        tk.Label(
            self.root,
            text="Nome",
            font=("Arial", 10)
        ).pack(anchor='w')  # Rótulo "Nome"
        self.name = tk.Entry(
            self.root,
            width=30  # Largura do campo de entrada
        )
        self.name.pack(
            pady=5,  # Espaçamento vertical
            anchor='w'  # Alinhamento à esquerda
        )

        # Campo para data de nascimento com calendário
        tk.Label(
            self.root,
            text="Data de nascimento",
            font=("Arial", 10)
        ).pack(anchor='w')  # Rótulo "Data de nascimento"
        self.date_of_birth = tk.StringVar()  # Variável para armazenar a data selecionada

        self.calendar = DateEntry(
            self.root,
            date_pattern='dd/mm/yyyy',  # Formato da data
            locale='pt_BR',  # Localização para português do Brasil
            textvariable=self.date_of_birth,  # Vincula à variável
            maxdate=datetime.date.today()  # Limita a data máxima ao dia atual
        )
        self.calendar.pack(pady=5)  # Exibe o calendário

        # Campo para entrada da seção eleitoral
        tk.Label(
            self.root,
            text="Seção",
            font=("Arial", 10)
        ).pack(anchor='w')  # Rótulo "Seção"
        self.section = tk.Entry(
            self.root,
            width=30
        )
        self.section.pack(
            pady=5,
            anchor='w'
        )
        
        # Frame para organizar os botões
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # Botão de cadastrar eleitor
        tk.Button(
            frame_buttons,
            text="Cadastrar eleitor",
            command=self.create_voter_button  # Chama função de criação ao clicar
        ).pack(side=tk.LEFT, anchor='w')  # Alinha à esquerda
        
        # Botão de cancelar
        tk.Button(
            frame_buttons,
            text="Cancelar",
            command=self.cancel_button  # Chama função de cancelar ao clicar
        ).pack(side=tk.RIGHT, anchor='w')  # Alinha à direita
    
    # Método para criar a janela de remoção de eleitor
    def remove(self):
        # Título da janela
        tk.Label(
            self.root,
            text="Remover eleitor",
            font=("Arial", 14)
        ).pack(pady=20)

        # Campo para entrada do ID do eleitor
        tk.Label(
            self.root,
            text="ID do eleitor",
            font=("Arial", 10)
        ).pack(anchor='w')
        self.voter_id = tk.Entry(
            self.root,
            width=30
        )
        self.voter_id.pack(
            pady=5,
            anchor='w'
        )
        
        # Frame para botões
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # Botão de remover eleitor
        tk.Button(
            frame_buttons,
            text="Remover eleitor",
            command=self.remove_voter_button  # Chama função de remoção
        ).pack(side=tk.LEFT, anchor='w')
        # Botão de cancelar
        tk.Button(
            frame_buttons,
            text="Cancelar",
            command=self.cancel_button
        ).pack(side=tk.RIGHT, anchor='w')

    # Método para criar a janela de busca de eleitor
    def find(self):
        # Título da janela
        tk.Label(
            self.root,
            text="Buscar eleitor",
            font=("Arial", 14)
        ).pack(pady=20)
        
        # Campo para entrada do ID do eleitor
        tk.Label(
            self.root,
            text="ID do eleitor",
            font=("Arial", 10)
        ).pack(anchor='w')
        self.voter_id = tk.Entry(
            self.root,
            width=30
        )
        self.voter_id.pack(
            pady=5,
            anchor='w'
        )
        
        # Frame para botões
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # Botão de buscar eleitor
        tk.Button(
            frame_buttons,
            text="Buscar eleitor",
            command=self.find_voter_button  # Chama função de busca
        ).pack(side=tk.LEFT, anchor='w')
        # Botão de cancelar
        tk.Button(
            frame_buttons,
            text="Cancelar",
            command=self.cancel_button
        ).pack(side=tk.RIGHT, anchor='w')

    # Método para criar a janela de listagem de todos os eleitores
    def find_all(self):
        # Título da janela
        tk.Label(
            self.root,
            text="Essa é a página de eleitores",
            font=("Arial", 14)
        ).pack(pady=20)
        
        # Frame para botões
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # Botão genérico (parece incompleto)
        tk.Button(
            frame_buttons,
            text="Botão",
            command=self.cancel_button  # Fecha a janela ao clicar
        ).pack(side=tk.LEFT, padx=10)  # padx=10 adiciona espaçamento horizontal

    # Método para processar o cadastro de um eleitor
    def create_voter_button(self):
        # Chama o método create do VoterManager com os valores inseridos
        self.voter_manager.create(
            self.name.get(),  # Nome do eleitor
            self.date_of_birth.get(),  # Data de nascimento
            self.section.get()  # Seção eleitoral
        )
        # Exibe mensagem de sucesso
        messagebox.showinfo(
            "Eleitor cadastrado",
            "O eleitor foi cadastrado com sucesso!"
        )
        self.root.destroy()  # Fecha a janela

    # Método para processar a remoção de um eleitor
    def remove_voter_button(self):
        # Chama o método remove do VoterManager com o ID fornecido
        self.voter_manager.remove(
            self.voter_id.get()
        )
        # Exibe mensagem de sucesso
        messagebox.showinfo(
            "Eleitor removido",
            "O eleitor foi removido com sucesso!"
        )
        self.root.destroy()  # Fecha a janela

    # Método para processar a busca de um eleitor
    def find_voter_button(self):
        # Busca o eleitor pelo ID fornecido
        self.voter = self.voter_manager.find(
            self.voter_id.get()
        )

        # Verifica se o eleitor foi encontrado
        if self.voter is None:
            messagebox.showerror(
                "Erro",
                "Eleitor não encontrado."
            )
            return
        
        # Exibe os dados do eleitor encontrado
        messagebox.showinfo(
            "Dados do eleitor",
            f"Nome: {self.voter['name']}\n"
            f"ID do eleitor: {self.voter['voter_id']}\n"
            f"Data de nascimento: {self.voter['date_of_birth']}\n"
            f"Seção: {self.voter['section']}"
        )
        self.root.destroy()  # Fecha a janela

    # Método para cancelar e fechar a janela
    def cancel_button(self):
        self.root.destroy()  # Destrói a janela atual