import tkinter as tk
from tkinter import messagebox

from voter import VoterManager

class VoterWindow:
    def __init__(self, root, action):
        self.voter_manager = VoterManager()

        self.root = root
        self.root.title("Eleitores")

        # seleciona a janela que será aberta.
        if action == 'create':
            self.create()
        elif action == 'remove':
            self.remove()
        elif action == 'find':
            self.find()
        elif action == 'find_all':
            self.find_all()

    def create(self):
        # janela principal.
        tk.Label(self.root, text="Cadastrar eleitor", font=("Arial", 14)).pack(pady=20, anchor='w')

        # frame para os campos de entrada.
        tk.Label(self.root, text="Nome", font=("Arial", 10)).pack(anchor='w')
        self.name = tk.Entry(self.root, width=30)
        self.name.pack(pady=5, anchor='w')

        tk.Label(self.root, text="Data de nascimento (DD/MM/AAAA)", font=("Arial", 10)).pack(anchor='w')
        self.date_of_birth = tk.Entry(self.root, width=30)
        self.date_of_birth.pack(pady=5, anchor='w')

        tk.Label(self.root, text="Seção", font=("Arial", 10)).pack(anchor='w')
        self.section = tk.Entry(self.root, width=30)
        self.section.pack(pady=5, anchor='w')
        
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # botões que abrem as janelas de cada módulo.
        tk.Button(frame_buttons, text="Cadastrar eleitor", command=self.create_voter_button).pack(side=tk.LEFT, anchor='w')
        tk.Button(frame_buttons, text="Cancelar", command=self.cancel_button).pack(side=tk.RIGHT, anchor='w')
    
    def remove(self):
        # janela principal.
        tk.Label(self.root, text="Remover eleitor", font=("Arial", 14)).pack(pady=20)

        # frame para os campos de entrada.
        tk.Label(self.root, text="ID do eleitor", font=("Arial", 10)).pack(anchor='w')
        self.voter_id = tk.Entry(self.root, width=30)
        self.voter_id.pack(pady=5, anchor='w')
        
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # botões que abrem as janelas de cada módulo.
        tk.Button(frame_buttons, text="Remover eleitor", command=self.remove_voter_button).pack(side=tk.LEFT, anchor='w')
        tk.Button(frame_buttons, text="Cancelar", command=self.cancel_button).pack(side=tk.RIGHT, anchor='w')

    def find(self):
        # janela principal.
        tk.Label(self.root, text="Buscar eleitor", font=("Arial", 14)).pack(pady=20)
        
        # frame para os campos de entrada.
        tk.Label(self.root, text="ID do eleitor", font=("Arial", 10)).pack(anchor='w')
        self.voter_id = tk.Entry(self.root, width=30)
        self.voter_id.pack(pady=5, anchor='w')
        
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # botões que abrem as janelas de cada módulo.
        tk.Button(frame_buttons, text="Buscar eleitor", command=self.find_voter_button).pack(side=tk.LEFT, anchor='w')
        tk.Button(frame_buttons, text="Cancelar", command=self.cancel_button).pack(side=tk.RIGHT, anchor='w')

    def find_all(self):
        # janela principal.
        tk.Label(self.root, text="Essa é a página de eleitores", font=("Arial", 14)).pack(pady=20)
        
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # botões que abrem as janelas de cada módulo.
        tk.Button(frame_buttons, text="Botão", command=self.cancel_button).pack(side=tk.LEFT, padx=10)

    # botões de ação.
    def create_voter_button(self):
        self.voter_manager.create(self.name.get(), self.date_of_birth.get(), self.section.get())
        messagebox.showinfo("Eleitor cadastrado", "O eleitor foi cadastrado com sucesso!")
        self.root.destroy()

    def remove_voter_button(self):
        self.voter_manager.remove(self.voter_id.get())
        messagebox.showinfo("Eleitor removido", "O eleitor foi removido com sucesso!")
        self.root.destroy()

    def find_voter_button(self):
        self.voter = self.voter_manager.find(self.voter_id.get())
        messagebox.showinfo(
            "Dados do eleitor",
            f"Nome: {self.voter['name']}\n"
            f"ID do eleitor: {self.voter['voter_id']}\n"
            f"Data de nascimento: {self.voter['date_of_birth']}\n"
            f"Seção: {self.voter['section']}\n"
        )
        self.root.destroy()

    def cancel_button(self):
        self.root.destroy()