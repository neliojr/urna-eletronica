from voter import VoterManager
voter_manager = VoterManager()

import os

class Voter:
    def menu(self):
        while True:
            os.system('clear')
            print(f'''Urna Eletrônica - Eleitores
Qual opção você deseja navegar?
[1] Cadastrar eleitor
[2] Remover eleitor
[3] Buscar eleitor
[4] Editar eleitor
[5] Listar eleitores
[6] Voltar ao menu anterior''')
            
            self.option = int(input('> '))

            if self.option == 1:
                os.system('clear')
                Voter().create()
            elif self.option == 2:
                os.system('clear')
                Voter().remove()
            elif self.option == 3:
                os.system('clear')
                Voter().find()
            elif self.option == 4:
                os.system('clear')
                Voter().update()
            elif self.option == 5:
                os.system('clear')
                Voter().display()
            elif self.option == 6:
                os.system('clear')
                break

    def create(self):
        print('Cadastrar eleitor')
        self.name = input('Nome: ')
        self.date_of_birth = input('Data de nascimento (DD/MM/YYYY): ')
        self.section = int(input('Seção: '))

        voter_manager.create(self.name, self.date_of_birth, self.section)

    def remove(self):
        print('Remover eleitor')
        self.voter_id = int(input('Número do eleitor: '))

        voter_manager.remove(self.voter_id)
    
    def find(self):
        print('Buscar eleitor')
        self.voter_id = int(input('Número do eleitor: '))

        voter = voter_manager.find(self.voter_id)

        input(voter)
    
    def update(self):
        print('Buscar cargo')
        self.name = input('Cargo: ')

        roles = voter_manager.find(self.name)

        input(roles)

    def display(self):
        print('Lista de eleitores')

        voters = voter_manager.display()

        input(voters)