# Importações necessárias para a interface gráfica e funcionalidades do sistema
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk, scrolledtext
from candidate import CandidateManager  # Gerenciador de candidatos
from config import ConfigManager  # Gerenciador de configurações
from role import RoleManager  # Gerenciador de cargos
from voter import VoterManager  # Gerenciador de eleitores
from GUI.vote import VoteWindow  # Janela de votação
from datetime import datetime  # Para manipulação de data/hora
from fpdf import FPDF  # Para geração de PDFs
import uuid  # Para geração de códigos únicos

class ElectionWindow:
    def __init__(self, root):
        # Inicializa todos os gerenciadores necessários
        self.role_manager = RoleManager()  # Gerencia cargos políticos
        self.candidate_manager = CandidateManager()  # Gerencia candidatos
        self.voter_manager = VoterManager()  # Gerencia eleitores
        self.config_manager = ConfigManager()  # Gerencia configurações do sistema

        self.waiting_voter = False # Indica se tem eleitor votando

        # Configuração da janela principal
        self.root = root
        self.root.withdraw()  # Esconde a janela inicialmente
        self.root.title("Liberar voto")  # Título da janela

        # Verifica se é o primeiro acesso (sem votos registrados)
        if self.has_no_votes():
            # Mostra a zerésima (boletim inicial vazio)
            self.show_bulletin_window('Zerésima', show_validate_after=True,)
        else:
            # Se já houver votos, mostra a janela principal
            self.root.deiconify()
            self.validate_voter()  # Inicia processo de validação do eleitor

    def has_no_votes(self):
        """Verifica se não há votos registrados para nenhum candidato"""
        candidates = self.candidate_manager.display()
        return all(candidate['votes'] == 0 for candidate in candidates)

    def show_bulletin_window(self, name, show_validate_after=False):
        """Exibe uma janela com o boletim de urna"""
        bulletin_window = tk.Toplevel(self.root)  # Cria janela secundária
        bulletin_window.title(name)  # Define título da janela
        
        # Configura ação ao fechar a janela
        bulletin_window.protocol("WM_DELETE_WINDOW", 
            lambda: self.on_bulletin_close(bulletin_window, show_validate_after))
        
        # Gera e exibe o conteúdo do boletim
        self.get_bulletin(name, bulletin_window)

    def on_bulletin_close(self, window, show_validate_after):
        """Lida com o fechamento da janela de boletim"""
        window.destroy()  # Fecha a janela
        if show_validate_after:
            self.root.deiconify()  # Mostra janela principal
            self.validate_voter()  # Inicia validação do eleitor

    def validate_voter(self):
        """Cria interface para validação do eleitor"""
        # Cria barra de menu
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Adiciona contador de votantes no menu
        self.remaining_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(
            label=f"{self.voter_manager.count_voted()}/{self.voter_manager.count_by_section(str(int(self.config_manager.get()['section'])))}"
        )

        # Rótulo com instruções
        tk.Label(
            self.root,
            text="Digite o ID do eleitor para liberar o voto",
            font=("Arial", 14)
        ).pack(pady=10, anchor='w')

        # Campo para inserção do ID do eleitor
        tk.Label(
            self.root,
            text="ID do eleitor",
            font=("Arial", 10)
        ).pack(anchor='w')
        
        self.voter_id = tk.Entry(self.root, width=45)
        self.voter_id.pack(pady=5, anchor='w')

        # Frame para os botões
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # Botão para continuar com a validação
        tk.Button(
            frame_buttons,
            text="Continuar",
            command=self.validate_button
        ).pack(side=tk.LEFT, anchor='w')
        
        # Botão para cancelar a operação
        tk.Button(
            frame_buttons,
            text="Cancelar",
            command=self.cancel_button
        ).pack(side=tk.RIGHT, anchor='w')
        
        # Botão para encerrar a eleição
        tk.Button(
            frame_buttons,
            text="Encerrar eleição",
            command=self.end_election
        ).pack(side=tk.RIGHT, anchor='w')

    def validate_button(self):
        """Valida o eleitor e inicia o processo de votação"""
        voter_id = self.voter_id.get()
        validate = self.voter_manager.validate(voter_id)

        if self.waiting_voter:
            # Mostra mensagem de erro se eleitor inválido
            messagebox.showerror(
                "Eleitor votando",
                "Já tem um eleitor votando, aguarde o eleitor votar."
            )

            return

        if validate and int(self.voter_manager.find(voter_id)['section']) == int(self.config_manager.get()['section']):
            # Marca como tem um eleitor votando
            self.waiting_voter = True

            # Abre janela de votação
            vote_window = tk.Toplevel(self.root)
            VoteWindow(vote_window, voter_id)
            
            # Limpa campo de ID imediatamente
            self.voter_id.delete(0, tk.END)

            # Aguarda a janela de votação fechar e atualiza o contador
            self.root.wait_window(vote_window)  # Espera a janela de votação ser destruída

            self.voter_manager = VoterManager()
            
            # Atualiza o contador no menu após o voto
            self.menu_bar.entryconfigure(1, 
                label=f"{self.voter_manager.count_voted()}/{self.voter_manager.count_by_section(str(self.config_manager.get()['section']))}")
            
            self.waiting_voter = False
        else:
            # Mostra mensagem de erro se eleitor inválido
            messagebox.showerror(
                "Eleitor votou",
                "O eleitor informado já votou ou não está cadastrado!"
            )

    def end_election(self):
        """Processo de encerramento da eleição"""
        if self.voter_id.get() == self.config_manager.get()['admin_pass']:
            # Mostra boletim final se senha estiver correta
            self.show_bulletin_window('Boletim de Urna')
        else:
            # Mensagem de erro para senha incorreta
            messagebox.showerror(
                "Senha inválida",
                "A senha do administrador está incorreta."
            )

    def get_bulletin(self, name, window):
        """Prepara a interface do boletim de urna"""
        # Título do boletim
        label_titulo = tk.Label(window, text=name.upper(), font=("Arial", 14, "bold"))
        label_titulo.pack(pady=10)

        # Área de texto rolável para o boletim
        texto_boletim = scrolledtext.ScrolledText(
            window,
            wrap=tk.WORD,
            width=70,
            height=20,
            font=("Courier New", 10)
        )
        texto_boletim.pack(padx=10, pady=5)
        # Insere conteúdo gerado no widget de texto
        texto_boletim.insert(tk.INSERT, self.generate_bulletin(name))

        # Botão para salvar em PDF
        botao_salvar = ttk.Button(
            window,
            text="Salvar em PDF",
            command=lambda: self.save_pdf(name, texto_boletim.get("1.0", tk.END))
        )
        botao_salvar.pack(pady=10)

    def generate_bulletin(self, name):
        """Gera o conteúdo textual do boletim de urna"""
        # Recarrega gerenciadores para garantir dados atualizados
        self.role_manager = RoleManager()
        self.candidate_manager = CandidateManager()
        self.voter_manager = VoterManager()
        self.config_manager = ConfigManager()

        # Obtém informações atuais
        date = datetime.now()
        section = str(self.config_manager.get()['section'])
        authentication_code = str(uuid.uuid4())  # Gera código único

        # Obtém dados para o boletim
        roles = self.role_manager.display()
        candidates = self.candidate_manager.display()
        total_aptos = self.voter_manager.count_by_section(section)
        total_apurado = self.voter_manager.count_voted_by_section(section)
        faltosos = total_aptos - total_apurado

        # Formata data e hora
        formatted_date = f"{date.day:02d}/{date.month:02d}/{date.year}"
        formatted_time = f"{date.hour:02d}:{date.minute:02d}:{date.second:02d}"

        # Cabeçalho do boletim
        bulletin = [
            "***************************************",
            f"*{name.upper().center(37)}*",
            "***************************************",
            f"Data {formatted_date.rjust(34)}",
            f"Horário {formatted_time.rjust(31)}",
            f"Seção {str(section).zfill(4).rjust(33)}",
            "",
            f"Eleitores Aptos {str(total_aptos).zfill(4).rjust(23)}",
            f"Comparecimento {str(total_apurado).zfill(4).rjust(24)}",
            f"Eleitores faltosos {str(faltosos).zfill(4).rjust(20)}",
            "",
            "=" * 39
        ]

        # Seções por cargo político
        for role in roles:
            # Título do cargo
            role_title = f"{role['name'].upper()}".center(39, "-")
            bulletin.extend(["", role_title])
            
            # Cabeçalho da tabela
            bulletin.append(
                "Nome do Candidato".ljust(25) + 
                "Nº".center(5) + 
                "Votos".rjust(8)
            )
            
            # Lista de candidatos e votos
            roll_call_votes = 0
            for candidate in candidates:
                if candidate['role'] == role['name']:
                    roll_call_votes += candidate['votes']
                    votes_text = str(candidate['votes']).zfill(4)
                    bulletin.append(
                        f"  {candidate['name'][:22]}".ljust(25) +
                        f"{candidate['number']}".center(5) +
                        votes_text.rjust(8)
                    )

            # Totais para o cargo
            bulletin.extend([
                "",
                "-" * 39,
                "Eleitores Aptos"+ f"{str(total_aptos).zfill(4).rjust(23)}",
                f"Total Apurado" + f"{str(total_apurado).zfill(4).rjust(25)}",
                f"Votos Nominais" + f"{str(roll_call_votes).zfill(4).rjust(24)}",
                f"Brancos/Nulos" + f"{str(total_apurado - roll_call_votes).zfill(4).rjust(25)}",
                "",
                "=" * 39
            ])

        # Rodapé com código de autenticação
        bulletin.extend([
            "",
            "Código de autenticação:",
            f"{authentication_code}",
            "***************************************"
        ])

        return "\n".join(bulletin)
    
    def save_pdf(self, name, conteudo):
        """Salva o boletim em arquivo PDF"""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Courier", size=12)
        pdf.multi_cell(0, 10, conteudo)
        
        # Gera nome do arquivo com timestamp
        nome_arquivo = f"{name.lower()}{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(nome_arquivo)
        messagebox.showinfo("Sucesso", f"PDF salvo como: {nome_arquivo}")

    def cancel_button(self):
        """Fecha a aplicação"""
        self.root.destroy()