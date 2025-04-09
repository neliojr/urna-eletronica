from time import sleep
import tkinter as tk
from tkinter import ttk
from candidate import CandidateManager
from role import RoleManager
from voter import VoterManager
from config import ConfigManager
import pygame

class VoteWindow:
    def __init__(self, root, voter_id):
        # Inicializa os gerenciadores de configuração, cargos, candidatos e eleitores
        self.config_manager = ConfigManager()
        self.role_manager = RoleManager()
        self.candidate_manager = CandidateManager()
        self.voter_manager = VoterManager()

        # Define variáveis de controle do estado da votação
        self.voted = False  # Indica se o eleitor já completou a votação
        self.voter_id = voter_id  # ID do eleitor atual
        self.root = root  # Janela principal do Tkinter
        self.root.title("Votar")  # Define o título da janela
        self.root.attributes('-fullscreen', True)  # Configura a janela em tela cheia
        
        # Controle das rodadas de votação
        self.current_round = 0  # Rodada atual de votação
        self.total_rounds = self.role_manager.count() - 1  # Total de rodadas baseado na quantidade de cargos
        self.votes = {}  # Dicionário para armazenar os votos
        
        # Variáveis para controle de animação de piscar
        self.blink_id = None  # ID do evento de piscar do dígito atual
        self.blink_state = False  # Estado atual do piscar do dígito
        self.blink_null_id = None  # ID do evento de piscar do texto "VOTO NULO"
        self.blink_null_state = False  # Estado atual do piscar do "VOTO NULO"
        self.window_active = True  # Flag para verificar se a janela está ativa
        
        # Inicia a votação para a rodada atual
        self.start_vote_for_current_round()

    def blink_null_vote(self):
        # Controla a animação de piscar do texto "VOTO NULO"
        if not self.window_active:
            return
            
        try:
            self.blink_null_state = not self.blink_null_state
            if self.blink_null_state:
                self.label_null_vote.config(fg="#7a7979")  # Cor cinza quando "desligado"
            else:
                self.label_null_vote.config(fg="black")  # Cor preta quando "ligado"
            self.blink_null_id = self.root.after(750, self.blink_null_vote)  # Agenda próxima execução
        except tk.TclError:
            self.blink_null_id = None  # Reseta o ID se houver erro

    def start_vote_for_current_round(self):
        # Inicia uma nova rodada de votação
        self.window_active = False  # Marca a janela como inativa durante a transição
        
        # Cancela a animação de piscar do "VOTO NULO" se estiver ativa
        if self.blink_null_id:
            self.root.after_cancel(self.blink_null_id)
            self.blink_null_id = None
        
        # Remove todos os widgets da janela atual
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.window_active = True  # Marca a nova janela como ativa
        self.current_role = self.role_manager.display()[self.current_round]  # Obtém o cargo atual
        self.vote()  # Inicia a interface de votação

    def vote(self):
        # Configura a interface de votação para o cargo atual
        self.number = ''  # Armazena o número digitado pelo usuário
        self.name = ''  # Armazena o nome do candidato (não usado diretamente aqui)
        self.root.bind('<Key>', self.read_keyboard)  # Vincula eventos de teclado

        # Cria rótulos informativos na parte superior
        tk.Label(self.root, text="Seu voto para", font=("Arial", 28)).pack(anchor='w', pady=10)
        tk.Label(self.root, text=self.current_role['name'], font=("Arial", 40, "bold")).pack()

        # Contêiner para os dígitos do número do candidato
        self.digits_container = tk.Frame(self.root)
        self.digits_container.pack(anchor='w', pady=(200,0))

        self.label_number_text = tk.Label(self.digits_container, text='Número: ', font=("Arial", 28), fg='#d9d9d9')
        self.label_number_text.pack(padx=(0,50), side=tk.LEFT)
        
        self.digit_frames = []  # Lista de frames para cada dígito
        self.digit_labels = []  # Lista de rótulos para cada dígito
        
        # Cria os campos de dígitos conforme a quantidade definida para o cargo
        for i in range(self.current_role['digits']):
            frame = tk.Frame(self.digits_container, width=60, height=80, 
                           highlightbackground="black", highlightthickness=2, bg="#d9d9d9")
            frame.pack_propagate(False)
            frame.pack(anchor='w', side=tk.LEFT)
            self.digit_frames.append(frame)
            
            label = tk.Label(frame, text="", font=("Arial", 50))
            label.pack(anchor='w', expand=True)
            self.digit_labels.append(label)

        # Contêiner para informações do candidato
        self.candidate_container = tk.Frame(self.root)
        self.candidate_container.pack(fill='x', expand=True, anchor='w')
        
        self.label_name = tk.Label(self.candidate_container, text="", font=("Arial", 28))
        self.label_name.pack(side='left', anchor='w')

        # Contêiner para informações do vice (se aplicável)
        self.vice_container = tk.Frame(self.root)
        self.vice_container.pack(fill='x', expand=True, anchor='w')

        self.label_vice_name = tk.Label(self.vice_container, text="", font=("Arial", 28))
        self.label_vice_name.pack(side='left', anchor='w')

        # Carrega imagens padrão vazias para candidato e vice
        self.photo_dir = tk.PhotoImage(file="")
        self.photo = tk.Label(self.candidate_container, image=self.photo_dir)
        self.photo.pack(side='right', anchor='e')

        self.vice_photo_dir = tk.PhotoImage(file="")
        self.vice_photo = tk.Label(self.vice_container, image=self.vice_photo_dir)
        self.vice_photo.pack(side='right', anchor='e')

        # Rótulo para exibir "VOTO NULO" ou mensagens de erro
        self.label_null_vote = tk.Label(self.root, text="", font=("Arial", 50))
        self.label_null_vote.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        self.highlight_current_digit()  # Destaca o dígito atual

    def highlight_current_digit(self):
        # Controla a animação de piscar do dígito atual
        if self.blink_id:
            self.root.after_cancel(self.blink_id)
            self.blink_id = None
        
        # Reseta a borda de todos os frames
        for frame in self.digit_frames:
            frame.config(highlightbackground="black", highlightthickness=2)
        
        # Aplica a animação de piscar ao dígito atual
        if len(self.number) < len(self.digit_frames):
            current_frame = self.digit_frames[len(self.number)]
            
            def blink():
                if not self.window_active:
                    return
                    
                self.blink_state = not self.blink_state
                if self.blink_state:
                    current_frame.config(highlightbackground="#d9d9d9", highlightthickness=2, bg="#d9d9d9")
                else:
                    current_frame.config(highlightbackground="black", highlightthickness=2)
                self.blink_id = self.root.after(500, blink)
            
            blink()

    def read_keyboard(self, event):
        # Processa a entrada do teclado
        if len(self.number) < self.current_role['digits']:
            # Aceita apenas números (teclado numérico ou normal)
            if event.keysym in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                              'KP_0', 'KP_1', 'KP_2', 'KP_3', 'KP_4',
                              'KP_5', 'KP_6', 'KP_7', 'KP_8', 'KP_9'):
                self.key = event.keysym[-1]
                self.number += self.key
                self.update_display(False)
            elif event.keysym == 'BackSpace':
                if len(self.number) > 0:
                    self.update_display(True)
        elif event.keysym == 'Return':
            self.confirm_vote()  # Confirma o voto com Enter
        elif event.keysym == 'BackSpace':
            self.update_display(True)  # Reinicia com Backspace

    def update_display(self, backspace):
        # Atualiza a exibição com base na entrada do usuário
        if backspace:
            self.number = ''  # Reseta o número digitado
            self.label_number_text.config(fg="#d9d9d9")  # Volta a cor padrão
            if self.blink_null_id:
                self.root.after_cancel(self.blink_null_id)
                self.blink_null_id = None
            self.label_null_vote.config(text="", fg="black")
            self.label_name.config(text="")
            self.photo_dir = tk.PhotoImage(file='')
            self.photo.config(image=self.photo_dir)

            # Reseta informações do vice, se aplicável
            if self.current_role['vice']:
                self.label_vice_name.config(text="", fg="black")
                self.vice_photo_dir = tk.PhotoImage(file='')
                self.vice_photo.config(image=self.photo_dir)
                
        # Atualiza os dígitos exibidos
        for i in range(len(self.digit_labels)):
            if i < len(self.number):
                self.digit_labels[i].config(text=self.number[i])
            else:
                self.digit_labels[i].config(text="")
        
        self.highlight_current_digit()
        
        # Remove instruções de confirmação, se existirem
        if hasattr(self, 'confirm_label'):
            self.confirm_label.destroy()
        if hasattr(self, 'separator'):
            self.separator.destroy()
        
        # Verifica o candidato quando todos os dígitos forem inseridos
        if len(self.number) == self.current_role['digits']:
            candidate = self.candidate_manager.find(self.current_role['name'], self.number)
            
            if candidate:
                # Exibe informações do candidato encontrado
                self.label_name.config(text=f"Nome: {candidate['name']}", fg="black")
                self.photo_dir = tk.PhotoImage(file=f'{self.config_manager.get()["data_dir"]}/images/{candidate["cand_id"]}.png')
                self.photo.config(image=self.photo_dir)

                # Exibe informações do vice, se aplicável
                if self.current_role['vice']:
                    self.label_vice_name.config(text=f"Vice-{self.current_role['name']}: {candidate['vice']}", fg="black")
                    self.vice_photo_dir = tk.PhotoImage(file=f'{self.config_manager.get()["data_dir"]}/images/{candidate["cand_id"]}.vice.png')
                    self.vice_photo.config(image=self.vice_photo_dir)
            else:
                # Exibe mensagem de voto nulo se o candidato não for encontrado
                self.label_null_vote.config(text="VOTO NULO")
                self.label_name.config(text="NÚMERO ERRADO")
                if not self.blink_null_id:
                    self.blink_null_vote()
            
            self.label_number_text.config(fg="black")
            
            # Exibe instruções para confirmar ou reiniciar o voto
            self.confirm_label = tk.Label(
                self.root,
                text="Aperte a tecla:\n"
                     "    ENTER para CONFIRMAR este voto\n"
                     "    BACKSPACE para REINICIAR este voto",
                font=("Arial", 16),
                justify=tk.LEFT,
                fg="black"
            )
            self.confirm_label.pack(side='bottom', anchor='w', pady=(0, 10))

            self.separator = tk.Frame(self.root, height=2, bd=1, relief=tk.SUNKEN, bg='black')
            self.separator.pack(side='bottom', fill=tk.X, pady=10, padx=20)

    def confirm_vote(self):
        # Confirma o voto e avança para a próxima rodada
        if not self.voted:
            self.votes[self.current_role['name']] = self.number  # Armazena o voto
            self.current_round += 1
            
            # Toca o som de confirmação
            pygame.mixer.init()
            pygame.mixer.Sound(f"{self.config_manager.get()['data_dir']}/sounds/confirmed_vote.wav").play()
            
            if self.current_round <= self.total_rounds:
                self.start_vote_for_current_round()  # Inicia próxima rodada
            else:
                self.voted = True
                self.save_votes_with_progress()  # Salva os votos ao final

    def save_votes_with_progress(self):
        # Salva os votos com uma barra de progresso
        self.voter_manager.voter_voted(self.voter_id)  # Marca o eleitor como votado

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.update_idletasks()

        # Exibe mensagem "Gravando" e barra de progresso
        label = tk.Label(
            self.root,
            text="Gravando",
            font=("Arial", 28)
        )
        label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        progress = ttk.Progressbar(
            self.root,
            length=400,
            mode='determinate'
        )
        progress.place(relx=0.5, rely=0.47, anchor=tk.CENTER)
        
        total_steps = len(self.votes)
        progress['maximum'] = total_steps
        progress['value'] = 0

        current_step = 0

        def save_next_vote():
            # Salva os votos um por um com animação
            nonlocal current_step
            if current_step < total_steps:
                role_name = list(self.votes.keys())[current_step]
                vote_number = self.votes[role_name]
                self.candidate_manager.add_vote(role_name, vote_number)
                current_step += 1
                progress['value'] = current_step
                self.root.update()
                self.root.after(200, save_next_vote)
            else:
                self.show_end_screen()  # Exibe tela final após salvar

        save_next_vote()

    def show_end_screen(self):
        # Exibe a tela final após a votação
        self.window_active = False  # Marca a janela como inativa
        
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Toca o som de encerramento
        pygame.mixer.Sound(f"{self.config_manager.get()['data_dir']}/sounds/end.wav").play()
        
        # Exibe mensagens "FIM" e "VOTOU"
        tk.Label(self.root, text="FIM", font=("Arial", 200)).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        tk.Label(self.root, text="VOTOU", font=("Arial", 36)).place(relx=0.98, rely=0.98, anchor=tk.SE)
        
        self.root.after(5000, self.root.destroy)  # Fecha a janela após 5 segundos