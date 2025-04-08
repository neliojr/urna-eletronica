from time import sleep  # Importa sleep para pausas temporizadas
import tkinter as tk  # Importa Tkinter para criar interfaces gráficas
from candidate import CandidateManager  # Importa gerenciador de candidatos
from role import RoleManager  # Importa gerenciador de cargos
from voter import VoterManager  # Importa gerenciador de eleitores
import pygame  # Importa Pygame para reprodução de sons

class VoteWindow:
    # Método construtor da classe
    def __init__(self, root, voter_id):
        self.role_manager = RoleManager()  # Instancia o gerenciador de cargos
        self.candidate_manager = CandidateManager()  # Instancia o gerenciador de candidatos
        self.voter_manager = VoterManager()  # Instancia o gerenciador de eleitores

        self.voted = False  # Flag para verificar se o voto foi concluído

        self.voter_id = voter_id  # ID do eleitor atual
        self.root = root  # Janela principal
        self.root.title("Votar")  # Define o título da janela
        self.root.attributes('-fullscreen', True)  # Configura a janela em tela cheia
        
        self.current_round = 0  # Rodada atual de votação (começa em 0)
        self.total_rounds = self.role_manager.count() - 1  # Total de rodadas baseado na quantidade de cargos

        self.blink_id = None  # ID da animação de piscar da caixa de dígitos
        self.blink_state = False  # Estado da animação de piscar (ligado/desligado)
        
        # Inicia a votação para o cargo da rodada atual
        self.start_vote_for_current_round()

    # Método para iniciar a votação da rodada atual
    def start_vote_for_current_round(self):
        # Remove todos os widgets existentes na janela
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Obtém o cargo atual da lista de cargos
        self.current_role = self.role_manager.display()[self.current_round]
        
        # Inicia a interface de votação para o cargo atual
        self.vote()

    # Método para configurar a interface de votação
    def vote(self):
        self.number = ''  # Armazena os dígitos digitados pelo usuário
        self.name = ''  # Armazena o nome do candidato (não usado diretamente aqui)

        # Vincula eventos de teclado à função read_keyboard
        self.root.bind('<Key>', self.read_keyboard)

        # Título "Seu voto para"
        tk.Label(
            self.root,
            text="Seu voto para",
            font=("Arial", 28)
        ).pack(anchor='w', pady=10)  # Alinhado à esquerda com espaçamento vertical

        # Exibe o nome do cargo atual
        tk.Label(
            self.root,
            text=self.current_role['name'],
            font=("Arial", 40, "bold")
        ).pack()

        # Container para exibir os dígitos
        self.digits_container = tk.Frame(self.root)
        self.digits_container.pack(anchor='w', pady=(200,0))  # Posicionado à esquerda com espaçamento superior

        # Rótulo "Número:"
        self.label_number_text = tk.Label(
            self.digits_container,
            text='Número: ',
            font=("Arial", 28),
            fg='#d9d9d9'  # Cor inicial cinza (quase invisível)
        )
        self.label_number_text.pack(padx=(0,50), side=tk.LEFT)  # Alinhado à esquerda com espaçamento horizontal
        
        # Criação das caixas para os dígitos
        self.digit_frames = []  # Lista de frames para os dígitos
        self.digit_labels = []  # Lista de labels dentro dos frames
        
        for i in range(self.current_role['digits']):  # Para cada dígito do cargo
            frame = tk.Frame(
                self.digits_container,
                width=60,  # Largura fixa
                height=80,  # Altura fixa
                highlightbackground="black",  # Borda preta
                highlightthickness=2,  # Espessura da borda
                highlightcolor="black",
                bg="#d9d9d9"  # Fundo cinza claro
            )
            frame.pack_propagate(False)  # Impede que o frame ajuste ao conteúdo
            frame.pack(anchor='w', side=tk.LEFT)  # Alinha à esquerda
            self.digit_frames.append(frame)
            
            # Label para exibir o dígito dentro do frame
            label = tk.Label(
                frame,
                text="",
                font=("Arial", 50)
            )
            label.pack(anchor='w', expand=True)  # Centraliza o texto no frame
            self.digit_labels.append(label)

        # Container para informações do candidato
        self.candidate_container = tk.Frame(self.root)
        self.candidate_container.pack(fill='x', expand=True, anchor='w')  # Preenche horizontalmente
        
        # Label para o nome do candidato
        self.label_name = tk.Label(
            self.candidate_container,
            text="",
            font=("Arial", 28)
        )
        self.label_name.pack(side='left', anchor='w')  # Alinhado à esquerda

        # Container para informações do vice (se houver)
        self.vice_container = tk.Frame(self.root)
        self.vice_container.pack(fill='x', expand=True, anchor='w')

        # Label para o nome do vice
        self.label_vice_name = tk.Label(
            self.vice_container,
            text="",
            font=("Arial", 28)
        )
        self.label_vice_name.pack(side='left', anchor='w')

        # Imagem inicial vaz她的ia para o candidato
        self.photo_dir = tk.PhotoImage(file="")
        self.photo = tk.Label(self.candidate_container, image=self.photo_dir)
        self.photo.pack(side='right', anchor='e')  # Alinhado à direita

        # Imagem inicial vazia para o vice
        self.vice_photo_dir = tk.PhotoImage(file="")
        self.vice_photo = tk.Label(self.vice_container, image=self.vice_photo_dir)
        self.vice_photo.pack(side='right', anchor='e')

        # Inicia o destaque do dígito atual
        self.highlight_current_digit()

    # Método para destacar o dígito atual com animação de piscar
    def highlight_current_digit(self):
        # Cancela qualquer animação de piscar existente
        if self.blink_id:
            self.root.after_cancel(self.blink_id)
            self.blink_id = None
        
        # Remove o destaque de todos os frames
        for frame in self.digit_frames:
            frame.config(highlightbackground="black", highlightthickness=2)
        
        # Destaca o frame do dígito atual se ainda houver espaço
        if len(self.number) < len(self.digit_frames):
            current_frame = self.digit_frames[len(self.number)]
            
            # Função interna para alternar o estado do piscar
            def blink():
                self.blink_state = not self.blink_state
                if self.blink_state:
                    current_frame.config(
                        highlightbackground="#d9d9d9",  # Cor igual ao fundo
                        highlightthickness=2,
                        bg="#d9d9d9"
                    )
                else:
                    current_frame.config(
                        highlightbackground="black",  # Borda preta
                        highlightthickness=2
                    )
                # Agenda o próximo piscar após 500ms
                self.blink_id = self.root.after(500, blink)
            
            # Inicia a animação de piscar
            blink()

    # Método para processar entradas do teclado
    def read_keyboard(self, event):
        # Se ainda houver dígitos a preencher
        if len(self.number) < self.current_role['digits']:
            # Verifica se a tecla pressionada é um número (normal ou numpad)
            if event.keysym in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                              'KP_0', 'KP_1', 'KP_2', 'KP_3', 'KP_4',
                              'KP_5', 'KP_6', 'KP_7', 'KP_8', 'KP_9'):
                # Extrai o número da tecla (remove "KP_" se for do numpad)
                self.key = event.keysym[-1]
                self.number += self.key
                
                # Atualiza a exibição na tela
                self.update_display(False)
                
            # Se a tecla for Backspace, limpa o número
            elif event.keysym == 'BackSpace':
                if len(self.number) > 0:
                    self.update_display(True)
        
        # Se todos os dígitos estiverem preenchidos
        elif event.keysym == 'Return':
            # Confirma o voto ao pressionar Enter
            self.confirm_vote()
        
        elif event.keysym == 'BackSpace':
            self.update_display(True)  # Atualiza a tela
        
    # Método para atualizar a exibição na tela
    def update_display(self, backspace):
        if backspace:
            # Reinicia o voto ao pressionar Backspace
            self.number = ''

            self.label_number_text.config(fg="#d9d9d9")  # Esconde o rótulo "Número"
            self.label_name.config(text="")  # Remove o nome do candidato
            self.photo_dir = tk.PhotoImage(file='')  # Remove a foto do candidato
            self.photo.config(image=self.photo_dir)

            if self.current_role['vice']:
                self.label_vice_name.config(text="", fg="black")  # Remove o nome do vice
                self.vice_photo_dir = tk.PhotoImage(file='')  # Remove a foto do vice
                self.vice_photo.config(image=self.photo_dir)
                
        # Atualiza os dígitos exibidos nos quadrados
        for i in range(len(self.digit_labels)):
            if i < len(self.number):
                self.digit_labels[i].config(text=self.number[i])
            else:
                self.digit_labels[i].config(text="")
        
        # Atualiza o destaque do dígito atual
        self.highlight_current_digit()
        
        # Remove mensagens de confirmação anteriores, se existirem
        if hasattr(self, 'confirm_label'):
            self.confirm_label.destroy()
        if hasattr(self, 'separator'):
            self.separator.destroy()
        
        # Quando todos os dígitos forem preenchidos
        if len(self.number) == self.current_role['digits']:
            # Busca o candidato com base no cargo e número digitado
            candidate = self.candidate_manager.find(self.current_role['name'], self.number)
            
            if candidate:
                # Exibe o nome do candidato
                self.label_name.config(
                    text=f"Nome: {candidate['name']}",
                    fg="black"
                )
                # Carrega e exibe a foto do candidato
                self.photo_dir = tk.PhotoImage(file=f'./data/images/{candidate['cand_id']}.png')
                self.photo.config(image=self.photo_dir)

                if self.current_role['vice']:
                    # Exibe o nome do vice
                    self.label_vice_name.config(
                        text=f"Vice-{self.current_role['name']}: {candidate['vice']}",
                        fg="black"
                    )
                    # Carrega e exibe a foto do vice
                    self.vice_photo_dir = tk.PhotoImage(file=f'./data/images/{candidate['cand_id']}.vice.png')
                    self.vice_photo.config(image=self.vice_photo_dir)
            else:
                # Caso não encontre candidato, exibe "VOTO NULO"
                self.label_name.config(text="VOTO NULO!")
            
            # Torna o rótulo "Número" visível
            self.label_number_text.config(fg="black")
            
            # Exibe instruções de confirmação
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

            # Adiciona uma linha separadora antes das instruções
            self.separator = tk.Frame(self.root, height=2, bd=1, relief=tk.SUNKEN, bg='black')
            self.separator.pack(side='bottom', fill=tk.X, pady=10, padx=20)

    # Método para confirmar o voto
    def confirm_vote(self):
        if not self.voted:  # Verifica se o eleitor ainda não votou
            self.current_round += 1  # Avança para a próxima rodada
            # Registra o voto no gerenciador de candidatos
            self.candidate_manager.add_vote(self.current_role['name'], self.number)
            
            if self.current_round <= self.total_rounds:
                # Reproduz som de confirmação
                pygame.mixer.init()
                pygame.mixer.Sound("./data/sounds/confirmed_vote.wav").play()
                # Inicia a próxima rodada de votação
                self.start_vote_for_current_round()
            else:
                self.voted = True  # Marca como votado
                # Reproduz som de finalização
                pygame.mixer.init()
                pygame.mixer.Sound("./data/sounds/end.wav").play()
                
                # Limpa a tela
                for widget in self.root.winfo_children():
                    widget.destroy()
                
                # Exibe mensagem "FIM" centralizada
                tk.Label(
                    self.root,
                    text="FIM",
                    font=("Arial", 200)
                ).place(relx=0.5, rely=0.4, anchor=tk.CENTER)
            
                # Exibe "VOTOU" no canto inferior direito
                tk.Label(
                    self.root,
                    text="VOTOU",
                    font=("Arial", 36)
                ).place(relx=0.98, rely=0.98, anchor=tk.SE)
                
                # Fecha a janela após 5 segundos
                self.root.after(5000, self.root.destroy)
        else:
            pass  # Não faz nada se já votou