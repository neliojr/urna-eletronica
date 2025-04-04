import tkinter as tk

from GUI.voter import VoterWindow

class Application:
    def __init__(self, root):
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

        role_menu.add_command(label="Novo")
        role_menu.add_command(label="Remover")
        role_menu.add_command(label="Buscar")
        role_menu.add_command(label="Listar")

        # adiciona o menu "Candidatos" à barra de menu.
        candidate_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Candidatos", menu=candidate_menu, underline=1)

        candidate_menu.add_command(label="Novo")
        candidate_menu.add_command(label="Remover")
        candidate_menu.add_command(label="Buscar")
        candidate_menu.add_command(label="Listar")

        # adiciona o menu "Eleitores" à barra de menu.
        voter_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Eleitores", menu=voter_menu, underline=0)

        voter_menu.add_command(label="Novo", command=self.open_create_voter_window)
        voter_menu.add_command(label="Remover", command=self.open_remove_voter_window)
        voter_menu.add_command(label="Buscar")
        voter_menu.add_command(label="Listar")

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