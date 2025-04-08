# Importação necessária para manipulação de arquivos JSON
import json
from config import ConfigManager  # Para acessar configurações do sistema

# Inicializa o gerenciador de configurações
config = ConfigManager()

# Classe que representa um cargo político no sistema
class Role:
    def __init__(self, name, digits, vice):
        # Inicializa os atributos do cargo:
        self.name = name    # Nome do cargo (ex: "Prefeito", "Vereador")
        self.digits = digits # Quantidade de dígitos no número do candidato
        self.vice = vice    # Booleano indicando se o cargo tem vice

# Classe principal que gerencia todas as operações com cargos políticos
class RoleManager:
    def __init__(self):
        # Inicializa a lista de cargos em memória
        self.roles = []
        # Define o caminho do arquivo de banco de dados JSON
        self.database = f'{config.get()['data_dir']}/roles.json'
        # Carrega os cargos do arquivo para a memória
        self.load()

    # Método para carregar cargos do arquivo JSON para a memória RAM
    def load(self):
        try:
            # Abre o arquivo JSON no modo leitura
            with open(self.database, 'r') as file:
                # Carrega os dados do arquivo JSON
                data = json.load(file)

                # Para cada cargo no arquivo JSON, cria um objeto Role
                for item in data['roles']:
                    role = Role(
                        item['name'],    # Nome do cargo
                        item['digits'], # Dígitos do número eleitoral
                        item["vice"]     # Se tem vice
                    )
                    # Adiciona o cargo à lista em memória
                    self.roles.append(role)
        except: # Se o arquivo não existir (primeira execução), cria um novo
            # Estrutura básica do JSON com array vazio de cargos
            data = {
                "roles": []
            }

            # Cria o arquivo JSON com a estrutura inicial
            with open(self.database, 'w') as file:
                json.dump(data, file, indent=4)  # indent=4 para formatação bonita
    
    # Método para salvar os cargos da memória RAM para o arquivo JSON
    def save(self):
        # Prepara a estrutura de dados para serialização
        data = {'roles': []}

        # Converte cada objeto Role em um dicionário para JSON
        for role in self.roles:
            data['roles'].append({
                'name': role.name,     # Nome do cargo
                'digits': role.digits,  # Dígitos do número eleitoral
                'vice': role.vice       # Se tem vice
            })

        # Escreve os dados no arquivo JSON
        with open(self.database, 'w') as file:
            json.dump(data, file, indent=4)  # indent=4 para formatação legível
    
    # Método para exibir todos os cargos no formato de dicionário
    def display(self):
        # Retorna uma lista de dicionários com informações dos cargos
        return [
            {
                'name': role.name,     # Nome do cargo
                'digits': role.digits, # Dígitos do número eleitoral
                'vice': role.vice      # Se tem vice
            }
            for role in self.roles  # List comprehension para iterar todos
        ]
    
    # Método para contar quantos cargos existem no sistema
    def count(self):
        return len(self.roles)  # Retorna o tamanho da lista de cargos
    
    # Método para criar um novo cargo no sistema
    def create(self, name, digits, vice):
        try:
            # Validação: número de dígitos deve estar entre 2 e 5
            if int(digits) > 5 or int(digits) < 2:
                return 'digitos insuficientes'  # Mensagem de erro
            
            # Verifica se já existe cargo com mesmo nome
            for role in self.roles:
                if role.name == name:
                    return 'role already registered'  # Mensagem de erro
                
            # Cria novo objeto Role com os parâmetros fornecidos
            new_role = Role(
                name,           # Nome do cargo
                int(digits),    # Dígitos (convertido para inteiro)
                vice           # Se tem vice
            )
            # Adiciona o novo cargo à lista em memória
            self.roles.append(new_role)
            # Persiste as alterações no arquivo JSON
            self.save()
        except ValueError:  # Captura erro se digits não for conversível para int
            return 'Invalid digits.'  # Mensagem de erro
    
    # Método para remover um cargo do sistema
    def remove(self, name):
        # Filtra a lista de cargos, removendo o especificado
        self.roles = [
            role for role in self.roles 
            if not (role.name == name)  # Mantém todos exceto o com nome especificado
        ]
        # Salva as alterações no arquivo JSON
        self.save()
    
    # Método para buscar um cargo específico
    def find(self, name):
        # Percorre a lista de cargos
        for role in self.roles:
            # Verifica se corresponde ao nome pesquisado
            if role.name == name:
                # Retorna os dados em formato de dicionário
                return {
                    'name': role.name,     # Nome do cargo
                    'digits': role.digits, # Dígitos do número eleitoral
                    'vice': role.vice      # Se tem vice
                }
        # Retorna None se não encontrar
        return None