import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
import tab_manager as tm
import file_handler as fh
import custom_widgets as cw
import utils as ut
import config as cfg

# Variáveis Locais
widgets_ids = []

########## Adicionar um widget ##########
def adicionar_widget(x, y, canvas, widget):
    global widgets_ids
    # Encontra as caracteristicas do widget
    classe = getattr(ttk, widget['classe'])
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
    context_menu_canvas.add_command(label='Alterar tamanho',command=lambda:tm.alterar_tamanho_canvas(canvas))
    context_menu_canvas.add_command(label='Imagem de fundo',command=lambda:tm.inserir_imagem(canvas))
    context_menu_canvas.post(event.x_root, event.y_root)

def menu_contexto_widget(event, item_id, canvas):
    context_menu = tk.Menu(canvas, tearoff=0)
    context_menu.add_command(label='Mover',command=lambda e=event:mover_widget(item_id, canvas))
    context_menu.add_command(label='Propriedades',command=lambda:propriedades_widget(item_id, canvas))
    context_menu.add_command(label='Personalizar',command=lambda:personalizar_widget(item_id, canvas))
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

########## Função de propriedades do widget ##########
def propriedades_widget(item_id, canvas):
    None

########## Função de personalizar a aparencia do widget ##########
def personalizar_widget(item_id, canvas):
    for tipo, id in widgets_ids:
        if id == item_id:
            widget = canvas.nametowidget(canvas.itemcget(item_id, 'window'))

            # Cria a janela de propriedades
            janela = cw.menuPropriedades('Personalização', resizable=(False, False), command=lambda:aplicar_propriedades())

            def aplicar_propriedades():
                janela.destroy()

            entradas = {}
            def escolher_cor(entry, valor):
                cor = colorchooser.askcolor(title="Escolher Cor", initialcolor=valor)[1]
                entry.delete(0, 'end')
                entry.insert(0, cor)
                entradas[prop] = cor

            props = {prop: widget.cget(prop) for prop in widget.config()}
            nomes = cfg.props_equivalentes.get(tipo)

            for i, prop in enumerate(props):
                print(props)
                if prop not in cfg.props_ignoradas:
                    nome = nomes.get(prop)
                    valor = props[prop]
                    ttk.Label(janela, text=nome, anchor='w', width=25).grid(row=i, column=0, pady=5)
                    if prop in cfg.props_selecionaveis:
                        ent = ttk.Combobox(janela, values=list(cfg.props_selecionaveis[prop]), textvariable=tk.StringVar(value=valor), state='readonly', width=12)
                        ent.grid(row=i, column=1, pady=5)
                        entradas[prop] = ent

                    elif prop in cfg.props_cor:
                        frame_cor = ttk.Frame(janela)
                        frame_cor.grid(row=i, column=1, pady=5)
                        ent = ttk.Entry(frame_cor, width=10)
                        ent.pack(side='left', padx=2)
                        ttk.Button(frame_cor, text='...', command=lambda e=ent, v=valor: escolher_cor(e, v)).pack(side='left', padx=5)

                    else:
                        ent = ttk.Entry(janela, textvariable=tk.StringVar(value=valor), width=12)
                        ent.grid(row=i, column=1, pady=2)
                        entradas[prop] = ent

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