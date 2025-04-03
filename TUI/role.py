from role import RoleManager
role_manager = RoleManager()

import os

class Role:
    def menu(self):
        while True:
            os.system('clear')
            print(f'''Urna Eletrônica - Cargos
Qual opção você deseja navegar?
[1] Cadastrar cargo
[2] Remover cargo
[3] Buscar cargo
[4] Listar cargos
[5] Voltar ao menu anterior''')
            
            self.option = int(input('> '))
            if self.option == 1:
                os.system('clear')
                Role().create()
            elif self.option == 2:
                os.system('clear')
                Role().remove()
            elif self.option == 3:
                os.system('clear')
                Role().find()
            elif self.option == 4:
                os.system('clear')
                Role().display()
            elif self.option == 5:
                os.system('clear')
                break

    def create(self):
        print('Cadastrar cargo')
        self.name = input('Nome: ')
        self.digits = int(input('Dígitos: '))
        self.vice = input('Tem vice? [S/n]: ')

        if self.vice == 'S' or self.vice == 's' or self.vice == '':
            self.vice = True
        else:
            self.vice = False

        role_manager.create(self.name, self.digits, self.vice)

    def remove(self):
        print('Remover cargo')
        self.name = input('Cargo: ')

        role_manager.remove(self.name)
    
    def find(self):
        print('Buscar cargo')
        self.name = input('Cargo: ')

        roles = role_manager.find(self.name)

        input(roles)

    def display(self):
        print('Lista de cargos')

        roles = role_manager.display()

        input(roles)