import tkinter as tk
from tkinter import ttk
import custom_widgets as cw

def preferencias(style):
    def aplicar():
        style.theme_use(tema_sel.get())

    # Cria a janela de propriedades
    janela = cw.menuPropriedades('Preferencias', geometry=(300,200), resizable=(False, False), command=aplicar)

    ttk.Label(janela, text='Tema').pack(padx=5, pady=2, side='left')
    temas = list(style.theme_names())
    tema_sel = ttk.Combobox(janela, values=temas, state='readonly', width=10)
    tema_sel.pack(padx=5, pady=2, side='right')
    tema_sel.current(temas.index(style.theme_use()))

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