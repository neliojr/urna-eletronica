import os
from TUI.candidate import Candidate
from TUI.role import Role
from TUI.voter import Voter

class TUI:
    def menu(self):
        while True:
            os.system('clear')
            print(f'''Urna Eletrônica
Qual opção você deseja navegar?
[1] Cargos
[2] Candidatos
[3] Eleitores
[4] Iniciar votação''')

            self.option = int(input('> '))

            if self.option == 1:
                Role().menu()
            elif self.option == 2:
                Candidate().menu()
            elif self.option == 3:
                Voter().menu()