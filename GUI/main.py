# Importações necessárias para a interface gráfica e módulos do sistema
import tkinter as tk
from tkinter import messagebox  # Para exibir mensagens de diálogo

# Importações das janelas específicas do sistema
from GUI.election import ElectionWindow  # Janela de votação
from GUI.voter import VoterWindow  # Janela de gerenciamento de eleitores
from GUI.candidate import CandidateWindow  # Janela de gerenciamento de candidatos
from GUI.role import RoleWindow  # Janela de gerenciamento de cargos
from config import ConfigManager  # Gerenciador de configurações do sistema

class Application:
    def __init__(self, root):
        """Inicializa a aplicação principal da urna eletrônica"""
        # Instancia o gerenciador de configurações
        self.config = ConfigManager()

        # Configuração da janela principal
        self.root = root
        self.root.title("Urna Eletrônica")  # Título da janela
        self.root.geometry("600x400")  # Dimensões iniciais da janela
        
        # Cria o menu principal
        self.menu()

    def menu(self):
        """Configura o menu principal da aplicação"""
        # Cria a barra de menu principal
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Menu "Cargos" - Gerencia os cargos políticos disponíveis
        role_menu = tk.Menu(
            menu_bar,
            tearoff=0  # Impede que o menu seja destacável
        )
        menu_bar.add_cascade(
            label="Cargos",
            menu=role_menu,
            underline=0  # Permite acesso rápido com Alt+C
        )

        # Itens do menu Cargos
        role_menu.add_command(
            label="Novo",
            command=self.open_create_role_window  # Abre janela para criar cargo
        )
        role_menu.add_command(
            label="Remover",
            command=self.open_remove_role_window  # Abre janela para remover cargo
        )
        role_menu.add_command(
            label="Buscar",
            command=self.open_find_role_window  # Abre janela para buscar cargo
        )
        role_menu.add_command(
            label="Listar"  # TODO: Implementar listagem de cargos
        )

        # Menu "Candidatos" - Gerencia os candidatos
        candidate_menu = tk.Menu(
            menu_bar,
            tearoff=0
        )
        menu_bar.add_cascade(
            label="Candidatos",
            menu=candidate_menu,
            underline=1  # Atalho Alt+A
        )

        # Itens do menu Candidatos
        candidate_menu.add_command(
            label="Novo",
            command=self.open_create_candidate_window
        )
        candidate_menu.add_command(
            label="Remover",
            command=self.open_remove_candidate_window
        )
        candidate_menu.add_command(
            label="Buscar",
            command=self.open_find_candidate_window
        )
        candidate_menu.add_command(
            label="Listar"  # TODO: Implementar listagem de candidatos
        )

        # Menu "Eleitores" - Gerencia os eleitores cadastrados
        voter_menu = tk.Menu(
            menu_bar,
            tearoff=0
        )
        menu_bar.add_cascade(
            label="Eleitores",
            menu=voter_menu,
            underline=0  # Atalho Alt+E
        )

        # Itens do menu Eleitores
        voter_menu.add_command(
            label="Novo",
            command=self.open_create_voter_window
        )
        voter_menu.add_command(
            label="Remover",
            command=self.open_remove_voter_window
        )
        voter_menu.add_command(
            label="Buscar",
            command=self.open_find_voter_window
        )
        voter_menu.add_command(
            label="Listar"  # TODO: Implementar listagem de eleitores
        )

        # Menu "Configurações" - Opções do sistema
        config_menu = tk.Menu(
            menu_bar,
            tearoff=0
        )
        menu_bar.add_cascade(
            label="Configurações",
            menu=config_menu,
            underline=1  # Atalho Alt+O
        )

        # Itens do menu Configurações
        config_menu.add_command(
            label="Alterar número da seção"  # TODO: Implementar alteração de seção
        )
        config_menu.add_command(
            label="Alterar número de dígitos do eleitor"  # TODO: Implementar
        )
        config_menu.add_command(
            label="Alterar senha do administrador"  # TODO: Implementar
        )
        config_menu.add_command(
            label="Mudar para TUI",  # Alternar para interface textual
            command=self.change_to_tui
        )
        config_menu.add_command(
            label="Procurar atualizações",  # Verificar atualizações
            command=self.update_program
        )
        config_menu.add_command(
            label="Apagar todos os dados",  # Limpar todos os dados
            command=self.delete_all_data
        )

        # Conteúdo principal da janela
        tk.Label(
            self.root,
            text="Clique no botão para iniciar a eleição",
            font=("Arial", 14)
        ).pack(pady=20)  # Rótulo com instruções
        
        # Frame para os botões principais
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # Botão para iniciar o processo de votação
        tk.Button(
            frame_buttons,
            text="Iniciar Eleição",
            command=self.start_election
        ).pack(side=tk.LEFT, padx=10)

    def start_election(self):
        """Inicia o processo de votação"""
        self.root.destroy()  # Fecha a janela atual
        election_window = tk.Tk()  # Cria nova janela
        ElectionWindow(election_window)  # Inicia a janela de votação
        election_window.mainloop()  # Inicia o loop principal

    # Métodos para abrir janelas de gerenciamento
    def open_create_voter_window(self):
        """Abre janela para cadastrar novo eleitor"""
        voter_window = tk.Toplevel(self.root)  # Janela secundária
        VoterWindow(voter_window, 'create')  # Modo criação

    def open_remove_voter_window(self):
        """Abre janela para remover eleitor"""
        voter_window = tk.Toplevel(self.root)
        VoterWindow(voter_window, 'remove')  # Modo remoção

    def open_find_voter_window(self):
        """Abre janela para buscar eleitor"""
        voter_window = tk.Toplevel(self.root)
        VoterWindow(voter_window, 'find')  # Modo busca

    def open_create_candidate_window(self):
        """Abre janela para cadastrar novo candidato"""
        candidate_window = tk.Toplevel(self.root)
        CandidateWindow(candidate_window, 'create')

    def open_remove_candidate_window(self):
        """Abre janela para remover candidato"""
        candidate_window = tk.Toplevel(self.root)
        CandidateWindow(candidate_window, 'remove')

    def open_find_candidate_window(self):
        """Abre janela para buscar candidato"""
        candidate_window = tk.Toplevel(self.root)
        CandidateWindow(candidate_window, 'find')

    def open_create_role_window(self):
        """Abre janela para criar novo cargo político"""
        role_window = tk.Toplevel(self.root)
        RoleWindow(role_window, 'create')

    def open_remove_role_window(self):
        """Abre janela para remover cargo político"""
        role_window = tk.Toplevel(self.root)
        RoleWindow(role_window, 'remove')

    def open_find_role_window(self):
        """Abre janela para buscar cargo político"""
        role_window = tk.Toplevel(self.root)
        RoleWindow(role_window, 'find')
    
    def change_to_tui(self):
        """Alterna para interface de texto (TUI)"""
        self.config.change_ui()  # Altera configuração
        messagebox.showinfo("Configurações", "Inicie o aplicativo novamente para aplicar as mudanças.")
        self.root.destroy()  # Fecha a aplicação

    def update_program(self):
        """Verifica atualizações disponíveis"""
        if self.config.find_update():
            messagebox.showinfo("Atualizações", "Seu aplicativo será atualizado.")
        else:
            messagebox.showinfo("Atualizações", "Seu aplicativo já está atualizado.")

    def delete_all_data(self):
        """Apaga todos os dados do sistema"""
        self.config.delete_all_data()  # Limpa os dados
        messagebox.showinfo(
            "Configurações", 
            "Todos os dados foram apagados.\n"
            "Inicie o aplicativo novamente para aplicar as mudanças."
        )
        self.root.destroy()  # Fecha a aplicação