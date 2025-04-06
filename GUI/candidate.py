import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

from candidate import CandidateManager
from role import RoleManager

class CandidateWindow:
    def __init__(self, root, action):
        self.candidate_manager = CandidateManager()
        self.role_manager = RoleManager()

        self.root = root
        self.root.title("Candidatos")

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
        self.roles = self.role_manager.display()
        
        # janela principal.
        self.content = tk.Frame(self.root)
        self.content.pack()

        tk.Label(
            self.content,
            text="Cadastrar candidato",
            font=("Arial", 14)
        ).pack(pady=20, anchor='w')

        # frame para os campos de entrada.
        tk.Label(
            self.content,
            text="Nome",
            font=("Arial", 10)
        ).pack(anchor='w')
        self.name = tk.Entry(
            self.content,
            width=30
        )
        self.name.pack(
            pady=5,
            anchor='w'
        )

        tk.Label(
            self.content,
            text="Número",
            font=("Arial", 10)
        ).pack(anchor='w')
        self.number = tk.Entry(
            self.content,
            width=30
        )
        self.number.pack(
            pady=5,
            anchor='w'
        )

        self.role_options = [role['name'] for role in self.roles]
        tk.Label(
            self.content,
            text="Cargo",
            font=("Arial", 10)
        ).pack(anchor='w')
        self.role = ttk.Combobox(
            self.content,
            values=self.role_options,
            state="readonly"
        )
        self.role.pack(
            pady=5,
            anchor='w'
        )

        self.role.bind("<<ComboboxSelected>>", self.toggle_vice_fields)

        tk.Label(
            self.content,
            text="Foto",
            font=("Arial", 10)
        ).pack(anchor='w')

        self.frame_photo = tk.Frame(self.content)
        self.frame_photo.pack(anchor='w')

        self.photo = tk.Entry(
            self.frame_photo,
            width=25
        )
        self.photo.pack(side=tk.LEFT, pady=5)

        tk.Button(
            self.frame_photo,
            text="Selecionar",
            command=self.select_photo
        ).pack(side=tk.LEFT, padx=5)

        self.vice_label = tk.Label(
            self.content,
            text="Nome do vice",
            font=("Arial", 10)
        )
        self.vice = tk.Entry(
            self.content,
            width=30
        )

        self.vice_photo_label = tk.Label(
            self.content,
            text="Foto do vice",
            font=("Arial", 10)
        )

        self.frame_vice_photo = tk.Frame(self.content)

        self.vice_photo = tk.Entry(
            self.frame_vice_photo,
            width=25
        )
        self.vice_photo.pack(side=tk.LEFT, pady=5)

        tk.Button(
            self.frame_vice_photo,
            text="Selecionar",
            command=self.select_vice_photo
        ).pack(side=tk.LEFT, padx=5)

        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # botões que abrem as janelas de cada módulo.
        tk.Button(
            frame_buttons,
            text="Cadastrar candidato",
            command=self.create_candidate_button
        ).pack(side=tk.LEFT, anchor='w')
        tk.Button(
            frame_buttons,
            text="Cancelar",
            command=self.cancel_button
        ).pack(side=tk.RIGHT, anchor='w')
    
    def remove(self):
        self.roles = self.role_manager.display()
        # janela principal.
        tk.Label(
            self.root,
            text="Remover candidato",
            font=("Arial", 14)
        ).pack(pady=20)

        # frame para os campos de entrada.
        self.role_options = [role['name'] for role in self.roles]
        tk.Label(
            self.root,
            text="Cargo",
            font=("Arial", 10)
        ).pack(anchor='w')
        self.role = ttk.Combobox(
            self.root,
            values=self.role_options,
            state="readonly"
        )
        self.role.pack(
            pady=5,
            anchor='w'
        )

        tk.Label(
            self.root,
            text="Número",
            font=("Arial", 10)
        ).pack(anchor='w')
        self.number = tk.Entry(
            self.root,
            width=30
        )
        self.number.pack(
            pady=5,
            anchor='w'
        )
        
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # botões que abrem as janelas de cada módulo.
        tk.Button(
            frame_buttons,
            text="Remover candidato",
            command=self.remove_candidate_button
        ).pack(side=tk.LEFT, anchor='w')
        tk.Button(
            frame_buttons,
            text="Cancelar",
            command=self.cancel_button
        ).pack(side=tk.RIGHT, anchor='w')

    def find(self):
        self.roles = self.role_manager.display()
        # janela principal.
        tk.Label(
            self.root,
            text="Buscar candidato",
            font=("Arial", 14)
        ).pack(pady=20)
        
        # frame para os campos de entrada.
        self.role_options = [role['name'] for role in self.roles]
        tk.Label(
            self.root,
            text="Cargo",
            font=("Arial", 10)
        ).pack(anchor='w')
        self.role = ttk.Combobox(
            self.root,
            values=self.role_options,
            state="readonly"
        )
        self.role.pack(
            pady=5,
            anchor='w'
        )

        tk.Label(
            self.root,
            text="Número",
            font=("Arial", 10)
        ).pack(anchor='w')
        self.number = tk.Entry(
            self.root,
            width=30
        )
        self.number.pack(
            pady=5,
            anchor='w'
        )
        
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # botões que abrem as janelas de cada módulo.
        tk.Button(
            frame_buttons,
            text="Buscar candidato",
            command=self.find_candidate_button
        ).pack(side=tk.LEFT, anchor='w')
        tk.Button(
            frame_buttons,
            text="Cancelar",
            command=self.cancel_button
        ).pack(side=tk.RIGHT, anchor='w')

    def find_all(self):
        # janela principal.
        tk.Label(
            self.root,
            text="Essa é a página de candidatos",
            font=("Arial", 14)
        ).pack(pady=20)
        
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # botões que abrem as janelas de cada módulo.
        tk.Button(
            frame_buttons,
            text="Botão",
            command=self.cancel_button
        ).pack(side=tk.LEFT, padx=10)

    # botões de ação.
    def create_candidate_button(self):
        self.candidate_manager.create(
            self.name.get(),
            self.number.get(),
            self.role.get(),
            self.photo.get(),
            self.vice.get(),
            self.vice_photo.get(),
        )
        messagebox.showinfo(
            "Candidato cadastrado",
            "O candidato foi cadastrado com sucesso!"
        )
        self.root.destroy()

    def remove_candidate_button(self):
        self.candidate_manager.remove(
            self.role.get(),
            self.number.get()
        )
        messagebox.showinfo(
            "Candidato removido",
            "O candidato foi removido com sucesso!"
        )
        self.root.destroy()

    def find_candidate_button(self):
        self.candidate = self.candidate_manager.find(
            self.role.get(),
            self.number.get()
        )
        
        if self.candidate is None:
            messagebox.showerror(
                "Erro",
                "Candidato não encontrado."
            )
            return
        
        messagebox.showinfo(
            "Dados do candidato",
            f"Nome: {self.candidate['name']}\n"
            f"Cargo: {self.candidate['role']}\n"
            f"Número: {self.candidate['number']}"
            f"Vice: {self.candidate['vice']}"
        )
        self.root.destroy()

    def toggle_vice_fields(self, event=None):
        selected_role_name = self.role.get()
        selected_role = next((role for role in self.roles if role['name'] == selected_role_name), None)

        if selected_role and selected_role.get('vice', False):
            self.vice_label.pack(anchor='w')
            self.vice.pack(pady=5, anchor='w')
            self.vice_photo_label.pack(anchor='w')
            self.frame_vice_photo.pack(anchor='w')
        else:
            self.vice_label.pack_forget()
            self.vice.pack_forget()
            self.vice_photo_label.pack_forget()
            self.frame_vice_photo.pack_forget()
    
    
    def select_photo(self):
        filepath = filedialog.askopenfilename(
            parent=self.root,
            title="Selecione a foto do candidato",
            filetypes=(("Arquivos PNG", "*.png"), ("Todos os arquivos", "*.*"))
        )
        if filepath:
            self.photo.delete(0, tk.END)
            self.photo.insert(0, filepath)

    def select_vice_photo(self):
        filepath = filedialog.askopenfilename(
            parent=self.root,
            title="Selecione a foto do vice",
            filetypes=(("Arquivos PNG", "*.png"), ("Todos os arquivos", "*.*"))
        )
        if filepath:
            self.vice_photo.delete(0, tk.END)
            self.vice_photo.insert(0, filepath)

    def cancel_button(self):
        self.root.destroy()