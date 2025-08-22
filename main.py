########### Preâmbulo ###########
# Imports do python
import tkinter as tk
from tkinter import ttk
import platform

# Imports do projeto
import notebook_manager as nm
import file_handler as fh
import utils as ut

########## Janela principal ##########
root = tk.Tk()
root.title('PyBusControl')
root.bind()
# Icone
root.iconphoto(True, ut.imagem('pbc.png'))
# Conjunto de Styles padrão
style = ttk.Style(root)

########## Configura conforme o sistema operacional ##########
if platform.system() == 'Windows':
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
    root.state('zoomed')
    style.theme_use('vista')
elif platform.system() == 'Linux':
    root.attributes('-zoomed', True)
    style.theme_use('default')

########## Menu ##########
menu_bar = tk.Menu(root, tearoff=0)
root.config(menu=menu_bar)

menu_arquivo = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Arquivo", menu=menu_arquivo)
menu_arquivo.add_command(label="Novo Projeto", command=lambda:nm.novo_projeto(root))
menu_arquivo.add_command(label="Carregar Projeto", command=lambda:fh.carregar_projeto(root))
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Preferências", command=lambda:ut.preferencias(style))
menu_arquivo.add_command(label="Sair", command=root.quit)

root.mainloop()