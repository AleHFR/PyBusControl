import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from file_handler import *
from custom_widgets import *
from utils import *
import config as cfg

# Variáveis Locais
widgets_ids = []

########## Adicionar um widget ##########
def adicionar_widget(x, y, canvas, widget):
    global widgets_ids
    # Encontra as caracteristicas do widget
    classe = getattr(tk, widget['classe'])
    props = widget.get('propriedades', {})
        
    # Cria o widget e insere no canvas
    w = classe(canvas, **props)
    item_id = canvas.create_window(x, y, window=w, anchor='nw')
    widgets_ids.append([classe.__name__,item_id])
    w.bind('<Button-3>', lambda e, i=item_id: menu_contexto_widget(e, i, canvas))

    return item_id

########## Funções de menu de contexto do canvas ##########
def menu_contexto_canvas(event, canvas):
    context_menu_canvas = tk.Menu(canvas, tearoff=0)
    context_submenu_canvas = tk.Menu(canvas, tearoff=0)
    x = event.x
    y = event.y
    for nome_widget in cfg.tipos_widgets:
        widget = cfg.tipos_widgets[nome_widget]
        context_submenu_canvas.add_command(
            label=nome_widget,
            command=lambda w=widget: adicionar_widget(x, y, canvas, w)
        )
    context_menu_canvas.add_cascade(label='Inserir Widget',menu=context_submenu_canvas)
    context_menu_canvas.add_command(label='Alterar tamanho',command=lambda:alterar_tamanho_canvas(canvas))
    context_menu_canvas.add_command(label='Imagem de fundo',command=lambda:inserir_imagem(canvas))
    context_menu_canvas.add_command(label='Tela cheia',command=lambda:tela_cheia())
    context_menu_canvas.add_separator()
    context_menu_canvas.add_command(label='Salvar',command=lambda:salvar_projeto(canvas))
    context_menu_canvas.post(event.x_root, event.y_root)

def menu_contexto_widget(event, item_id, canvas):
    context_menu = tk.Menu(canvas, tearoff=0)
    context_menu.add_command(label='Mover',command=lambda e=event:mover_widget(item_id, canvas))
    context_menu.add_command(label='Propriedades',command=lambda:propiedades_widget(item_id, canvas))
    context_menu.add_command(label='Excluir', command=lambda: excluir(item_id, canvas))

    context_menu.post(event.x_root, event.y_root)

def mover_widget(item_id, canvas):
    canvas._drag_data = {'item': item_id}

    def mover(event):
        canvas.coords(item_id, event.x, event.y)

    def parar(event):
        canvas.unbind('<Motion>')
        canvas.unbind('<Button-1>')
        canvas._drag_data = {}

    canvas.bind('<Motion>', mover)
    canvas.bind('<Button-1>', parar)

########## Função para abrir a janela de propriedades ##########
def propiedades_widget(item_id, canvas):
    for tipo, id in widgets_ids:
        if id == item_id:
            widget = canvas.nametowidget(canvas.itemcget(item_id, 'window'))
            props = {prop: widget.cget(prop) for prop in widget.config()}

            # Cria a janela de propriedades
            janela = tk.Toplevel()
            janela.title("Propriedades")
            janela.minsize(250, 300)
            janela.resizable(False, False)
            janela.columnconfigure(0, weight=1)

            # Funções auxiliares
            def escolher_cor(prop, ent, entradas):
                cor = colorchooser.askcolor(title="Escolher Cor")[1]
                if cor:
                    ent.delete(0, tk.END)  # troca o texto
                    ent.insert(0, cor)
                    ent.config(bg=cor)
                    entradas[prop] = ent

            def aplicar_propriedades(widget, entradas):
                print(entradas)
                for prop, entry in entradas.items():
                    valor = entry.get()
                    widget.config({prop: valor})
                janela.destroy()

            entradas = {}
            for i, prop in enumerate(props):
                # Pega a tradução
                texto = cfg.props_equivalentes.get(prop)
                if prop not in cfg.props_ignoradas and texto is not None:
                    # Adiciona label
                    tk.Label(janela, text=texto, anchor='w', width=15).grid(row=i, column=0, sticky='w', pady=2)
                    # Cria as entradas
                    if prop == 'font':
                        ent = ttk.Combobox(janela, values=list(cfg.listas_configs_comuns[prop]), textvariable=tk.StringVar(value=props[prop]), state='readonly', width=12)
                        ent.grid(row=i, column=1, sticky='e', pady=2)
                        entradas[prop] = ent
                    elif prop in ['justify','relief','orient']:
                        ent = ttk.Combobox(janela, values=list(cfg.listas_configs_comuns[prop]), textvariable=tk.StringVar(value=props[prop]), state='readonly', width=12)
                        ent.grid(row=i, column=1, sticky='e', pady=2)
                        entradas[prop] = ent
                    elif prop in ['fg', 'bg', 'highlightcolor', 'highlightbackground']:
                        frame_cor = tk.Frame(janela)
                        frame_cor.grid(row=i, column=1, sticky='e', pady=2)
                        ent = tk.Entry(frame_cor, width=10, bg=props[prop])
                        ent.grid(row=0, column=0, sticky='e', padx=2)
                        tk.Button(frame_cor, text='...', command=lambda p=prop, e=ent: escolher_cor(p, e, entradas)).grid(row=0, column=1, padx=2, sticky='e')
                    else:
                        ent = tk.Entry(janela, width=15)
                        ent.insert(0, props[prop])  # Preenche com valor atual
                        ent.grid(row=i, column=1, sticky='e', pady=2)
                        entradas[prop] = ent

            # Botão de aplicar
            tk.Button(janela, text='Aplicar', command=lambda: aplicar_propriedades(widget, entradas)).grid(row=i+1, column=0, columnspan=2, sticky='s', pady=5)

            break

########## Excluir widget ##########
def excluir(item_id, canvas):
    # Remove o widget do canvas e da lista de ids
    global widgets_ids
    for tipo, id in widgets_ids:
        if id == item_id:
            widget = canvas.nametowidget(canvas.itemcget(item_id, 'window'))
            widget.destroy()
            canvas.delete(item_id)
            widgets_ids.remove([tipo, id])
