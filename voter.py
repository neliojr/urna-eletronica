import json
import random

from config import ConfigManager
config = ConfigManager()

class Voter:
    def __init__(self, voter_id, name, date_of_birth, section, voted):
        self.voter_id = voter_id
        self.name = name
        self.date_of_birth = date_of_birth
        self.section = section
        self.voted = voted


class VoterManager:
    def __init__(self):
        self.voters = []
        self.database = './data/voters.json'
        self.load()

    # carregar eleitores para a RAM.
    def load(self):
        try:
            with open(self.database, 'r') as file:
                data = json.load(file)

                for item in data['voters']:
                    voter = Voter(
                        item['voter_id'],
                        item['name'],
                        item['date_of_birth'],
                        item['section'],
                        item['voted']
                    )
                    self.voters.append(voter)
        except: # criando arquio JSON caso não exista.
            data = {
                "voters": []
            }

            with open(self.database, 'w') as file:
                json.dump(data, file, indent=4)
    
    # salvar eleitores na database.
    def save(self):
        data = {'voters': []}

        for voter in self.voters:
            data['voters'].append({
                'voter_id': voter.voter_id,
                'name': voter.name,
                'date_of_birth': voter.date_of_birth,
                'section': voter.section,
                'voted': voter.voted
            })

        with open(self.database, 'w') as file:
            json.dump(data, file, indent=4)
    
    # exibir eleitores.
    def display(self):
        return [
            {
                'voter_id': voter.voter_id,
                'name': voter.name,
                'date_of_birth': voter.date_of_birth,
                'section': voter.section,
                'voted': voter.voted
            }
            for voter in self.voters
        ]
    
    # criar eleitor.
    def create(self, name, date_of_birth, section):
        new_voter = Voter(
            self.generate_id(),
            name,
            date_of_birth,
            section,
            False
        )
        self.voters.append(new_voter)
        self.save()
    
    # remover eleitor.
    def remove(self, voter_id):
        try:
            self.voters = [
                voter for voter in self.voters
                if not (voter.voter_id == int(voter_id))
            ]
            self.save()
        except:
            return 'Invalid voter ID'

    # atualizar um eleitor.
    def update(self, voter_id, name, section):
        for voter in self.voters:
            if voter.voter_id == voter_id:
                if name is not None:
                    voter.name = name
                if section is not None:
                    voter.section = section
                self.save()
        return 'Voter not found'
    
    # buscar um eleitor.
    def find(self, voter_id):
        try:
            for voter in self.voters:
                if voter.voter_id == int(voter_id):
                    return {
                        'voter_id': voter.voter_id,
                        'name': voter.name,
                        'date_of_birth': voter.date_of_birth,
                        'section': voter.section,
                        'voted': voter.voted
                    }
            return None
        except:
            return None

    
    def generate_id(self):
        while True:
            voter_number_digit_length = 10 ** config.get()['voter_number_digit_length'] - 1
            voter_id = random.randint(
                1,
                voter_number_digit_length
            )
            check_exists = self.find(voter_id)
            if check_exists == None:
                break

        return voter_id
    
    def voter_voted(self, voter_id):
        for voter in self.voters:
            if voter.voter_id == int(voter_id):
                if voter.voted:
                    return 'eleitor já votou.'
                voter.voted = True
                self.save()
    
    def validate(self, voter_id):
        try:
            for voter in self.voters:
                if voter.voter_id == int(voter_id):
                    if not voter.voted:
                        return True
                    else:
                        return False
        except:
            return False