import os
import tkinter as tk
from tkinter import ttk
import custom_widgets as cw
from PIL import Image, ImageTk

def imagem(nome, tamanho_icone=None):
    caminho_icone = os.path.join(os.path.dirname(__file__), 'assets', nome)
    image = Image.open(caminho_icone)
    if tamanho_icone:
        image = image.resize((tamanho_icone))
    image = ImageTk.PhotoImage(image)
    return image

def preferencias(style):
    # Cria a janela de propriedades
    janela = cw.janelaScroll('Preferencias', geometry=(300,200), resizable=(False, False), command=lambda:aplicar())

    ttk.Label(janela, text='Tema').pack(padx=5, pady=2, side='left')
    temas = list(style.theme_names())
    tema_sel = ttk.Combobox(janela, values=temas, state='readonly', width=10)
    tema_sel.pack(padx=5, pady=2, side='right')
    tema_sel.current(temas.index(style.theme_use()))

    def aplicar():
        style.theme_use(tema_sel.get())

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