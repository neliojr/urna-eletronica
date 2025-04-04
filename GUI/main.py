import tkinter as tk
from tkinter import messagebox

from GUI.voter import VoterWindow
from GUI.candidate import CandidateWindow
from GUI.role import RoleWindow
from config import ConfigManager

class Application:
    def __init__(self, root):
        self.config = ConfigManager()

        self.root = root
        self.root.title("Urna Eletrônica")
        self.root.geometry("600x400")
        self.menu()

    def menu(self):
        # cria a barra de menu principal.
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # adiciona o menu "Cargos" à barra de menu.
        role_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Cargos", menu=role_menu, underline=0)

        role_menu.add_command(label="Novo", command=self.open_create_role_window)
        role_menu.add_command(label="Remover", command=self.open_remove_role_window)
        role_menu.add_command(label="Buscar", command=self.open_find_role_window)
        role_menu.add_command(label="Listar")

        # adiciona o menu "Candidatos" à barra de menu.
        candidate_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Candidatos", menu=candidate_menu, underline=1)

        candidate_menu.add_command(label="Novo", command=self.open_create_candidate_window)
        candidate_menu.add_command(label="Remover", command=self.open_remove_candidate_window)
        candidate_menu.add_command(label="Buscar", command=self.open_find_candidate_window)
        candidate_menu.add_command(label="Listar")

        # adiciona o menu "Eleitores" à barra de menu.
        voter_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Eleitores", menu=voter_menu, underline=0)

        voter_menu.add_command(label="Novo", command=self.open_create_voter_window)
        voter_menu.add_command(label="Remover", command=self.open_remove_voter_window)
        voter_menu.add_command(label="Buscar", command=self.open_find_voter_window)
        voter_menu.add_command(label="Listar")

        # adiciona o menu "Configurações" à barra de menu.
        config_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Configurações", menu=config_menu, underline=1)

        config_menu.add_command(label="Alterar número da seção")
        config_menu.add_command(label="Alterar número de dígitos do eleitor")
        config_menu.add_command(label="Alterar senha do administrador")
        config_menu.add_command(label="Mudar para TUI", command=self.change_to_tui)
        config_menu.add_command(label="Procurar atualizações", command=self.update_program)

        # janela principal.
        tk.Label(self.root, text="Clique no botão para iniciar a eleição", font=("Arial", 14)).pack(pady=20)
        
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # botões que abrem as janelas de cada módulo.
        tk.Button(frame_buttons, text="Iniciar Eleição", command=self.start_election).pack(side=tk.LEFT, padx=10)

    def start_election(self):
        input("clicou")

    def open_create_voter_window(self):
        # abre a janela de cadastro de eleitores.
        voter_window = tk.Toplevel(self.root)
        VoterWindow(voter_window, 'create')

    def open_remove_voter_window(self):
        # abre a janela de cadastro de eleitores.
        voter_window = tk.Toplevel(self.root)
        VoterWindow(voter_window, 'remove')

    def open_find_voter_window(self):
        # abre a janela de cadastro de eleitores.
        voter_window = tk.Toplevel(self.root)
        VoterWindow(voter_window, 'find')

    def open_create_candidate_window(self):
        # abre a janela de cadastro de eleitores.
        candidate_window = tk.Toplevel(self.root)
        CandidateWindow(candidate_window, 'create')

    def open_remove_candidate_window(self):
        # abre a janela de cadastro de eleitores.
        candidate_window = tk.Toplevel(self.root)
        CandidateWindow(candidate_window, 'remove')

    def open_find_candidate_window(self):
        # abre a janela de cadastro de eleitores.
        candidate_window = tk.Toplevel(self.root)
        CandidateWindow(candidate_window, 'find')

    def open_create_role_window(self):
        # abre a janela de cadastro de eleitores.
        role_window = tk.Toplevel(self.root)
        RoleWindow(role_window, 'create')

    def open_remove_role_window(self):
        # abre a janela de cadastro de eleitores.
        role_window = tk.Toplevel(self.root)
        RoleWindow(role_window, 'remove')

    def open_find_role_window(self):
        # abre a janela de cadastro de eleitores.
        role_window = tk.Toplevel(self.root)
        RoleWindow(role_window, 'find')
    
    def change_to_tui(self):
        # fecha a janela atual.
        self.config.change_ui()
        messagebox.showinfo("Configurações", "Inicie o aplicativo novamente para aplicar as mudanças.")
        self.root.destroy()

    def update_program(self):
        # fecha a janela atual.
        if self.config.find_update():
            messagebox.showinfo("Atualizações", "Seu aplicativo será atualizado.")
        else:
            messagebox.showinfo("Atualizações", "Seu aplicativo já está atualizado.")