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
    root.state('zoomed') # inicia a janela em tela cheia
    style.theme_use('vista') # Escolhe o melhor tema para o Windows
elif platform.system() == 'Linux':
    root.attributes('-zoomed', True) # inicia a janela em tela cheia
    style.theme_use('default') # Escolhe o melhor tema para o Linux

########## Menu ##########
menu_bar = tk.Menu(root, tearoff=0)
root.config(menu=menu_bar)

# Criar um menu de arquivo
menu_arquivo = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Arquivo", menu=menu_arquivo)
menu_arquivo.add_command(label="Novo Projeto", command=lambda:nm.novo_projeto(root))
menu_arquivo.add_command(label="Carregar Projeto", command=lambda:fh.carregar_projeto(root))
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Preferências", command=lambda:ut.preferencias(style))
menu_arquivo.add_command(label="Sair", command=root.quit)

##########  ##########
# Espaçamento em cima
ttk.Label(root).pack(side='top', fill='both', expand=True)

frame_central = ttk.Frame(root, relief='raised', borderwidth=2)
frame_central.pack(expand=True, padx=20, pady=20)

# Configuração do grid
frame_central.columnconfigure(0, weight=1)
frame_central.columnconfigure(1, weight=2)
frame_central.rowconfigure(0, weight=1)

# Coluna da esquerda (botões)
frame_btn = ttk.Frame(frame_central)
frame_btn.grid(row=0, column=0, padx=20, pady=20, sticky='ns')

ttk.Button(frame_btn, text='Novo Projeto', command=lambda:nm.novo_projeto(root)).pack(pady=5, fill='x')
ttk.Button(frame_btn, text='Carregar Projeto', command=lambda:fh.carregar_projeto(root)).pack(pady=5, fill='x')

# Coluna da direita (arquivos recentes)
frame_arquivos = ttk.LabelFrame(frame_central, text='Arquivos recentes')
frame_arquivos.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')

lista = tk.Listbox(frame_arquivos, width=30, height=10, exportselection=False)
lista.pack(fill='both', expand=True)

# Espaçamento embaixo
ttk.Label(root).pack(side='bottom', fill='both', expand=True)

root.mainloop()