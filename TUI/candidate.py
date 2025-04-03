from candidate import CandidateManager
candidate_manager = CandidateManager()

import os

class Candidate:
    def menu(self):
        while True:
            os.system('clear')
            print(f'''Urna Eletrônica - Candidatos
Qual opção você deseja navegar?
[1] Cadastrar candidato
[2] Remover candidato
[3] Buscar candidato
[4] Listar candidatos
[5] Voltar ao menu anterior''')
            
            self.option = int(input('> '))

            if self.option == 1:
                os.system('clear')
                Candidate().create()
            elif self.option == 2:
                os.system('clear')
                Candidate().remove()
            elif self.option == 3:
                os.system('clear')
                Candidate().find()
            elif self.option == 4:
                os.system('clear')
                Candidate().display()
            elif self.option == 5:
                os.system('clear')
                break

    def create(self):
        print('Cadastrar candidato')
        self.name = input('Nome: ')
        self.number = int(input('Número: '))
        self.role = input('Cargo: ')

        candidate_manager.create(self.name, self.number, self.role)

    def remove(self):
        print('Remover candidato')
        self.role = input('Cargo: ')
        self.number = int(input('Número: '))

        candidate_manager.remove(self.role, self.number)
    
    def find(self):
        print('Buscar candidato')
        self.role = input('Cargo: ')
        self.number = int(input('Número: '))

        candidates = candidate_manager.find(self.role, self.number)

        input(candidates)

    def display(self):
        print('Lista de candidatos')

        candidates = candidate_manager.display()

        input(candidates)