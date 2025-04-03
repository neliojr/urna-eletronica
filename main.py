from config import ConfigManager

config = ConfigManager()

from TUI.main import TUI

def select_ui(enable_gui):
    if enable_gui:
        pass
    else:
        TUI().menu()

try:
    select_ui(config.get()['enable_gui'])
except:
    config = ConfigManager()
    select_ui(config.get()['enable_gui'])
