# Importações necessárias para a interface gráfica
import tkinter as tk
from tkinter import messagebox  # Para exibir mensagens de diálogo
from tkinter import filedialog  # Para seleção de arquivos
from tkinter import ttk  # Para widgets temáticos mais modernos

# Importações dos gerenciadores de dados
from candidate import CandidateManager  # Gerenciador de candidatos
from role import RoleManager  # Gerenciador de cargos políticos

class CandidateWindow:
    def __init__(self, root, action):
        """Inicializa a janela de gerenciamento de candidatos"""
        # Instancia os gerenciadores de dados
        self.candidate_manager = CandidateManager()
        self.role_manager = RoleManager()

        # Configuração da janela principal
        self.root = root
        self.root.title("Candidatos")  # Define o título da janela

        # Seleciona qual tela será exibida com base na ação recebida
        if action == 'create':
            self.create()  # Tela de criação de candidato
        elif action == 'remove':
            self.remove()  # Tela de remoção de candidato
        elif action == 'find':
            self.find()  # Tela de busca de candidato
        elif action == 'find_all':
            self.find_all()  # Tela de listagem geral (ainda não implementada)

    def create(self):
        """Configura a interface para criação de novo candidato"""
        # Obtém a lista de cargos disponíveis
        self.roles = self.role_manager.display()
        
        # Frame principal para o conteúdo
        self.content = tk.Frame(self.root)
        self.content.pack()

        # Título da tela
        tk.Label(
            self.content,
            text="Cadastrar candidato",
            font=("Arial", 14)
        ).pack(pady=20, anchor='w')

        # Campo para nome do candidato
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

        # Campo para número do candidato
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

        # Combobox para seleção do cargo
        self.role_options = [role['name'] for role in self.roles]
        tk.Label(
            self.content,
            text="Cargo",
            font=("Arial", 10)
        ).pack(anchor='w')
        self.role = ttk.Combobox(
            self.content,
            values=self.role_options,
            state="readonly"  # Impede edição direta
        )
        self.role.pack(
            pady=5,
            anchor='w'
        )

        # Vincula evento de seleção para mostrar/ocultar campos de vice
        self.role.bind("<<ComboboxSelected>>", self.toggle_vice_fields)

        # Campo para seleção da foto do candidato
        tk.Label(
            self.content,
            text="Foto",
            font=("Arial", 10)
        ).pack(anchor='w')

        # Frame para o campo de foto + botão de seleção
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
            command=self.select_photo  # Abre diálogo de seleção de arquivo
        ).pack(side=tk.LEFT, padx=5)

        # Campos para vice (inicialmente ocultos)
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
            command=self.select_vice_photo  # Abre diálogo para foto do vice
        ).pack(side=tk.LEFT, padx=5)

        # Frame para os botões de ação
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # Botão para confirmar cadastro
        tk.Button(
            frame_buttons,
            text="Cadastrar candidato",
            command=self.create_candidate_button
        ).pack(side=tk.LEFT, anchor='w')
        # Botão para cancelar
        tk.Button(
            frame_buttons,
            text="Cancelar",
            command=self.cancel_button
        ).pack(side=tk.RIGHT, anchor='w')
    
    def remove(self):
        """Configura a interface para remoção de candidato"""
        self.roles = self.role_manager.display()
        
        # Título da tela
        tk.Label(
            self.root,
            text="Remover candidato",
            font=("Arial", 14)
        ).pack(pady=20)

        # Combobox para seleção do cargo
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

        # Campo para número do candidato a remover
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
        
        # Frame para os botões de ação
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # Botão para confirmar remoção
        tk.Button(
            frame_buttons,
            text="Remover candidato",
            command=self.remove_candidate_button
        ).pack(side=tk.LEFT, anchor='w')
        # Botão para cancelar
        tk.Button(
            frame_buttons,
            text="Cancelar",
            command=self.cancel_button
        ).pack(side=tk.RIGHT, anchor='w')

    def find(self):
        """Configura a interface para busca de candidato"""
        self.roles = self.role_manager.display()
        
        # Título da tela
        tk.Label(
            self.root,
            text="Buscar candidato",
            font=("Arial", 14)
        ).pack(pady=20)
        
        # Combobox para seleção do cargo
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

        # Campo para número do candidato a buscar
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
        
        # Frame para os botões de ação
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # Botão para confirmar busca
        tk.Button(
            frame_buttons,
            text="Buscar candidato",
            command=self.find_candidate_button
        ).pack(side=tk.LEFT, anchor='w')
        # Botão para cancelar
        tk.Button(
            frame_buttons,
            text="Cancelar",
            command=self.cancel_button
        ).pack(side=tk.RIGHT, anchor='w')

    def find_all(self):
        """Configura a interface para listagem geral de candidatos"""
        # Título da tela (implementação básica)
        tk.Label(
            self.root,
            text="Essa é a página de candidatos",
            font=("Arial", 14)
        ).pack(pady=20)
        
        # Frame para botões (implementação básica)
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # Botão de exemplo
        tk.Button(
            frame_buttons,
            text="Botão",
            command=self.cancel_button
        ).pack(side=tk.LEFT, padx=10)

    # Métodos para ações dos botões
    def create_candidate_button(self):
        """Ação do botão para criar novo candidato"""
        self.candidate_manager.create(
            self.name.get(),        # Nome do candidato
            self.number.get(),      # Número eleitoral
            self.role.get(),        # Cargo político
            self.photo.get(),       # Caminho da foto
            self.vice.get(),        # Nome do vice
            self.vice_photo.get(),  # Caminho da foto do vice
        )
        # Exibe mensagem de sucesso
        messagebox.showinfo(
            "Candidato cadastrado",
            "O candidato foi cadastrado com sucesso!"
        )
        self.root.destroy()  # Fecha a janela

    def remove_candidate_button(self):
        """Ação do botão para remover candidato"""
        self.candidate_manager.remove(
            self.role.get(),   # Cargo do candidato
            self.number.get()  # Número do candidato
        )
        # Exibe mensagem de sucesso
        messagebox.showinfo(
            "Candidato removido",
            "O candidato foi removido com sucesso!"
        )
        self.root.destroy()  # Fecha a janela

    def find_candidate_button(self):
        """Ação do botão para buscar candidato"""
        self.candidate = self.candidate_manager.find(
            self.role.get(),   # Cargo do candidato
            self.number.get() # Número do candidato
        )
        
        # Verifica se o candidato foi encontrado
        if self.candidate is None:
            messagebox.showerror(
                "Erro",
                "Candidato não encontrado."
            )
            return
        
        # Exibe informações do candidato encontrado
        messagebox.showinfo(
            "Dados do candidato",
            f"Nome: {self.candidate['name']}\n"
            f"Cargo: {self.candidate['role']}\n"
            f"Número: {self.candidate['number']}"
            f"Vice: {self.candidate['vice']}"
        )
        self.root.destroy()  # Fecha a janela

    def toggle_vice_fields(self, event=None):
        """Mostra/oculta campos de vice conforme o cargo selecionado"""
        selected_role_name = self.role.get()
        # Encontra o cargo selecionado na lista de cargos
        selected_role = next((role for role in self.roles if role['name'] == selected_role_name), None)

        # Se o cargo tem vice, mostra os campos correspondentes
        if selected_role and selected_role.get('vice', False):
            self.vice_label.pack(anchor='w')
            self.vice.pack(pady=5, anchor='w')
            self.vice_photo_label.pack(anchor='w')
            self.frame_vice_photo.pack(anchor='w')
        else:
            # Oculta os campos se o cargo não tem vice
            self.vice_label.pack_forget()
            self.vice.pack_forget()
            self.vice_photo_label.pack_forget()
            self.frame_vice_photo.pack_forget()
    
    def select_photo(self):
        """Abre diálogo para seleção da foto do candidato"""
        filepath = filedialog.askopenfilename(
            parent=self.root,
            title="Selecione a foto do candidato",
            filetypes=(("Arquivos PNG", "*.png"), ("Todos os arquivos", "*.*"))
        )
        if filepath:
            self.photo.delete(0, tk.END)
            self.photo.insert(0, filepath)  # Insere caminho no campo

    def select_vice_photo(self):
        """Abre diálogo para seleção da foto do vice"""
        filepath = filedialog.askopenfilename(
            parent=self.root,
            title="Selecione a foto do vice",
            filetypes=(("Arquivos PNG", "*.png"), ("Todos os arquivos", "*.*"))
        )
        if filepath:
            self.vice_photo.delete(0, tk.END)
            self.vice_photo.insert(0, filepath)  # Insere caminho no campo

    def cancel_button(self):
        """Fecha a janela sem realizar nenhuma ação"""
        self.root.destroy()