import tkinter as tk
from tkinter import messagebox

from role import RoleManager

class RoleWindow:
    def __init__(self, root, action):
        self.role_manager = RoleManager()

        self.root = root
        self.root.title("Cargos")

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
        tk.Label(self.root, text="Cadastrar cargo", font=("Arial", 14)).pack(pady=20, anchor='w')

        # frame para os campos de entrada.
        tk.Label(self.root, text="Nome", font=("Arial", 10)).pack(anchor='w')
        self.name = tk.Entry(self.root, width=30)
        self.name.pack(pady=5, anchor='w')

        tk.Label(self.root, text="Dígitos", font=("Arial", 10)).pack(anchor='w')
        self.digits = tk.Entry(self.root, width=30)
        self.digits.pack(pady=5, anchor='w')

        tk.Label(self.root, text="Tem vice?", font=("Arial", 10)).pack(anchor='w')
        self.vice = tk.Entry(self.root, width=30)
        self.vice.pack(pady=5, anchor='w')
        
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # botões que abrem as janelas de cada módulo.
        tk.Button(frame_buttons, text="Criar cargo", command=self.create_role_button).pack(side=tk.LEFT, anchor='w')
        tk.Button(frame_buttons, text="Cancelar", command=self.cancel_button).pack(side=tk.RIGHT, anchor='w')
    
    def remove(self):
        # janela principal.
        tk.Label(self.root, text="Remover cargo", font=("Arial", 14)).pack(pady=20)

        # frame para os campos de entrada.
        tk.Label(self.root, text="Nome", font=("Arial", 10)).pack(anchor='w')
        self.name = tk.Entry(self.root, width=30)
        self.name.pack(pady=5, anchor='w')
        
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # botões que abrem as janelas de cada módulo.
        tk.Button(frame_buttons, text="Remover cargo", command=self.remove_role_button).pack(side=tk.LEFT, anchor='w')
        tk.Button(frame_buttons, text="Cancelar", command=self.cancel_button).pack(side=tk.RIGHT, anchor='w')

    def find(self):
        # janela principal.
        tk.Label(self.root, text="Buscar cargo", font=("Arial", 14)).pack(pady=20)
        
        # frame para os campos de entrada.
        tk.Label(self.root, text="Nome", font=("Arial", 10)).pack(anchor='w')
        self.name = tk.Entry(self.root, width=30)
        self.name.pack(pady=5, anchor='w')
        
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # botões que abrem as janelas de cada módulo.
        tk.Button(frame_buttons, text="Buscar cargo", command=self.find_role_button).pack(side=tk.LEFT, anchor='w')
        tk.Button(frame_buttons, text="Cancelar", command=self.cancel_button).pack(side=tk.RIGHT, anchor='w')

    def find_all(self):
        # janela principal.
        tk.Label(self.root, text="Essa é a página de cargos", font=("Arial", 14)).pack(pady=20)
        
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # botões que abrem as janelas de cada módulo.
        tk.Button(frame_buttons, text="Botão", command=self.cancel_button).pack(side=tk.LEFT, padx=10)

    # botões de ação.
    def create_role_button(self):
        if self.vice.get() == 'Sim':
            self.vice = True
        else:
            self.vice = False
        self.role_manager.create(self.name.get(), self.digits.get(), self.vice)
        messagebox.showinfo("Cargo cadastrado", "O cargo foi criado com sucesso!")
        self.root.destroy()

    def remove_role_button(self):
        self.role_manager.remove(self.name.get())
        messagebox.showinfo("cargo removido", "O cargo foi removido com sucesso!")
        self.root.destroy()

    def find_role_button(self):
        self.role = self.role_manager.find(self.name.get())

        if self.role is None:
            messagebox.showerror("Erro", "Cargo não encontrado.")
            return

        if self.role['vice']:
            self.role['vice'] = "Sim"
        else:
            self.role['vice'] = "Não"

        messagebox.showinfo(
            "Dados do cargo",
            f"Nome: {self.role['name']}\n"
            f"Dígitos: {self.role['digits']}\n"
            f"Tem vice? {self.role['vice']}"
        )
        self.root.destroy()

    def cancel_button(self):
        self.root.destroy()