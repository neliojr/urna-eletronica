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
        """Configura a interface para listagem geral de cargos"""
        # Limpa a janela principal
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Título da tela
        tk.Label(
            self.root,
            text="Lista de Todos os Cargos",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        # Obtém todos os eleitores
        all_roles = self.role_manager.display()
        
        if not all_roles:
            tk.Label(
                self.root,
                text="Nenhum cargo cadastrado.",
                font=("Arial", 10)
            ).pack(pady=20)
            return
        
        # Frame principal para a lista
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview para exibir os candidatos em formato de tabela
        columns = ("Nome", "Dígitos", "Vice")
        tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        # Configurações das colunas (largura personalizada para cada uma)
        column_config = {
            "Nome": {"width": 150, "anchor": "w", "minwidth": 100},
            "Dígitos": {"width": 75, "anchor": "center", "minwidth": 50},
            "Vice": {"width": 75, "anchor": "center", "minwidth": 40}
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
        for role in all_roles:
            tree.insert("", "end", values=(
                role['name'],
                role['digits'],
                "Sim" if role['vice'] else "Não"
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