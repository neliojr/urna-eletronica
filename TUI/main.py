import os
from TUI.candidate import Candidate
from TUI.role import Role
from TUI.voter import Voter
from config import ConfigManager

class Application:
    def menu(self):
        self.config = ConfigManager()
        while True:
            os.system('clear')
            print(f'''Urna Eletrônica
Qual opção você deseja navegar?
[1] Cargos
[2] Candidatos
[3] Eleitores
[4] Iniciar votação
[5] Mudar para GUI
[6] Procurar atualizações''')

            self.option = int(input('> '))

            if self.option == 1:
                Role().menu()
            elif self.option == 2:
                Candidate().menu()
            elif self.option == 3:
                Voter().menu()
            elif self.option == 5:
                self.config.change_ui()
                exit()
            elif self.option == 6:
                self.config.find_update()
                if self.config.find_update():
                    os.system('clear')
                    print('Atualização encontrada!')
                    print('Seu programa será atualizado.')
                    input('Pressione Enter para continuar...')
                else:
                    os.system('clear')
                    print('Seu programa já está atualizado!')
                    input('Pressione Enter para continuar...')
                    os.system('clear')