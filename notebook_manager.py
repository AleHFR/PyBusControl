########### Preâmbulo ###########
# Imports do python
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from tktooltip import ToolTip

# Imports do projeto
import notebook_handler as nh
import project_handler as pj
import widget_manager as wm
import custom_widgets as cw
import modbus_handler as mh
import utils as ut

def novo_projeto(root, nome=None):
    # Instancia o projeto principal
    notebook = nh.Notebook(root)
    projeto = pj.Projeto()
    # Cria a barra de edição
    barra_ferramentas = ttk.LabelFrame(root, text=nome if nome else 'Novo Projeto')
    barra_ferramentas.pack(side='top', anchor='nw', fill='x', padx=2, pady=2)
    # Botões da aba
    itens = {
        'Nova Aba': {
            'command': lambda: notebook.add_aba(projeto),
            'icone': 'assets/nova_aba.png',
        },
        'Configurar Servidores': {
            'command': lambda:mh.criar_conexao(projeto),
            'icone': 'assets/servidor.png',
        },
        'Inserir Widget': {
            'command': lambda e:wm.adicionar_widget(e.x, e.y, projeto),
            'icone': 'assets/nova_aba.png',
        },
        'Configurar Aba': {
            'command': lambda:notebook.alterar_tamanho_canvas(projeto),
            'icone': 'assets/nova_aba.png',
        },
        'Tela Cheia':{
            'command': lambda:ut.tela_cheia(),
            'icone': 'assets/nova_aba.png',
        },
    }
    # Cria os botões
    tamanho_icone = (25, 25)
    for i in itens.keys():
        command = itens[i]['command']
        image = ImageTk.PhotoImage(Image.open(itens[i]['icone']).resize(tamanho_icone))
        bt = ttk.Button(barra_ferramentas, text='', command=command, image=image)
        bt.pack(side='left', padx=5, pady=2)
        ToolTip(bt, msg=i)