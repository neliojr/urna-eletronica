import datetime  # Importa módulo para manipulação de datas
import tkinter as tk  # Importa Tkinter para criar interfaces gráficas
from tkinter import messagebox  # Importa messagebox para exibir mensagens popup
from tkinter import ttk
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

        self.date_of_birth = DateEntry(
            self.root,
            date_pattern='dd/mm/yyyy',  # Formato da data
            locale='pt_BR',  # Localização para português do Brasil
            maxdate=datetime.date.today()  # Limita a data máxima ao dia atual
        )
        self.date_of_birth.pack(pady=5)  # Exibe o calendário

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
        """Configura a interface para listagem geral de eleitores"""
        # Limpa a janela principal
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Título da tela
        tk.Label(
            self.root,
            text="Lista de Todos os Eleitoress",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        # Obtém todos os eleitores
        all_voters = self.voter_manager.display()
        
        if not all_voters:
            tk.Label(
                self.root,
                text="Nenhum eleitor cadastrado.",
                font=("Arial", 10)
            ).pack(pady=20)
            return
        
        # Frame principal para a lista
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview para exibir os candidatos em formato de tabela
        columns = ("ID", "Nome", "Data de nascimento", "Seção")
        tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        # Configurações das colunas (largura personalizada para cada uma)
        column_config = {
            "ID": {"width": 150, "anchor": "center", "minwidth": 100},
            "Nome": {"width": 250, "anchor": "w", "minwidth": 150},
            "Data de nascimento": {"width": 200, "anchor": "center", "minwidth": 100},
            "Seção": {"width": 40, "anchor": "center", "minwidth": 40}
        }
        
        # Configura as colunas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, **column_config[col]) # Aplica as configurações
        
        # Adiciona barra de rolagem
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Preenche a tabela com os eleitores
        for voter in all_voters:
            tree.insert("", "end", values=(
                voter['voter_id'],
                voter['name'],
                voter['date_of_birth'],
                voter['section'],
            ))
        
        # Frame para os botões
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        # Botão para fechar
        tk.Button(
            button_frame,
            text="Fechar",
            command=self.root.destroy,
            width=20
        ).pack()

    # Método para processar o cadastro de um eleitor
    def create_voter_button(self):
        date_of_birth = self.date_of_birth.get_date()
        date_of_birth_formated = date_of_birth.strftime('%d/%m/%Y')
        # Chama o método create do VoterManager com os valores inseridos
        self.voter_manager.create(
            self.name.get(),  # Nome do eleitor
            date_of_birth_formated,  # Data de nascimento
            self.section.get()  # Seção eleitoral
        )
        # Exibe mensagem de sucesso
        messagebox.showinfo(
            "Eleitor cadastrado",
            "O eleitor foi cadastrado com sucesso!",
            parent=self.root
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
            "O eleitor foi removido com sucesso!",
            parent=self.root
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
                "Eleitor não encontrado.",
            parent=self.root
            )
            return
        
        # Exibe os dados do eleitor encontrado
        messagebox.showinfo(
            "Dados do eleitor",
            f"Nome: {self.voter['name']}\n"
            f"ID do eleitor: {self.voter['voter_id']}\n"
            f"Data de nascimento: {self.voter['date_of_birth']}\n"
            f"Seção: {self.voter['section']}",
            parent=self.root
        )
        self.root.destroy()  # Fecha a janela

    # Método para cancelar e fechar a janela
    def cancel_button(self):
        self.root.destroy()  # Destrói a janela atual