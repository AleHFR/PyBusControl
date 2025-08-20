########### Preâmbulo ###########
# Imports do python
import tkinter as tk
from tkinter import ttk
import platform
import os

# Imports do projeto
import tab_manager as tm
import file_handler as fh
import utils as ut
from project_handler import Projeto

########## Janela principal ##########
root = tk.Tk()
root.title('PyBusControl')
root.attributes('-zoomed', True)
root.bind()
# Icone
icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'pbc.png')
root.iconphoto(True, tk.PhotoImage(file=icon_path))
# Conjunto de Styles padrão
style = ttk.Style(root)
style.theme_use('default')
# Instancia o projeto principal
projeto = Projeto()

########## Verifica o sistema operacional ##########
if platform.system() == 'Windows':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

########## Menu ##########
menu_bar = tk.Menu(root, tearoff=0)
root.config(menu=menu_bar)

menu_arquivo = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Arquivo", menu=menu_arquivo)
menu_arquivo.add_command(label="Novo Projeto", command=lambda:tm.novo_projeto(root, projeto))
menu_arquivo.add_command(label="Carregar Projeto", command=lambda:fh.carregar_projeto(root))
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Preferências", command=lambda:ut.preferencias(style))
menu_arquivo.add_command(label="Sair", command=root.quit)

root.mainloop()