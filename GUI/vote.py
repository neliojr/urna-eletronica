import tkinter as tk
from PIL import ImageTk, Image
from candidate import CandidateManager
from role import RoleManager
from voter import VoterManager

class VoteWindow:
    def __init__(self, root, voter_id):
        self.role_manager = RoleManager()
        self.candidate_manager = CandidateManager()
        self.voter_manager = VoterManager()

        self.voter_id = voter_id

        self.root = root
        self.root.title("Votar")
        self.root.attributes('-fullscreen', True)
        
        self.current_round = 0
        self.total_rounds = self.role_manager.count() - 1
        
        # iniciar o primeiro voto.
        self.start_vote_for_current_round()

    def start_vote_for_current_round(self):
        # limpa todos os widgets existentes.
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # obtém o cargo atual.
        self.current_role = self.role_manager.display()[self.current_round]
        
        # inicia a votação para o cargo atual
        self.vote()

    def vote(self):
        self.number = ''
        self.incomplet_number = '█ ' * (self.current_role['digits'] - len(self.number))
        self.name = ''

        # carregando e convertendo a imagem.
        self.imagem = Image.open("./data/foto.png")
        self.imagem = ImageTk.PhotoImage(self.imagem)

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
        self.label_imagem = tk.Label(self.root, image=self.imagem)
        self.label_imagem.pack()

        self.label_number = tk.Label(
            self.root,
            text=f"{self.number}{self.incomplet_number}",
            font=("Arial", 20)
        )
        self.label_number.pack(padx=5, anchor='w')

        self.label_name = tk.Label(
            self.root,
            text=f"{self.name}",
            font=("Arial", 20)
        )
        self.label_name.pack(padx=5, anchor='w')
        
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

    def read_keyboard(self, event):
        if len(self.number) < self.current_role['digits']:
            if event.keysym == '0' or event.keysym == 'KP_0':
                self.key = '0'
            elif event.keysym == '1' or event.keysym == 'KP_1':
                self.key = '1'
            elif event.keysym == '2' or event.keysym == 'KP_2':
                self.key = '2'
            elif event.keysym == '3' or event.keysym == 'KP_3':
                self.key = '3'
            elif event.keysym == '4' or event.keysym == 'KP_4':
                self.key = '4'
            elif event.keysym == '5' or event.keysym == 'KP_5':
                self.key = '5'
            elif event.keysym == '6' or event.keysym == 'KP_6':
                self.key = '6'
            elif event.keysym == '7' or event.keysym == 'KP_7':
                self.key = '7'
            elif event.keysym == '8' or event.keysym == 'KP_8':
                self.key = '8'
            elif event.keysym == '9' or event.keysym == 'KP_9':
                self.key = '9'
            elif event.keysym == 'BackSpace':
                self.number = ''
            else:
                return
        else:
            if event.keysym == 'BackSpace':
                self.number = ''
            elif event.keysym == 'Return':
                # lógica para confirmar e avançar para o próximo cargo.
                self.confirm_vote()
                return
            else:
                return

        if event.keysym != 'BackSpace':
            self.number += self.key

        self.incomplet_number = '█ ' * (self.current_role['digits'] - len(self.number))
        self.label_number.config(
            text=f"Número: {self.number} {self.incomplet_number}",
            font=("Arial", 20)
        )

        if len(self.number) == self.current_role['digits']:
            candidate = self.candidate_manager.find(self.current_role['name'], self.number)
            
            if candidate != None:
                self.label_name.config(
                    text=f"Nome: {candidate['name']}",
                    font=("Arial", 20)
                )
            else:
                self.label_name.config(
                    text=f"VOTO NULO!",
                    font=("Arial", 20)
                )
                
        
        self.imagem = Image.open("./data/foto2.png")
        self.imagem = ImageTk.PhotoImage(self.imagem)

        self.label_imagem.config(
            image=self.imagem
        )

    def confirm_vote(self):
        self.current_round += 1
        self.candidate_manager.add_vote(self.current_role['name'], self.number)
        
        if self.current_round <= self.total_rounds:
            self.start_vote_for_current_round()
        else:
            # todos os cargos foram votados, fecha a janela.
            self.root.destroy()

    def cancel_button(self):
        self.root.destroy()