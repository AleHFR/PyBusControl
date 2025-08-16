########### Preâmbulo ###########
from ctypes import windll
import tkinter as tk
from tkinter import ttk
import tab_manager as tm
import file_handler as fh
import widget_manager as wm
import utils as ut
import config as cfg

windll.shcore.SetProcessDpiAwareness(1)

########## Janela principal ##########
root = tk.Tk()
root.title('PyBusControl')
root.minsize(1280, 720)
root.bind()

########## Conjunto de Styles padrão ##########
style = ttk.Style(root)
style.theme_use('vista')

style.configure('TLabel', background=cfg.bg, foreground='Black')
style.configure('TButton', background=cfg.bg, foreground='Black')
style.configure('TFrame', background=cfg.bg, foreground='Black')

########## Menu ##########
menu_bar = tk.Menu(root, tearoff=0)
root.config(menu=menu_bar)

menu_arquivo = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Arquivo", menu=menu_arquivo)
menu_arquivo.add_command(label="Novo Projeto", command=lambda:tm.novo_projeto(notebook))
menu_arquivo.add_command(label="Carregar Projeto", command=lambda:fh.carregar_projeto(notebook))
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Sair", command=root.quit)

# Menu Editar
menu_editar = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Editar", menu=menu_editar)
menu_editar.add_command(label="Preferências", command=lambda:ut.preferencias(style))

# Menu Ajuda
menu_ajuda = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Ajuda", menu=menu_ajuda)
menu_ajuda.add_command(label="Sobre")
menu_ajuda.add_command(label="Documentação")

########## Cria o notebook ##########
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)
notebook.bind("<Button-2>", lambda e: tm.excluir_aba_projeto(e, notebook))

root.mainloop()