import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from widget_manager import *
from tab_manager import *
import json
import config as cfg

# Variáveis Locais
caminho_imagem = None

########## Salvar o projeto atual em um arquivo Json ##########
def salvar_projeto(canvas):
    # Pergunta onde salvar
    caminho = filedialog.asksaveasfilename(
        defaultextension='.json',
        filetypes=[('Arquivos JSON', '*.json'), ('Todos os arquivos', '*.*')],
        title='Salvar arquivo',
    )
    if not caminho:
        return
    
    # Salva as informações do canvas
    configs_canvas = {}
    configs_canvas['config_canvas'] = {
        'tamanho_x': canvas.winfo_width(),
        'tamanho_y': canvas.winfo_height(),
        'imagem_fundo': caminho_imagem,
    }

    # Percorre os widgets do canvas
    for item_id in canvas.find_all():
        if canvas.type(item_id) == 'window':
            widget = canvas.nametowidget(canvas.itemcget(item_id, 'window'))
            x, y = canvas.coords(item_id)

            # Pega a classe e resolve o nome do tipo
            classe = widget.__class__.__name__
            tipo = [k for k, v in cfg.tipos_widgets.items() if v['classe'] == classe][0]
            # Pega propriedades
            props = {prop: widget.cget(prop) for prop in widget.config()}
            # Adiciona ao dicionario
            configs_canvas[f'{tipo}_{item_id}'] = {
                    'classe': classe,
                    'x': x,
                    'y': y,
                    'propriedades': props
                }
            

    # Salva tudo em JSON
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(configs_canvas, f, indent=4, ensure_ascii=False)

########## Carrega o projeto de um arquivo Json ##########
def carregar_projeto(notebook):
    global widgets_ids, imagem_id
    widgets_ids = []
    # Procura o arquivo
    caminho = filedialog.askopenfilename(
        defaultextension='.json',
        filetypes=[('Arquivos JSON', '*.json'), ('Todos os arquivos', '*.*')],
        title='Abrir arquivo'
    )
    if not caminho:
        return
    
    # Lê o arquivo com os widgets
    with open(caminho, 'r', encoding='utf-8') as arquivo:
        configs = json.load(arquivo)
        # Cria a área de desenho
        nome = caminho.split('/')[-1].replace('.json','')
        configs_canvas = configs['config_canvas']
        canvas = novo_projeto(notebook, nome=nome, x=configs_canvas['tamanho_x'], y=configs_canvas['tamanho_y'])
        canvas.image_ref = ImageTk.PhotoImage(Image.open(configs_canvas['imagem_fundo']))
        imagem_id = canvas.create_image(configs_canvas['tamanho_x']/2, configs_canvas['tamanho_y']/2, anchor='center', image=canvas.image_ref)
        # Adiciona os widgets
        for widget in configs:
            if widget == 'config_canvas':
                continue
            widget = configs[widget]
            classe = getattr(tk, widget['classe'])
            x = widget['x']
            y = widget['y']
            item_id = adicionar_widget(x, y, canvas, widget)
            widgets_ids.append([classe.__name__,item_id])