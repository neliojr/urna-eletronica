from config import ConfigManager  # Importa a classe ConfigManager do módulo config
import tkinter as tk  # Importa o Tkinter para criar interfaces gráficas

# Instancia o gerenciador de configurações
config = ConfigManager()

# Função para selecionar a interface do usuário (GUI ou TUI) com base na configuração
def select_ui(enable_gui):
    if enable_gui:  # Se a interface gráfica (GUI) estiver habilitada
        from GUI.main import Application  # Importa a classe Application do módulo GUI.main
        root = tk.Tk()  # Cria a janela principal do Tkinter
        app = Application(root)  # Instancia a aplicação GUI passando a janela
        root.mainloop()  # Inicia o loop principal da interface gráfica
    else:  # Se a interface gráfica estiver desabilitada (usa TUI - Interface de Texto)
        from TUI.main import Application  # Importa a classe Application do módulo TUI.main
        Application().menu()  # Instancia a aplicação TUI e chama o método menu()

# Bloco principal para executar a interface selecionada
try:
    # Tenta obter a configuração 'enable_gui' e seleciona a interface correspondente
    select_ui(config.get()['enable_gui'])
except:
    # Em caso de erro (ex.: arquivo de configuração corrompido ou inexistente)
    config = ConfigManager()  # Reinicia o ConfigManager (cria configurações padrão, se necessário)
    select_ui(config.get()['enable_gui'])  # Tenta novamente selecionar a interface