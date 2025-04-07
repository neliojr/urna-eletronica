import tkinter as tk  # Importa a biblioteca Tkinter para criar interfaces gráficas
from tkinter import messagebox  # Importa messagebox para exibir mensagens popup
from tkinter import ttk  # Importa ttk para widgets mais modernos

from role import RoleManager  # Importa a classe RoleManager do arquivo role.py

class RoleWindow:
    # Método construtor da classe
    def __init__(self, root, action):
        self.role_manager = RoleManager()  # Instancia o gerenciador de cargos

        self.root = root  # Define a janela principal
        self.root.title("Cargos")  # Define o título da janela

        # Decide qual janela abrir com base na ação fornecida
        if action == 'create':
            self.create()  # Chama método para criar cargo
        elif action == 'remove':
            self.remove()  # Chama método para remover cargo
        elif action == 'find':
            self.find()  # Chama método para buscar cargo
        elif action == 'find_all':
            self.find_all()  # Chama método para listar todos os cargos

    # Método para criar a janela de cadastro de cargo
    def create(self):
        # Cria e exibe o título da janela
        tk.Label(
            self.root,
            text="Cadastrar cargo",
            font=("Arial", 14)
        ).pack(pady=20, anchor='w')  # pady=20 adiciona espaçamento vertical, anchor='w' alinha à esquerda

        # Campo para entrada do nome do cargo
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

        # Opções para o campo de dígitos
        self.digits_options = ["2", "3", "4", "5"]  # Lista de opções disponíveis

        tk.Label(
            self.root,
            text="Dígitos",
            font=("Arial", 10)
        ).pack(anchor='w')  # Rótulo "Dígitos"
        self.digits = ttk.Combobox(
            self.root,
            values=self.digits_options,  # Define as opções do combobox
            state="readonly"  # Impede edição manual
        )
        self.digits.pack(
            pady=5,
            anchor='w'
        )

        # Opções para o campo de vice
        self.vice_options = ["Sim", "Não"]  # Lista de opções disponíveis

        tk.Label(
            self.root,
            text="Tem vice?",
            font=("Arial", 10)
        ).pack(anchor='w')  # Rótulo "Tem vice?"
        self.vice = ttk.Combobox(
            self.root,
            values=self.vice_options,
            state="readonly"
        )
        self.vice.pack(
            pady=5,
            anchor='w'
        )
        
        # Frame para organizar os botões
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # Botão de criar cargo
        tk.Button(
            frame_buttons,
            text="Criar cargo",
            command=self.create_role_button  # Chama função de criação ao clicar
        ).pack(side=tk.LEFT, anchor='w')  # side=tk.LEFT alinha à esquerda
        
        # Botão de cancelar
        tk.Button(
            frame_buttons,
            text="Cancelar",
            command=self.cancel_button  # Chama função de cancelar ao clicar
        ).pack(side=tk.RIGHT, anchor='w')  # side=tk.RIGHT alinha à direita
    
    # Método para criar a janela de remoção de cargo
    def remove(self):
        tk.Label(
            self.root,
            text="Remover cargo",
            font=("Arial", 14)
        ).pack(pady=20)  # Título da janela

        # Campo para entrada do nome do cargo a ser removido
        tk.Label(
            self.root,
            text="Nome",
            font=("Arial", 10)
        ).pack(anchor='w')
        self.name = tk.Entry(
            self.root,
            width=30
        )
        self.name.pack(
            pady=5,
            anchor='w'
        )
        
        frame_buttons = tk.Frame(self.root)  # Frame para botões
        frame_buttons.pack()

        tk.Button(
            frame_buttons,
            text="Remover cargo",
            command=self.remove_role_button  # Chama função de remoção
        ).pack(side=tk.LEFT, anchor='w')
        tk.Button(
            frame_buttons,
            text="Cancelar",
            command=self.cancel_button  # Chama função de cancelar
        ).pack(side=tk.RIGHT, anchor='w')

    # Método para criar a janela de busca de cargo
    def find(self):
        tk.Label(
            self.root,
            text="Buscar cargo",
            font=("Arial", 14)
        ).pack(pady=20)  # Título da janela
        
        tk.Label(
            self.root,
            text="Nome",
            font=("Arial", 10)
        ).pack(anchor='w')  # Campo de entrada do nome
        self.name = tk.Entry(
            self.root,
            width=30
        )
        self.name.pack(
            pady=5,
            anchor='w'
        )
        
        frame_buttons = tk.Frame(self.root)  # Frame para botões
        frame_buttons.pack()

        tk.Button(
            frame_buttons,
            text="Buscar cargo",
            command=self.find_role_button  # Chama função de busca
        ).pack(side=tk.LEFT, anchor='w')
        tk.Button(
            frame_buttons,
            text="Cancelar",
            command=self.cancel_button
        ).pack(side=tk.RIGHT, anchor='w')

    # Método para criar a janela de listagem de todos os cargos
    def find_all(self):
        tk.Label(
            self.root,
            text="Essa é a página de cargos",
            font=("Arial", 14)
        ).pack(pady=20)  # Título da janela
        
        frame_buttons = tk.Frame(self.root)  # Frame para botões
        frame_buttons.pack()

        tk.Button(
            frame_buttons,
            text="Botão",
            command=self.cancel_button  # Botão genérico (parece incompleto)
        ).pack(side=tk.LEFT, padx=10)  # padx=10 adiciona espaçamento horizontal

    # Método para processar a criação de um cargo
    def create_role_button(self):
        # Converte a opção de vice para booleano
        if self.vice.get() == 'Sim':
            self.vice = True
        else:
            self.vice = False

        # Chama o método create do RoleManager com os valores inseridos
        self.role_manager.create(
            self.name.get(),  # Nome do cargo
            self.digits.get(),  # Número de dígitos
            self.vice  # Tem vice?
        )

        # Exibe mensagem de sucesso
        messagebox.showinfo(
            "Cargo cadastrado",
            "O cargo foi criado com sucesso!"
        )

        self.root.destroy()  # Fecha a janela

    # Método para processar a remoção de um cargo
    def remove_role_button(self):
        self.role_manager.remove(
            self.name.get()  # Remove o cargo com o nome fornecido
        )
        messagebox.showinfo(
            "cargo removido",
            "O cargo foi removido com sucesso!"
        )

        self.root.destroy()  # Fecha a janela

    # Método para processar a busca de um cargo
    def find_role_button(self):
        self.role = self.role_manager.find(
            self.name.get()  # Busca o cargo pelo nome
        )

        # Verifica se o cargo foi encontrado
        if self.role is None:
            messagebox.showerror(
                "Erro",
                "Cargo não encontrado."
            )
            return

        # Converte o valor booleano de vice para texto
        if self.role['vice']:
            self.role['vice'] = "Sim"
        else:
            self.role['vice'] = "Não"

        # Exibe os dados do cargo encontrado
        messagebox.showinfo(
            "Dados do cargo",
            f"Nome: {self.role['name']}\n"
            f"Dígitos: {self.role['digits']}\n"
            f"Tem vice? {self.role['vice']}"
        )
        self.root.destroy()  # Fecha a janela

    # Método para cancelar e fechar a janela
    def cancel_button(self):
        self.root.destroy()  # Destrói a janela atual