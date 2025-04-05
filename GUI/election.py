import tkinter as tk
from tkinter import messagebox
from voter import VoterManager
from GUI.vote import VoteWindow

class ElectionWindow:
    def __init__(self, root):
        self.voter_manager = VoterManager()

        self.root = root
        self.root.title("Liberar voto")
        
        # iniciar o primeiro voto.
        self.validate_voter()

    def validate_voter(self):
        # janela principal.
        tk.Label(
            self.root,
            text="Digite o ID do eleitor para liberar o voto",
            font=("Arial", 14)
        ).pack(pady=10, anchor='w')

        # frame para os campos de entrada.
        tk.Label(
            self.root,
            text="ID do eleitor",
            font=("Arial", 10)
        ).pack(anchor='w')
        self.voter_id = tk.Entry(
            self.root,
            width=45
        )
        self.voter_id.pack(
            pady=5,
            anchor='w'
        )

        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack()

        # botões de ação da janela.
        tk.Button(
            frame_buttons,
            text="Continuar",
            command=self.validate_button
        ).pack(side=tk.LEFT, anchor='w')
        tk.Button(
            frame_buttons,
            text="Cancelar",
            command=self.cancel_button
        ).pack(side=tk.RIGHT, anchor='w')

    def validate_button(self):
        validate = self.voter_manager.validate(
            self.voter_id.get()
        )

        if validate:
            self.voter_manager.voter_voted(
                self.voter_id.get()
            )
            
            self.voter_manager = VoterManager()
            vote_window = tk.Toplevel(self.root)
            VoteWindow(vote_window, self.voter_id.get())
        else:
            messagebox.showerror(
                "Eleitor votou",
                "O eleitor informado já votou ou não está cadastrado!"
            )

    def cancel_button(self):
        self.root.destroy()