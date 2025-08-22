########### Preâmbulo ###########
# Imports do python
from tkinter import ttk
from tktooltip import ToolTip

# Imports do projeto
import notebook_handler as nh
import project_handler as pj
import widget_manager as wm
import modbus_handler as mh
import utils as ut

imagens = {}

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
            'icone': 'nova_aba.png',
        },
        'Configurar Servidores': {
            'command': lambda:mh.criar_conexao(projeto),
            'icone': 'servidor.png',
        },
        'Inserir Widget': {
            'command': lambda e:wm.adicionar_widget(projeto),
            'icone': 'novo_widget.png',
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