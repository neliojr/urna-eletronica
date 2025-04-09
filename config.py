import json  # Importa o módulo json para manipulação de arquivos JSON
import os  # Importa o módulo os para manipulação de arquivos e diretórios
import gdown

# Classe que representa uma configuração
class Config:
    def __init__(self, section, enable_gui, admin_pass, voter_number_digit_length):
        self.section = section  # Seção (provavelmente um identificador numérico)
        self.enable_gui = enable_gui  # Booleano para habilitar/desabilitar interface gráfica
        self.admin_pass = admin_pass  # Senha administrativa
        self.voter_number_digit_length = voter_number_digit_length  # Comprimento dos dígitos do número do eleitor

# Classe para gerenciar as configurações
class ConfigManager:
    def __init__(self):
        self.version = '1.0'  # Versão do gerenciador de configurações
        self.config = []  # Lista para armazenar objetos Config
        self.user_dir = os.path.expanduser('~') # Obtém o diretório do usuário
        self.data_dir = f'{self.user_dir}/.urnadata' # Diretório onde os dados serão armazenados
        self.database = f'{self.data_dir}/config.json' # Caminho do arquivo JSON de configurações
        self.load()  # Carrega as configurações ao inicializar

    # Método para carregar as configurações do arquivo JSON para a memória
    def load(self):
        try:
            # Cria o diretório './data' se não existir
            if not os.path.exists(f'{self.data_dir}'):
                os.mkdir(f'{self.data_dir}')
            
            # Cria o diretório './data/images' se não existir
            if not os.path.exists(f'{self.data_dir}/images'):
                os.mkdir(f'{self.data_dir}/images')
            
            # Cria o diretório './data/sounds' e baixa os sons se não existirem
            if not os.path.exists(f'{self.data_dir}/sounds'):
                os.mkdir(f'{self.data_dir}/sounds')
                gdown.download(
                    'https://drive.google.com/uc?id=1ojuJCuz354-1YBt04Isu3DXH7ivOZ3V9',
                    f'{self.data_dir}/sounds/end.wav',
                    quiet=False
                )

                gdown.download(
                    'https://drive.google.com/uc?id=1fzay61HupLIgbVZo9v51zsF9aewNhTyG',
                    f'{self.data_dir}/sounds/confirmed_vote.wav',
                    quiet=False
                )

            # Tenta abrir e ler o arquivo de configurações
            with open(self.database, 'r') as file:
                data = json.load(file)  # Carrega os dados do JSON

                # Itera sobre os itens na seção "config" do JSON
                for item in data['config']:
                    # Cria um objeto Config com os dados do item
                    config = Config(
                        item['section'],
                        item['enable_gui'],
                        item['admin_pass'],
                        item['voter_number_digit_length']
                    )
                    self.config.append(config)  # Adiciona o objeto à lista
        except:
            # Define configurações padrão
            data = {
                "config": [
                    {
                        "section": 1,  # Seção padrão
                        "enable_gui": True,  # Interface gráfica habilitada por padrão
                        "admin_pass": "1234",  # Senha padrão
                        "voter_number_digit_length": 6  # Comprimento padrão do número do eleitor
                    }
                ]
            }

            # Salva as configurações padrão no arquivo JSON
            with open(self.database, 'w') as file:
                json.dump(data, file, indent=4)  # indent=4 formata o JSON com indentação

    # Método para obter as configurações atuais
    def get(self):
        # Itera sobre a lista de configurações (assume apenas um item por simplicidade)
        for config in self.config:
            return {
                'data_dir': self.data_dir,
                'section': config.section,
                'enable_gui': config.enable_gui,
                'admin_pass': config.admin_pass,
                'voter_number_digit_length': config.voter_number_digit_length
            }
        return None  # Retorna None se a lista estiver vazia

    # Método para salvar as configurações no arquivo JSON
    def save(self):
        # Cria um dicionário com os dados da configuração
        data = {
            "config": [
                {
                    "section": self.config['section'],
                    "enable_gui": self.config['enable_gui'],
                    "admin_pass": self.config['admin_pass'],
                    "voter_number_digit_length": self.config['voter_number_digit_length']
                }
            ]
        }

        # Escreve os dados no arquivo JSON
        with open(self.database, 'w') as file:
            json.dump(data, file, indent=4)
    
    def change_admin_pass(self, new_password):
        self.config = self.get()
        self.config['admin_pass'] = new_password

        self.save()

        return
    
    def change_section(self, new_section):
        self.config = self.get()
        self.config['section'] = new_section

        self.save()

    # Método para alternar o estado da interface gráfica
    def change_ui(self):
        self.config = self.get()  # Obtém as configurações atuais como dicionário
        if self.config['enable_gui']:  # Se a GUI está habilitada
            self.config['enable_gui'] = False  # Desabilita
        else:
            self.config['enable_gui'] = True  # Habilita
        
        self.save()  # Salva as alterações no arquivo

    # Método para verificar atualizações (não implementado)
    def find_update(self):
        # Lógica de verificação de atualizações ainda não implementada
        return False  # Retorna False por padrão

    # Método para excluir todos os dados
    def delete_all_data(self):
        # Tenta remover cada arquivo de dados, ignorando erros se não existirem
        try:
            os.remove('./data/candidates.json')  # Remove arquivo de candidatos
        except:
            pass
        try:
            os.remove('./data/config.json')  # Remove arquivo de configurações
        except:
            pass
        try:
            os.remove('./data/roles.json')  # Remove arquivo de cargos
        except:
            pass
        try:
            os.remove('./data/voters.json')  # Remove arquivo de eleitores
        except:
            pass