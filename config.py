import json
import os

class Config:
    def __init__(self, section, enable_gui, admin_pass, voter_number_digit_length):
        self.section = section
        self.enable_gui = enable_gui
        self.admin_pass = admin_pass
        self.voter_number_digit_length = voter_number_digit_length

class ConfigManager:
    def __init__(self):
        self.config = []
        self.database = './data/config.json'
        self.load()

    # carregar as configurações para a RAM.
    def load(self):
        try:
            with open(self.database, 'r') as file:
                data = json.load(file)

                for item in data['config']:
                    config = Config(item['section'], item['enable_gui'], item['admin_pass'], item['voter_number_digit_length'])
                    self.config.append(config)
        except: # criando arquivo JSON caso não exista.
            if not os.path.exists(self.database):
                os.mkdir('./data')
            data = {
                "config": [
                    {
                        "section": 1,
                        "enable_gui": True,
                        "admin_pass": "1234",
                        "voter_number_digit_length": 6
                    }
                ]
            }

            with open(self.database, 'w') as file:
                json.dump(data, file, indent=4)

    
    def get(self):
        for config in self.config:
            return {
                'section': config.section,
                'enable_gui': config.enable_gui,
                'admin_pass': config.admin_pass,
                'voter_number_digit_length': config.voter_number_digit_length
            }
        return None