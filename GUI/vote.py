from time import sleep
import tkinter as tk
from candidate import CandidateManager
from role import RoleManager
from voter import VoterManager
import pygame

class VoteWindow:
    def __init__(self, root, voter_id):
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

        self.blink_id = None  # variável para armazenar o ID da animação de piscar caixa de número.
        self.blink_state = False  # estado do piscar (True/False).
        
        # inicia o primeiro voto.
        self.start_vote_for_current_round()

    def start_vote_for_current_round(self):
        # limpa todos os widgets existentes.
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # obtém o cargo atual.
        self.current_role = self.role_manager.display()[self.current_round]
        
        # inicia a votação para o cargo atual.
        self.vote()

    def vote(self):
        self.number = ''
        self.name = ''

        # configurando o binding de teclado.
        self.root.bind('<Key>', self.read_keyboard)

        # janela principal.
        tk.Label(
            self.root,
            text="Seu voto para",
            font=("Arial", 28)
        ).pack(anchor='w', pady=10)

        tk.Label(
            self.root,
            text=self.current_role['name'],
            font=("Arial", 40, "bold")
        ).pack()

        # container para os dígitos.
        self.digits_container = tk.Frame(self.root)
        self.digits_container.pack(anchor='w', pady=(200,0))

        self.label_number_text = tk.Label(
            self.digits_container,
            text='Número: ',
            font=("Arial", 28),
            fg= '#d9d9d9'
        )
        self.label_number_text.pack(padx=(0,50), side=tk.LEFT)
        
        # criando os quadrados dos dígitos.
        self.digit_frames = []
        self.digit_labels = []
        
        for i in range(self.current_role['digits']):
            frame = tk.Frame(
                self.digits_container,
                width=60,
                height=80,
                highlightbackground="black",
                highlightthickness=2,
                highlightcolor="black",
                bg="#d9d9d9"
            )
            frame.pack_propagate(False)
            frame.pack(anchor='w', side=tk.LEFT)
            self.digit_frames.append(frame)
            
            # label que mostra o dígito.
            label = tk.Label(
                frame,
                text="",
                font=("Arial", 36)
            )
            label.pack(anchor='w', expand=True)
            self.digit_labels.append(label)

        # container para as informações do candidato.
        self.candidate_container = tk.Frame(self.root)
        self.candidate_container.pack(fill='x', expand=True, anchor='w')
        
        # label para o nome do candidato.
        self.label_name = tk.Label(
            self.candidate_container,
            text="",
            font=("Arial", 28)
        )
        self.label_name.pack(side='left', anchor='w')


        # container para as informações do vice.
        self.vice_container = tk.Frame(self.root)
        self.vice_container.pack(fill='x', expand=True, anchor='w')

        self.label_vice_name = tk.Label(
            self.vice_container,
            text="",
            font=("Arial", 28)
        )
        self.label_vice_name.pack(side='left', anchor='w')

        self.photo_dir = tk.PhotoImage(file="")
        self.photo = tk.Label(self.candidate_container, image=self.photo_dir)
        self.photo.pack(side='right', anchor='e')

        self.vice_photo_dir = tk.PhotoImage(file="")
        self.vice_photo = tk.Label(self.vice_container, image=self.vice_photo_dir)
        self.vice_photo.pack(side='right', anchor='e')

        # atualiza o destaque do dígito atual.
        self.highlight_current_digit()

    def highlight_current_digit(self):
        # Cancela qualquer animação de piscar existente
        if self.blink_id:
            self.root.after_cancel(self.blink_id)
            self.blink_id = None
        
        # remove destaque de todos os dígitos.
        for frame in self.digit_frames:
            frame.config(highlightbackground="black", highlightthickness=2)
        
        # destaca o dígito atual (se houver espaço).
        if len(self.number) < len(self.digit_frames):
            current_frame = self.digit_frames[len(self.number)]
            
            # Função para alternar o estado do piscar
            def blink():
                self.blink_state = not self.blink_state
                if self.blink_state:
                    current_frame.config(
                        highlightbackground="#d9d9d9",
                        highlightthickness=2,
                        bg="#d9d9d9"
                    )
                else:
                    current_frame.config(
                        highlightbackground="black",
                        highlightthickness=2
                    )
                # Agenda o próximo piscar
                self.blink_id = self.root.after(500, blink)  # 500ms = 0.5s
            
            # Inicia a animação
            blink()

    def read_keyboard(self, event):
        if len(self.number) < self.current_role['digits']:
            if event.keysym in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                              'KP_0', 'KP_1', 'KP_2', 'KP_3', 'KP_4',
                              'KP_5', 'KP_6', 'KP_7', 'KP_8', 'KP_9'):
                # extrai o número da tecla (remove o prefixo KP_ se for tecla numérica).
                self.key = event.keysym[-1]
                self.number += self.key
                
                # atualiza a exibição.
                self.update_display()
                
            elif event.keysym == 'BackSpace':
                if len(self.number) > 0:
                    self.number = ''
                    self.update_display()
        
        elif event.keysym == 'Return':
                self.confirm_vote()
        
        elif event.keysym == 'BackSpace':
            self.number = ''
            # oculta o label "Número"
            self.label_number_text.config(
                    fg="#d9d9d9"
            )

            # remove o label "Nome"
            self.label_name.config(
                    text=""
            )

            # exibe a foto do candidato na tela.
            self.photo_dir = tk.PhotoImage(file=f'')
            self.photo.config(image=self.photo_dir)

            if self.current_role['vice']:
                self.label_vice_name.config(
                    text="",
                    fg="black"
                )

                # exibe a foto do vice na tela.
                self.vice_photo_dir = tk.PhotoImage(file=f'')
                self.vice_photo.config(image=self.photo_dir)
                
            self.update_display()
        
    def update_display(self):
         # atualiza os dígitos nos quadrados.
        for i in range(len(self.digit_labels)):
            if i < len(self.number):
                self.digit_labels[i].config(text=self.number[i])
            else:
                self.digit_labels[i].config(text="")
        
        # atualiza o destaque do dígito atual.
        self.highlight_current_digit()
        
        # remove a mensagem de confirmação anterior se existir.
        if hasattr(self, 'confirm_label'):
            self.confirm_label.destroy()
            # Remove a mensagem de confirmação anterior e o separator se existirem
        if hasattr(self, 'separator'):
            self.separator.destroy()
        
        # verifica candidato quando todos os dígitos estiverem preenchidos.
        if len(self.number) == self.current_role['digits']:
            candidate = self.candidate_manager.find(self.current_role['name'], self.number)
            
            if candidate:
                # exibe o nome do candidato na tela.
                self.label_name.config(
                    text=f"Nome: {candidate['name']}",
                    fg="black"
                )

                # exibe a foto do candidato na tela.
                self.photo_dir = tk.PhotoImage(file=f'./data/images/{candidate['cand_id']}.png')
                self.photo.config(image=self.photo_dir)

                if self.current_role['vice']:
                    # exibe o nome do vice na tela.
                    self.label_vice_name.config(
                        text=f"Vice-{self.current_role['name']}: {candidate['vice']}",
                        fg="black"
                    )

                    # exibe a foto do vice na tela.
                    self.vice_photo_dir = tk.PhotoImage(file=f'./data/images/{candidate['cand_id']}.vice.png')
                    self.vice_photo.config(image=self.vice_photo_dir)
            else:
                self.label_name.config(
                    text="VOTO NULO!"
                )
                # imagem padrão para voto nulo.
                #self.image = Image.open("./data/foto2.png")
                #self.image = ImageTk.PhotoImage(self.image)
            
            # mostra o label "Número"
            self.label_number_text.config(
                    fg="black"
            )
            
            #self.label_image.config(image=self.image)
            
            # adiciona a mensagem de confirmação.
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

            # adiciona a linha horizontal antes da mensagem.
            self.separator = tk.Frame(self.root, height=2, bd=1, relief=tk.SUNKEN, bg='black')
            self.separator.pack(side='bottom', fill=tk.X, pady=10, padx=20)

    def confirm_vote(self):
        if not self.voted:
            self.current_round += 1
            self.candidate_manager.add_vote(self.current_role['name'], self.number)
            
            if self.current_round <= self.total_rounds:
                pygame.mixer.init()
                pygame.mixer.Sound("./data/sounds/confirmed_vote.wav").play()
                self.start_vote_for_current_round()
            else:
                self.voted = True
                # tocar som de finalização.
                pygame.mixer.init()
                pygame.mixer.Sound("./data/sounds/end.wav").play()
                
                # Limpa a tela
                for widget in self.root.winfo_children():
                    widget.destroy()
                
                # exibe mensagem "FIM" centralizada.
                tk.Label(
                    self.root,
                    text="FIM",
                    font=("Arial", 200)
                ).place(relx=0.5, rely=0.4, anchor=tk.CENTER)
            
                # label "VOTOU" no canto inferior direito.
                tk.Label(
                    self.root,
                    text="VOTOU",
                    font=("Arial", 36)
                ).place(relx=0.98, rely=0.98, anchor=tk.SE)
                
                # fecha após 5 segundos.
                self.root.after(5000, self.root.destroy)
        else:
            pass

    def cancel_button(self):
        self.root.destroy()