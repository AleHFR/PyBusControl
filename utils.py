import os
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import custom_widgets as cw
from PIL import Image, ImageTk

widgets_padrao = {
    'Texto': {
        'classe': 'CTkLabel',
        'propriedades': {
            'text': 'Texto',
            'font': None,
            'text_color': None,
            'fg_color': 'transparent',
            'corner_radius': 0,
            'width': 0, # Auto-ajustável
            'height': 0, # Auto-ajustável
            'image': None,
            'compound': 'left',
            'anchor': 'center'
        }
    },
    'Botão': {
        'classe': 'CTkButton',
        'funcao': None, # Usado para armazenar a função do comando
        'propriedades': {
            'text': 'Botão',
            'font': None,
            'state': 'normal',
            'width': 140,
            'height': 28,
            'corner_radius': None,
            'border_width': None,
            'border_spacing': 2,
            'fg_color': None,
            'hover_color': None,
            'border_color': None,
            'text_color': None,
            'text_color_disabled': None,
            'image': None,
            'compound': 'left',
            'anchor': 'center'
        }
    },
    'Indicador': {
        'classe': 'CTkLabel',
        'propriedades': {
            'text': '0.00',
            'font': ('Arial', 14, 'bold'),
            'text_color': None,
            'fg_color': 'transparent',
            'corner_radius': 0,
            'width': 0,
            'height': 0,
            'anchor': 'center'
        }
    },
    'Slider': {
        'classe': 'CTkSlider',
        'funcao': None,
        'propriedades': {
            'from_': 0,
            'to': 100,
            'number_of_steps': None,
            'orientation': 'horizontal',
            'width': 200,
            'height': 16,
            'fg_color': None,
            'progress_color': None,
            'button_color': None,
            'button_hover_color': None
        }
    },
    'Caixa de Seleção': {
        'classe': 'CTkCheckBox',
        'funcao': None,
        'propriedades': {
            'text': 'Opção',
            'variable': None,
            'onvalue': 1,
            'offvalue': 0,
            'font': None,
            'width': 0,
            'height': 0,
            'corner_radius': None,
            'border_width': None,
            'fg_color': None,
            'hover_color': None,
            'border_color': None,
            'text_color': None
        }
    },
    'Interruptor': {
        'classe': 'CTkSwitch',
        'funcao': None, # Usado para armazenar a função do comando
        'propriedades': {
            'text': 'Opção',
            'variable': None,
            'onvalue': 1,
            'offvalue': 0,
            'command': None,
            'state': 'normal',
            'font': None,
            'width': 50, # Largura padrão
            'height': 24, # Altura padrão
            'corner_radius': None,
            'border_width': None,
            'fg_color': None, # Cor da "pista" (fundo)
            'progress_color': None, # Cor da "pista" quando está ligado
            'button_color': None,
            'button_hover_color': None,
            'border_color': None,
            'text_color': None
        }
    },
}

def dica(texto:str=None):
    # Encontra a barra de ferrementas do projeto principal
    barra_ferramentas = None
    for widget in tk._default_root.winfo_children():
        if widget.winfo_class() == 'TLabelframe':
            barra_ferramentas = widget
    # Verifica se o label já existe
    for widget in barra_ferramentas.winfo_children():
        if widget.winfo_class() == 'TLabel':
            widget.config(text=texto if texto else 'Nenhuma Atividade')

def imagem(nome, tamanho_icone=None):
    caminho_icone = os.path.join(os.path.dirname(__file__), 'assets', nome)
    image = Image.open(caminho_icone)
    # Muda a cor da imagem
    if tamanho_icone:
        image = image.resize((tamanho_icone))
    image = ImageTk.PhotoImage(image)
    return image

def preferencias(): # Passe a janela principal como argumento
    # 1. Cria a janela Toplevel (janela secundária)
    janela = cw.janelaScroll('Preferências', geometry=(300, 200), resizable=(False, False), buttonName='Aplicar', closeWindow=False, command=lambda:aplicar())

    # --- Frame para o Modo de Aparência (Light/Dark) ---
    frame_modo = ctk.CTkFrame(janela)
    frame_modo.pack(pady=10, padx=15, fill="x")

    ctk.CTkLabel(frame_modo, text='Modo de Aparência:').pack(padx=10, pady=5, side='left')
    
    modos = ['Light', 'Dark', 'System']
    modo_sel = ctk.CTkComboBox(frame_modo, values=modos, state='readonly', width=120)
    modo_sel.pack(padx=10, pady=5, side='right')
    modo_sel.set(ctk.get_appearance_mode()) # Pega o modo atual e define no ComboBox

    # --- Frame para o Tema de Cores ---
    frame_tema = ctk.CTkFrame(janela)
    frame_tema.pack(pady=10, padx=15, fill="x")

    ctk.CTkLabel(frame_tema, text='Tema de Cores:').pack(padx=10, pady=5, side='left')
    
    # Nota: Temas de cores personalizados podem ser carregados de arquivos JSON
    temas = ['blue', 'green', 'dark-blue']
    tema_sel = ctk.CTkComboBox(frame_tema, values=temas, state='readonly', width=120)
    tema_sel.pack(padx=10, pady=5, side='right')
    # Não há uma função para "get" do tema de cores, então podemos setar um padrão
    tema_sel.set('blue')

    # --- Botão Aplicar ---
    def aplicar():
        # Pega os valores selecionados e aplica
        novo_modo = modo_sel.get().lower()
        novo_tema = tema_sel.get()
        
        ctk.set_appearance_mode(novo_modo)
        ctk.set_default_color_theme(novo_tema)

def tela_cheia():
    root = tk._default_root
    if root is not None:
        is_fullscreen = root.attributes('-fullscreen')
        root.attributes('-fullscreen', not is_fullscreen)
        
        # Adiciona ou remove o binding do ESC quando entra/sai do modo tela cheia
        if not is_fullscreen:
            root.bind('<Escape>', lambda e: tela_cheia())
        else:
            root.unbind('<Escape>')