########### Preâmbulo ###########
from ctypes import windll
import tkinter as tk
from tkinter import ttk
import tab_manager as tm
import file_handler as fh
import utils as ut

windll.shcore.SetProcessDpiAwareness(1)

########## Janela principal ##########
root = tk.Tk()
root.title('PyBusControl')
root.minsize(1280, 720)
root.bind()

########## Conjunto de Styles padrão ##########
style = ttk.Style(root)
style.theme_use('vista')

########## Menu ##########
menu_bar = tk.Menu(root, tearoff=0)
root.config(menu=menu_bar)

menu_arquivo = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Arquivo", menu=menu_arquivo)
menu_arquivo.add_command(label="Novo Projeto", command=lambda:tm.novo_projeto(root))
menu_arquivo.add_command(label="Carregar Projeto", command=lambda:fh.carregar_projeto(root))
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Preferências", command=lambda:ut.preferencias(style))
menu_arquivo.add_command(label="Sair", command=root.quit)

# Menu Editar
menu_editar = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Editar", menu=menu_editar)
menu_editar.add_command(label="Nova Aba", command=lambda:tm.nova_aba(root))
menu_editar.add_command(label='Tela cheia',command=lambda:ut.tela_cheia())
menu_editar.add_command(label='Salvar',command=lambda:fh.salvar_projeto(root))

# Menu Ajuda
menu_ajuda = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Ajuda", menu=menu_ajuda)
menu_ajuda.add_command(label="Sobre")
menu_ajuda.add_command(label="Documentação")

root.mainloop()