import os
import json
import uuid
from PIL import Image

class Candidate:
    def __init__(self, cand_id, name, number, role, vice, votes):
        self.cand_id = cand_id
        self.name = name
        self.number = number
        self.role = role
        self.vice = vice
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
                    candidate = Candidate(
                        item['cand_id'],
                        item['name'],
                        item['number'],
                        item["role"],
                        item["vice"],
                        item["votes"]
                    )
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
                'cand_id': candidate.cand_id,
                'name': candidate.name,
                'number': candidate.number,
                'role': candidate.role,
                'vice': candidate.vice,
                'votes': candidate.votes
            })

        with open(self.database, 'w') as file:
            json.dump(data, file, indent=4)
    
    # exibir candidatos.
    def display(self):
        return [
            {
                'cand_id': candidate.cand_id,
                'name': candidate.name,
                'number': candidate.number,
                'role': candidate.role,
                'vice': candidate.vice,
                'votes': candidate.votes
            }
            for candidate in self.candidates
        ]
    
    # criar candidato.
    def create(self, name, number, role, photo, vice, vice_photo):
        for candidate in self.candidates:
            if candidate.role == role and candidate.number == number:
                return 'candidate already registered'
        
        cand_id = str(uuid.uuid4())

        try:
            # foto do cabeça da chapa.
            img = Image.open(photo)
            # redimensionar para 300x400 pixels (pode distorcer).
            img_resized = img.resize((225, 300))

            # salvar a imagem redimensionada.
            img_resized.save(f'./data/images/{cand_id}.png')

            # foto do vice.
            if vice_photo != '':
                img = Image.open(vice_photo)
                # redimensionar para 300x400 pixels (pode distorcer).
                img_resized = img.resize((150, 200))
                
                # salvar a imagem redimensionada.
                img_resized.save(f'./data/images/{cand_id}.vice.png')
        except:
            pass
        
        new_candidate = Candidate(
            cand_id,
            name,
            number,
            role,
            vice,
            0
        )
        self.candidates.append(new_candidate)
        self.save()
    
    # remover candidato.
    def remove(self, role, number):
        candidate = self.find(role, number)
        try:
            os.remove(f'./data/images/{candidate['cand_id']}.png')
            os.remove(f'./data/images/{candidate['cand_id']}.vice.png')
        except:
            pass

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
                    'cand_id': candidate.cand_id,
                    'name': candidate.name,
                    'number': candidate.number,
                    'role': candidate.role,
                    'vice': candidate.vice,
                    'votes': candidate.votes
                }
        return None
    
