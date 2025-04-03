import json

class Role:
    def __init__(self, name, digits, vice):
        self.name = name
        self.digits = digits
        self.vice = vice

class RoleManager:
    def __init__(self):
        self.roles = []
        self.database = './data/roles.json'
        self.load()

    # carregar cargos para a RAM.
    def load(self):
        try:
            with open(self.database, 'r') as file:
                data = json.load(file)

                for item in data['roles']:
                    role = Role(item['name'], item['digits'], item["vice"])
                    self.roles.append(role)
        except: # criando arquio JSON caso não exista.
            data = {
                "roles": []
            }

            with open(self.database, 'w') as file:
                json.dump(data, file, indent=4)
    
    # salvar cargos na database.
    def save(self):
        data = {'roles': []}

        for role in self.roles:
            data['roles'].append({
                'name': role.name,
                'digits': role.digits,
                'vice': role.vice
            })

        with open(self.database, 'w') as file:
            json.dump(data, file, indent=4)
    
    # exibir cargos.
    def display(self):
        return [
            {
                'name': role.name,
                'digits': role.digits,
                'vice': role.vice
            }
            for role in self.roles
        ]
    
    # criar cargo.
    def create(self, name, digits, vice):
        if digits > 5 or digits < 2:
            return 'digitos insuficientes'
        
        for role in self.roles:
            if role.name == name:
                return 'role already registered'
            
        new_role = Role(name, digits, vice)
        self.roles.append(new_role)
        self.save()
    
    # remover cargo.
    def remove(self, name):
        self.roles = [
            role for role in self.roles 
            if not (role.name == name)
        ]
        self.save()
    
    # buscar um cargo.
    def find(self, name):
        for role in self.roles:
            if role.name == name:
                return {
                    'name': role.name,
                    'digits': role.digits,
                    'vice': role.vice
                }
        return None
    