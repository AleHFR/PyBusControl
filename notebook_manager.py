########### Preâmbulo ###########
# Imports do python
import tkinter as tk
from tkinter import ttk
from tktooltip import ToolTip

# Imports do projeto
import project_handler as pj
import widget_manager as wm
import server_manager as sm
import utils as ut

imagens = {}

def novo_projeto(root, nome=None):
    # Limpa o root
    for widget in root.winfo_children():
        # Destroi apenas os widgets não necessários
        if widget.winfo_class() not in ['LabelFrame', 'Menu']:
            widget.destroy()
    # Instancia o projeto principal
    projeto = pj.Projeto(root)
    # Cria a barra de edição
    barra_ferramentas = ttk.LabelFrame(root, text=nome if nome else 'Novo Projeto')
    barra_ferramentas.pack(side='top', anchor='nw', fill='x', padx=2, pady=2)
    # Botões da aba
    itens = {
        'Nova Aba': {
            'command': lambda:projeto.add_aba(),
            'icone': 'nova_aba.png',
        },
        'Configurar Servidores': {
            'command': lambda:sm.configurar_servidores(projeto),
            'icone': 'servidor.png',
        },
        'Conectar Servidores':{
            'command': lambda:sm.conectar_servidores(projeto),
            'icone': 'conectar.png',
        },
        'Adicionar Widget': {
            'command': lambda:wm.adicionar_widget(projeto),
            'icone': 'widget.png',
        },
        'Tela Cheia':{
            'command': lambda:ut.tela_cheia(),
            'icone': 'tela_cheia.png',
        },
    }
    # Cria os botões
    for nome_botao, cfg in itens.items():
        imagens[nome_botao] = ut.imagem(cfg['icone'], (15, 15))
        bt = ttk.Button(
            barra_ferramentas,
            command=cfg['command'],
            image=imagens[nome_botao]
        )
        bt.pack(side='left', padx=1, pady=2)
        ToolTip(bt, msg=nome_botao)

    # Cria um texto de suporte
    ttk.Label(barra_ferramentas, text='Nenhuma Atividade').pack(side='right', padx=5)