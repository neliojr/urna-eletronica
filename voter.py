# Importações necessárias
import json       # Para manipulação de arquivos JSON
import random     # Para geração de números aleatórios (IDs de eleitores)
from config import ConfigManager  # Para acessar configurações do sistema

# Inicializa o gerenciador de configurações
config = ConfigManager()

# Classe que representa um eleitor no sistema
class Voter:
    def __init__(self, voter_id, name, date_of_birth, section, voted):
        # Inicializa os atributos do eleitor:
        self.voter_id = voter_id        # ID único do eleitor
        self.name = name                # Nome completo do eleitor
        self.date_of_birth = date_of_birth  # Data de nascimento (formato não especificado)
        self.section = section          # Seção eleitoral à qual pertence
        self.voted = voted              # Status se já votou (True/False)

# Classe principal que gerencia todas as operações com eleitores
class VoterManager:
    def __init__(self):
        # Inicializa a lista de eleitores em memória
        self.voters = []
        # Define o caminho do arquivo de banco de dados JSON
        self.database = f'{config.get()['data_dir']}/voters.json'
        # Carrega os eleitores do arquivo para a memória
        self.load()

    # Método para carregar eleitores do arquivo JSON para a memória RAM
    def load(self):
        try:
            # Tenta abrir e ler o arquivo JSON
            with open(self.database, 'r') as file:
                data = json.load(file)

                # Para cada eleitor no arquivo JSON, cria um objeto Voter
                for item in data['voters']:
                    voter = Voter(
                        item['voter_id'],
                        item['name'],
                        item['date_of_birth'],
                        item['section'],
                        item['voted']
                    )
                    # Adiciona o eleitor à lista em memória
                    self.voters.append(voter)
        except: # Se o arquivo não existir (primeira execução), cria um novo
            # Estrutura básica do JSON com array vazio de eleitores
            data = {
                "voters": []
            }

            # Cria o arquivo JSON com a estrutura inicial
            with open(self.database, 'w') as file:
                json.dump(data, file, indent=4)
    
    # Método para salvar os eleitores da memória RAM para o arquivo JSON
    def save(self):
        # Prepara a estrutura de dados para serialização
        data = {'voters': []}

        # Converte cada objeto Voter em um dicionário para JSON
        for voter in self.voters:
            data['voters'].append({
                'voter_id': voter.voter_id,
                'name': voter.name,
                'date_of_birth': voter.date_of_birth,
                'section': voter.section,
                'voted': voter.voted
            })

        # Escreve os dados no arquivo JSON
        with open(self.database, 'w') as file:
            json.dump(data, file, indent=4)
    
    # Método para exibir todos os eleitores no formato de dicionário
    def display(self):
        # Retorna uma lista de dicionários com informações dos eleitores
        return [
            {
                'voter_id': voter.voter_id,
                'name': voter.name,
                'date_of_birth': voter.date_of_birth,
                'section': voter.section,
                'voted': voter.voted
            }
            for voter in self.voters  # List comprehension para iterar todos
        ]
    
    # Método para criar um novo eleitor no sistema
    def create(self, name, date_of_birth, section):
        # Cria novo objeto Voter com ID gerado automaticamente
        new_voter = Voter(
            self.generate_id(),  # Gera um ID único
            name,
            date_of_birth,
            section,
            False  # Inicializa como não tendo votado
        )
        # Adiciona o novo eleitor à lista em memória
        self.voters.append(new_voter)
        # Persiste as alterações no arquivo JSON
        self.save()
    
    # Método para remover um eleitor do sistema
    def remove(self, voter_id):
        try:
            # Filtra a lista de eleitores, removendo o especificado
            self.voters = [
                voter for voter in self.voters
                if not (voter.voter_id == int(voter_id))  # Converte para int e compara
            ]
            # Salva as alterações no arquivo JSON
            self.save()
        except:
            return 'Invalid voter ID'  # Se o ID não for numérico

    # Método para atualizar informações de um eleitor
    def update(self, voter_id, name, section):
        for voter in self.voters:
            if voter.voter_id == voter_id:
                # Atualiza nome se fornecido
                if name is not None:
                    voter.name = name
                # Atualiza seção se fornecida
                if section is not None:
                    voter.section = section
                # Persiste as alterações
                self.save()
                return
        return 'Voter not found'  # Se não encontrar o eleitor
    
    # Método para buscar um eleitor específico
    def find(self, voter_id):
        try:
            # Percorre a lista de eleitores
            for voter in self.voters:
                # Converte para int e compara
                if voter.voter_id == int(voter_id):
                    # Retorna os dados em formato de dicionário
                    return {
                        'voter_id': voter.voter_id,
                        'name': voter.name,
                        'date_of_birth': voter.date_of_birth,
                        'section': voter.section,
                        'voted': voter.voted
                    }
            return None  # Se não encontrar
        except:
            return None  # Se ocorrer erro na conversão para int
    
    # Método para gerar um ID único para novo eleitor
    def generate_id(self):
        while True:
            # Calcula o número máximo baseado na configuração
            voter_number_digit_length = 10 ** config.get()['voter_number_digit_length'] - 1
            # Gera um número aleatório no intervalo permitido
            voter_id = random.randint(1, voter_number_digit_length)
            # Verifica se o ID já existe
            check_exists = self.find(voter_id)
            if check_exists == None:
                break  # Sai do loop quando achar um ID único

        return voter_id
    
    # Método para marcar um eleitor como tendo votado
    def voter_voted(self, voter_id):
        for voter in self.voters:
            if voter.voter_id == int(voter_id):
                if voter.voted:
                    return 'eleitor já votou.'  # Mensagem se já tiver votado
                # Marca como votado e salva
                voter.voted = True
                self.save()
                return
        return 'Eleitor não encontrado'  # Se não encontrar o eleitor

    # Método para contar eleitores por seção
    def count_by_section(self, section):
        voters = 0  # Contador

        # Percorre todos os eleitores
        for voter in self.voters:
            if voter.section == section:
                voters += 1  # Incrementa se for da seção especificada

        return voters
    
    # Método para contar o total de eleitores
    def count(self):
        return len(self.voters)  # Retorna o tamanho da lista

    # Método para contar quantos eleitores já votaram
    def count_voted(self):
        voters = 0
        
        for voter in self.voters:
            if voter.voted == True:
                voters += 1  # Incrementa se já tiver votado

        return voters

    # Método para contar votantes por seção específica
    def count_voted_by_section(self, section):
        voters = 0
        
        for voter in self.voters:
            if voter.section == section:  # Verifica a seção
                if voter.voted == True:  # Verifica se votou
                    voters += 1

        return voters
    
    # Método para validar se um eleitor pode votar
    def validate(self, voter_id):
        try:
            for voter in self.voters:
                if voter.voter_id == int(voter_id):
                    if not voter.voted:
                        return True  # Pode votar (não votou ainda)
                    else:
                        return False  # Já votou
        except:
            return False  # ID inválido ou erro