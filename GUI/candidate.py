import tkinter as tk
from tkinter import messagebox

from candidate import CandidateManager

class CandidateWindow:
    def __init__(self, root, action):
        self.candidate_manager = CandidateManager()

        self.root = root
        self.root.title("candidatoes")

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
        tk.Label(self.root, text="Cadastrar candidato", font=("Arial", 14)).pack(pady=20, anchor='w')

        # frame para os campos de entrada.
        tk.Label(self.root, text="Nome", font=("Arial", 10)).pack(anchor='w')
        self.name = tk.Entry(self.root, width=30)
        self.name.pack(pady=5, anchor='w')

        tk.Label(self.root, text="Número", font=("Arial", 10)).pack(anchor='w')
        self.number = tk.Entry(self.root, width=30)
        self.number.pack(pady=5, anchor='w')

        tk.Label(self.root, text="Cargo", font=("Arial", 10)).pack(anchor='w')
        self.role = tk.Entry(self.root, width=30)
        self.role.pack(pady=5, anchor='w')
        
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # botões que abrem as janelas de cada módulo.
        tk.Button(frame_buttons, text="Cadastrar candidato", command=self.create_candidate_button).pack(side=tk.LEFT, anchor='w')
        tk.Button(frame_buttons, text="Cancelar", command=self.cancel_button).pack(side=tk.RIGHT, anchor='w')
    
    def remove(self):
        # janela principal.
        tk.Label(self.root, text="Remover candidato", font=("Arial", 14)).pack(pady=20)

        # frame para os campos de entrada.
        tk.Label(self.root, text="Cargo", font=("Arial", 10)).pack(anchor='w')
        self.role = tk.Entry(self.root, width=30)
        self.role.pack(pady=5, anchor='w')

        tk.Label(self.root, text="Número", font=("Arial", 10)).pack(anchor='w')
        self.number = tk.Entry(self.root, width=30)
        self.number.pack(pady=5, anchor='w')
        
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # botões que abrem as janelas de cada módulo.
        tk.Button(frame_buttons, text="Remover candidato", command=self.remove_candidate_button).pack(side=tk.LEFT, anchor='w')
        tk.Button(frame_buttons, text="Cancelar", command=self.cancel_button).pack(side=tk.RIGHT, anchor='w')

    def find(self):
        # janela principal.
        tk.Label(self.root, text="Buscar candidato", font=("Arial", 14)).pack(pady=20)
        
        # frame para os campos de entrada.
        tk.Label(self.root, text="Cargo", font=("Arial", 10)).pack(anchor='w')
        self.role = tk.Entry(self.root, width=30)
        self.role.pack(pady=5, anchor='w')

        tk.Label(self.root, text="Número", font=("Arial", 10)).pack(anchor='w')
        self.number = tk.Entry(self.root, width=30)
        self.number.pack(pady=5, anchor='w')
        
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # botões que abrem as janelas de cada módulo.
        tk.Button(frame_buttons, text="Buscar candidato", command=self.find_candidate_button).pack(side=tk.LEFT, anchor='w')
        tk.Button(frame_buttons, text="Cancelar", command=self.cancel_button).pack(side=tk.RIGHT, anchor='w')

    def find_all(self):
        # janela principal.
        tk.Label(self.root, text="Essa é a página de candidatos", font=("Arial", 14)).pack(pady=20)
        
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # botões que abrem as janelas de cada módulo.
        tk.Button(frame_buttons, text="Botão", command=self.cancel_button).pack(side=tk.LEFT, padx=10)

    # botões de ação.
    def create_candidate_button(self):
        self.candidate_manager.create(self.name.get(), self.number.get(), self.role.get())
        messagebox.showinfo("Candidato cadastrado", "O candidato foi cadastrado com sucesso!")
        self.root.destroy()

    def remove_candidate_button(self):
        self.candidate_manager.remove(self.role.get(), self.number.get())
        messagebox.showinfo("Candidato removido", "O candidato foi removido com sucesso!")
        self.root.destroy()

    def find_candidate_button(self):
        self.candidate = self.candidate_manager.find(self.role.get(), self.number.get())
        
        if self.candidate is None:
            messagebox.showerror("Erro", "Candidato não encontrado.")
            return
        
        messagebox.showinfo(
            "Dados do candidato",
            f"Nome: {self.candidate['name']}\n"
            f"Cargo: {self.candidate['role']}\n"
            f"Número: {self.candidate['number']}"
        )
        self.root.destroy()

    def cancel_button(self):
        self.root.destroy()