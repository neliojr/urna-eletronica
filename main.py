from config import ConfigManager
import tkinter as tk

config = ConfigManager()

def select_ui(enable_gui):
    if enable_gui:
        from GUI.main import Application
        root = tk.Tk()
        app = Application(root)
        root.mainloop()
    else:
        from TUI.main import Application
        Application().menu()

try:
    select_ui(config.get()['enable_gui'])
except:
    config = ConfigManager()
    select_ui(config.get()['enable_gui'])
