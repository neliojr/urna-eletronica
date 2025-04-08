# Importações necessárias para o funcionamento do sistema
import os          # Para operações com arquivos e diretórios
import json        # Para manipulação de arquivos JSON
import uuid        # Para geração de IDs únicos
from PIL import Image  # Para processamento de imagens (redimensionamento)
from config import ConfigManager  # Para acessar configurações do sistema

# Inicializa o gerenciador de configurações
config = ConfigManager()

# Classe que representa um candidato no sistema
class Candidate:
    def __init__(self, cand_id, name, number, role, vice, votes):
        # Inicializa os atributos do candidato:
        self.cand_id = cand_id    # ID único do candidato
        self.name = name           # Nome completo do candidato
        self.number = number       # Número de campanha
        self.role = role           # Cargo político que está concorrendo
        self.vice = vice           # Nome do vice-candidato (se aplicável)
        self.votes = votes         # Contagem de votos recebidos

# Classe principal que gerencia todas as operações com candidatos
class CandidateManager:
    def __init__(self):
        # Inicializa a lista de candidatos em memória
        self.candidates = []
        # Define o caminho do arquivo de banco de dados JSON
        self.database = f'{config.get()['data_dir']}/candidates.json'
        # Carrega os candidatos do arquivo para a memória
        self.load()

    # Método para carregar candidatos do arquivo JSON para a memória RAM
    def load(self):
        try:
            # Abre o arquivo JSON no modo leitura
            with open(self.database, 'r') as file:
                # Carrega os dados do arquivo JSON
                data = json.load(file)

                # Para cada candidato no arquivo JSON, cria um objeto Candidate
                for item in data['candidates']:
                    candidate = Candidate(
                        item['cand_id'],
                        item['name'],
                        item['number'],
                        item["role"],
                        item["vice"],
                        item["votes"]
                    )
                    # Adiciona o candidato à lista em memória
                    self.candidates.append(candidate)
        except: # Se o arquivo não existir (primeira execução), cria um novo
            # Estrutura básica do JSON com array vazio de candidatos
            data = {
                "candidates": []
            }

            # Cria o arquivo JSON com a estrutura inicial
            with open(self.database, 'w') as file:
                json.dump(data, file, indent=4)  # indent=4 para formatação bonita

    # Método para salvar os candidatos da memória RAM para o arquivo JSON
    def save(self):
        # Prepara a estrutura de dados para serialização
        data = {'candidates': []}

        # Converte cada objeto Candidate em um dicionário para JSON
        for candidate in self.candidates:
            data['candidates'].append({
                'cand_id': candidate.cand_id,
                'name': candidate.name,
                'number': candidate.number,
                'role': candidate.role,
                'vice': candidate.vice,
                'votes': candidate.votes
            })

        # Escreve os dados no arquivo JSON
        with open(self.database, 'w') as file:
            json.dump(data, file, indent=4)  # indent=4 para formatação legível
    
    # Método para exibir todos os candidatos no formato de dicionário
    def display(self):
        # Retorna uma lista de dicionários com informações dos candidatos
        return [
            {
                'cand_id': candidate.cand_id,
                'name': candidate.name,
                'number': candidate.number,
                'role': candidate.role,
                'vice': candidate.vice,
                'votes': candidate.votes
            }
            for candidate in self.candidates  # List comprehension para iterar todos
        ]
    
    # Método para criar um novo candidato no sistema
    def create(self, name, number, role, photo, vice, vice_photo):
        # Verifica se já existe candidato com mesmo número para o mesmo cargo
        for candidate in self.candidates:
            if candidate.role == role and candidate.number == number:
                return 'candidate already registered'  # Mensagem de erro
        
        # Gera um ID único para o novo candidato
        cand_id = str(uuid.uuid4())

        try:
            # Processamento da foto principal do candidato:
            # Abre a imagem usando PIL (Python Imaging Library)
            img = Image.open(photo)
            # Redimensiona a imagem para 225x300 pixels (pode distorcer a imagem)
            img_resized = img.resize((225, 300))

            # Salva a imagem redimensionada no diretório de imagens
            img_resized.save(f'{config.get()['data_dir']}/images/{cand_id}.png')

            # Processamento da foto do vice-candidato (se fornecida)
            if vice_photo != '':  # Verifica se foi fornecida foto do vice
                img = Image.open(vice_photo)
                # Redimensiona para 150x200 pixels
                img_resized = img.resize((150, 200))
                
                # Salva a imagem do vice com extensão especial (.vice.png)
                img_resized.save(f'{config.get()['data_dir']}/images/{cand_id}.vice.png')
        except:
            pass  # Se houver erro no processamento das imagens, ignora
        
        # Cria novo objeto Candidate com votos zerados
        new_candidate = Candidate(
            cand_id,
            name,
            number,
            role,
            vice,
            0  # Inicializa com 0 votos
        )
        # Adiciona o novo candidato à lista em memória
        self.candidates.append(new_candidate)
        # Persiste as alterações no arquivo JSON
        self.save()
    
    # Método para remover um candidato do sistema
    def remove(self, role, number):
        # Encontra o candidato a ser removido
        candidate = self.find(role, number)
        try:
            # Remove a foto principal do candidato
            os.remove(f'{config.get()['data_dir']}/images/{candidate['cand_id']}.png')
            # Remove a foto do vice (se existir)
            os.remove(f'{config.get()['data_dir']}/images/{candidate['cand_id']}.vice.png')
        except:
            pass  # Se não encontrar as imagens, continua normalmente

        # Filtra a lista de candidatos, removendo o especificado
        self.candidates = [
            candidate for candidate in self.candidates 
            if not (candidate.role == role and candidate.number == number)
        ]
        # Salva as alterações no arquivo JSON
        self.save()
    
    # Método para adicionar um voto a um candidato específico
    def add_vote(self, role, number):
        # Percorre a lista de candidatos
        for candidate in self.candidates:
            # Encontra o candidato pelo cargo e número
            if candidate.role == role and candidate.number == number:
                # Incrementa a contagem de votos
                candidate.votes += 1
                # Persiste a alteração
                self.save()
    
    # Método para buscar um candidato específico
    def find(self, role, number):
        # Percorre a lista de candidatos
        for candidate in self.candidates:
            # Verifica se corresponde ao cargo e número
            if candidate.role == role and candidate.number == number:
                # Retorna os dados em formato de dicionário
                return {
                    'cand_id': candidate.cand_id,
                    'name': candidate.name,
                    'number': candidate.number,
                    'role': candidate.role,
                    'vice': candidate.vice,
                    'votes': candidate.votes
                }
        # Retorna None se não encontrar
        return None