import tkinter as tk
from PIL import ImageTk, Image
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

        # carregando e convertendo a imagem.
        #self.image = Image.open("./data/foto.png")
        #self.image = ImageTk.PhotoImage(self.image)

        # configurando o binding de teclado.
        self.root.bind('<Key>', self.read_keyboard)

        # janela principal.
        tk.Label(
            self.root,
            text="Seu voto para",
            font=("Arial", 14)
        ).pack(pady=10, anchor='w')

        tk.Label(
            self.root,
            text=self.current_role['name'],
            font=("Arial", 20)
        ).pack(padx=75, anchor='w')

        # exibindo a imagem.
        #self.label_image = tk.Label(self.root, image=self.image)
        #self.label_image.pack()

        # container para os dígitos.
        self.digits_container = tk.Frame(self.root)
        self.digits_container.pack(anchor='w', pady=20)
        
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
                bg="white"
            )
            frame.pack_propagate(False)
            frame.pack(anchor='w', side=tk.LEFT, padx=5)
            self.digit_frames.append(frame)
            
            # label que mostra o dígito.
            label = tk.Label(
                frame,
                text="",
                font=("Arial", 36),
                bg="white"
            )
            label.pack(anchor='w', expand=True)
            self.digit_labels.append(label)
        
        # label para o nome do candidato.
        self.label_name = tk.Label(
            self.root,
            text="",
            font=("Arial", 20)
        )
        self.label_name.pack(anchor='w', pady=20)

        # atualiza o destaque do dígito atual.
        self.highlight_current_digit()

    def highlight_current_digit(self):
        # remove destaque de todos os dígitos.
        for frame in self.digit_frames:
            frame.config(highlightbackground="black", highlightthickness=2)
        
        # destaca o dígito atual (se houver espaço).
        if len(self.number) < len(self.digit_frames):
            self.digit_frames[len(self.number)].config(
                highlightbackground="#0066cc",
                highlightthickness=3
            )

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
            self.label_name.config(
                    text=""
            )
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
                self.label_name.config(
                    text=f"Nome: {candidate['name']}",
                    fg="black"
                )
                # atualiza imagem do candidato.
                #self.image = Image.open(f"./data/candidates/{candidate['image']}")
                #self.image = ImageTk.PhotoImage(self.image)
            else:
                self.label_name.config(
                    text="VOTO NULO!"
                )
                # imagem padrão para voto nulo.
                #self.image = Image.open("./data/foto2.png")
                #self.image = ImageTk.PhotoImage(self.image)
            
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
                pygame.mixer.Sound("./data/sounds/voto_confirmado.wav").play()
                self.start_vote_for_current_round()
            else:
                self.voted = True
                # tocar som de finalização.
                pygame.mixer.init()
                pygame.mixer.Sound("./data/sounds/fim.wav").play()
                
                # Limpa a tela
                for widget in self.root.winfo_children():
                    widget.destroy()
                
                # exibe mensagem "FIM" centralizada.
                tk.Label(
                    self.root,
                    text="FIM",
                    font=("Arial", 200, "bold")
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