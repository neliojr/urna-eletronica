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
[6] Procurar atualizações
[7] Apagar todos os dados''')

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
            elif self.option == 7:
                os.system('clear')
                print('Você tem certeza que deseja apagar todos os dados?')
                print('[1] Sim')
                print('[2] Não')
                option = int(input('> '))
                if option == 1:
                    self.config.delete_all_data()
                    os.system('clear')
                    print('Todos os dados foram apagados!')
                    print('Inicie o programa novamente para aplicar as mudanças.')
                    input('Pressione Enter para continuar...')
                    exit()
                else:
                    os.system('clear')