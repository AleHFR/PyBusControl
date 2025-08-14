########### Preâmbulo ###########
from ctypes import windll
import tkinter as tk
from tkinter import ttk
from funcoes import *
import config as cfg

windll.shcore.SetProcessDpiAwareness(1)

########## Janela principal ##########
root = tk.Tk()
root.title('PyBusControl')
root.minsize(1280, 720)
root.bind()

########## Menu ##########
menu_bar = tk.Menu(root, tearoff=0)
root.config(menu=menu_bar)

menu_arquivo = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Arquivo", menu=menu_arquivo)
menu_arquivo.add_command(label="Novo Projeto", command=lambda:novo_projeto(notebook))
menu_arquivo.add_command(label="Carregar Projeto", command=lambda:carregar_projeto(notebook))
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Sair", command=root.quit)

# Menu Editar
menu_editar = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Editar", menu=menu_editar)
menu_editar.add_command(label="Preferências")

# Menu Ajuda
menu_ajuda = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Ajuda", menu=menu_ajuda)
menu_ajuda.add_command(label="Sobre")
menu_ajuda.add_command(label="Documentação")


########## Cria o notebook ##########
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)
notebook.bind("<Button-2>", lambda e: excluir_aba_projeto(e, notebook))

root.mainloop()
