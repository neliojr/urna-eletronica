import json

class Candidate:
    def __init__(self, name, number, role, votes):
        self.name = name
        self.number = number
        self.role = role
        self.votes = votes

class CandidateManager:
    def __init__(self):
        self.candidates = []
        self.database = './data/candidates.json'
        self.load()

    # carregar candidatos para a RAM.
    def load(self):
        try:
            with open(self.database, 'r') as file:
                data = json.load(file)

                for item in data['candidates']:
                    candidate = Candidate(item['name'], item['number'], item["role"], item["votes"])
                    self.candidates.append(candidate)
        except: # criando arquio JSON caso não exista.
            data = {
                "candidates": []
            }

            with open(self.database, 'w') as file:
                json.dump(data, file, indent=4)

    # salvar candidatos na database.
    def save(self):
        data = {'candidates': []}

        for candidate in self.candidates:
            data['candidates'].append({
                'name': candidate.name,
                'number': candidate.number,
                'role': candidate.role,
                'votes': candidate.votes
            })

        with open(self.database, 'w') as file:
            json.dump(data, file, indent=4)
    
    # exibir candidatos.
    def display(self):
        return [
            {
                'name': candidate.name,
                'number': candidate.number,
                'role': candidate.role,
                'votes': candidate.votes
            }
            for candidate in self.candidates
        ]
    
    # criar candidato.
    def create(self, name, number, role):
        for candidate in self.candidates:
            if candidate.role == role and candidate.number == number:
                return 'candidate already registered'
            
        new_candidate = Candidate(name, number, role, 0)
        self.candidates.append(new_candidate)
        self.save()
    
    # remover candidato.
    def remove(self, role, number):
        self.candidates = [
            candidate for candidate in self.candidates 
            if not (candidate.role == role and candidate.number == number)
        ]
        self.save()
    
    # adicionar voto para um candidato.
    def add_vote(self, role, number):
        for candidate in self.candidates:
            if candidate.role == role and candidate.number == number:
                candidate.votes += 1
                self.save()
    
    # buscar um candidato.
    def find(self, role, number):
        for candidate in self.candidates:
            if candidate.role == role and candidate.number == number:
                return {
                    'name': candidate.name,
                    'number': candidate.number,
                    'role': candidate.role,
                    'votes': candidate.votes
                }
        return None
    
