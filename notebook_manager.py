########### Preâmbulo ###########
# Imports do python
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

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
    ttk.Button(barra_ferramentas, text='Nova Aba', command=lambda:notebook.add_aba(projeto)).pack(side='left', padx=5, pady=2)
    ttk.Button(barra_ferramentas, text='Configurar Servidores', command=lambda:mh.criar_conexao(projeto)).pack(side='left', padx=5, pady=2)
    ttk.Button(barra_ferramentas, text='Inserir Widget',command=lambda e:wm.adicionar_widget(e.x, e.y, projeto)).pack(side='left', padx=5, pady=2)
    ttk.Button(barra_ferramentas, text='Configurar Aba',command=lambda:notebook.alterar_tamanho_canvas(projeto)).pack(side='left', padx=5, pady=2)
    ttk.Button(barra_ferramentas, text='Tela Cheia', command=lambda:ut.tela_cheia()).pack(side='left', padx=5, pady=2)