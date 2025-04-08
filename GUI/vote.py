from time import sleep
import tkinter as tk
from tkinter import ttk  # Importa ttk para a barra de progresso
from candidate import CandidateManager
from role import RoleManager
from voter import VoterManager
from config import ConfigManager
import pygame

class VoteWindow:
    def __init__(self, root, voter_id):
        self.config_manager = ConfigManager()
        self.role_manager = RoleManager()
        self.candidate_manager = CandidateManager()
        self.voter_manager = VoterManager()

        self.voted = False
        self.voter_id = voter_id
        self.root = root
        self.root.title("Votar")
        self.root.attributes('-fullscreen', True)
        
        self.current_round = 0
        self.total_rounds = self.role_manager.count() - 1
        self.votes = {}  # Dicionário para armazenar os votos temporariamente
        
        self.blink_id = None
        self.blink_state = False
        
        self.start_vote_for_current_round()

    def start_vote_for_current_round(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.current_role = self.role_manager.display()[self.current_round]
        self.vote()

    def vote(self):
        self.number = ''
        self.name = ''
        self.root.bind('<Key>', self.read_keyboard)

        tk.Label(self.root, text="Seu voto para", font=("Arial", 28)).pack(anchor='w', pady=10)
        tk.Label(self.root, text=self.current_role['name'], font=("Arial", 40, "bold")).pack()

        self.digits_container = tk.Frame(self.root)
        self.digits_container.pack(anchor='w', pady=(200,0))

        self.label_number_text = tk.Label(self.digits_container, text='Número: ', font=("Arial", 28), fg='#d9d9d9')
        self.label_number_text.pack(padx=(0,50), side=tk.LEFT)
        
        self.digit_frames = []
        self.digit_labels = []
        
        for i in range(self.current_role['digits']):
            frame = tk.Frame(self.digits_container, width=60, height=80, 
                           highlightbackground="black", highlightthickness=2, bg="#d9d9d9")
            frame.pack_propagate(False)
            frame.pack(anchor='w', side=tk.LEFT)
            self.digit_frames.append(frame)
            
            label = tk.Label(frame, text="", font=("Arial", 50))
            label.pack(anchor='w', expand=True)
            self.digit_labels.append(label)

        self.candidate_container = tk.Frame(self.root)
        self.candidate_container.pack(fill='x', expand=True, anchor='w')
        
        self.label_name = tk.Label(self.candidate_container, text="", font=("Arial", 28))
        self.label_name.pack(side='left', anchor='w')

        self.vice_container = tk.Frame(self.root)
        self.vice_container.pack(fill='x', expand=True, anchor='w')

        self.label_vice_name = tk.Label(self.vice_container, text="", font=("Arial", 28))
        self.label_vice_name.pack(side='left', anchor='w')

        self.photo_dir = tk.PhotoImage(file="")
        self.photo = tk.Label(self.candidate_container, image=self.photo_dir)
        self.photo.pack(side='right', anchor='e')

        self.vice_photo_dir = tk.PhotoImage(file="")
        self.vice_photo = tk.Label(self.vice_container, image=self.vice_photo_dir)
        self.vice_photo.pack(side='right', anchor='e')

        self.highlight_current_digit()

    def highlight_current_digit(self):
        if self.blink_id:
            self.root.after_cancel(self.blink_id)
            self.blink_id = None
        
        for frame in self.digit_frames:
            frame.config(highlightbackground="black", highlightthickness=2)
        
        if len(self.number) < len(self.digit_frames):
            current_frame = self.digit_frames[len(self.number)]
            
            def blink():
                self.blink_state = not self.blink_state
                if self.blink_state:
                    current_frame.config(highlightbackground="#d9d9d9", highlightthickness=2, bg="#d9d9d9")
                else:
                    current_frame.config(highlightbackground="black", highlightthickness=2)
                self.blink_id = self.root.after(500, blink)
            
            blink()

    def read_keyboard(self, event):
        if len(self.number) < self.current_role['digits']:
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
            self.confirm_vote()
        elif event.keysym == 'BackSpace':
            self.update_display(True)

    def update_display(self, backspace):
        if backspace:
            self.number = ''
            self.label_number_text.config(fg="#d9d9d9")
            self.label_name.config(text="")
            self.photo_dir = tk.PhotoImage(file='')
            self.photo.config(image=self.photo_dir)

            if self.current_role['vice']:
                self.label_vice_name.config(text="", fg="black")
                self.vice_photo_dir = tk.PhotoImage(file='')
                self.vice_photo.config(image=self.photo_dir)
                
        for i in range(len(self.digit_labels)):
            if i < len(self.number):
                self.digit_labels[i].config(text=self.number[i])
            else:
                self.digit_labels[i].config(text="")
        
        self.highlight_current_digit()
        
        if hasattr(self, 'confirm_label'):
            self.confirm_label.destroy()
        if hasattr(self, 'separator'):
            self.separator.destroy()
        
        if len(self.number) == self.current_role['digits']:
            candidate = self.candidate_manager.find(self.current_role['name'], self.number)
            
            if candidate:
                self.label_name.config(text=f"Nome: {candidate['name']}", fg="black")
                self.photo_dir = tk.PhotoImage(file=f'{self.config_manager.get()["data_dir"]}/images/{candidate["cand_id"]}.png')
                self.photo.config(image=self.photo_dir)

                if self.current_role['vice']:
                    self.label_vice_name.config(text=f"Vice-{self.current_role['name']}: {candidate['vice']}", fg="black")
                    self.vice_photo_dir = tk.PhotoImage(file=f'{self.config_manager.get()["data_dir"]}/images/{candidate["cand_id"]}.vice.png')
                    self.vice_photo.config(image=self.vice_photo_dir)
            else:
                self.label_name.config(text="VOTO NULO!")
            
            self.label_number_text.config(fg="black")
            
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
        if not self.voted:
            # Armazena o voto no dicionário temporário
            self.votes[self.current_role['name']] = self.number
            self.current_round += 1
            
            pygame.mixer.init()
            pygame.mixer.Sound(f"{self.config_manager.get()['data_dir']}/sounds/confirmed_vote.wav").play()
            
            if self.current_round <= self.total_rounds:
                self.start_vote_for_current_round()
            else:
                self.voted = True
                self.save_votes_with_progress()

    def save_votes_with_progress(self):
        # Marca eleitor como votou
        self.voter_manager.voter_voted(self.voter_id)

        # Limpa a tela
        for widget in self.root.winfo_children():
            widget.destroy()

        # Garante que a janela esteja atualizada antes de posicionar os widgets
        self.root.update_idletasks()

        # Label "Gravando..." acima da barra
        label = tk.Label(
            self.root,
            text="Gravando",
            font=("Arial", 28)
        )
        label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Barra de progresso no centro exato
        progress = ttk.Progressbar(
            self.root,
            length=400,
            mode='determinate'
        )
        progress.place(relx=0.5, rely=0.47, anchor=tk.CENTER)
        
        # Configura a barra de progresso
        total_steps = len(self.votes)
        progress['maximum'] = total_steps
        progress['value'] = 0

        current_step = 0

        def save_next_vote():
            nonlocal current_step
            if current_step < total_steps:
                role_name = list(self.votes.keys())[current_step]
                vote_number = self.votes[role_name]
                self.candidate_manager.add_vote(role_name, vote_number)
                current_step += 1
                progress['value'] = current_step
                self.root.update()  # Força atualização da interface
                self.root.after(200, save_next_vote)
            else:
                self.show_end_screen()

        save_next_vote()

    def show_end_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        pygame.mixer.Sound(f"{self.config_manager.get()['data_dir']}/sounds/end.wav").play()
        
        tk.Label(self.root, text="FIM", font=("Arial", 200)).place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        tk.Label(self.root, text="VOTOU", font=("Arial", 36)).place(relx=0.98, rely=0.98, anchor=tk.SE)
        
        self.root.after(5000, self.root.destroy)