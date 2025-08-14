import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import colorchooser
from PIL import Image, ImageTk
import unicodedata
import json
import config as cfg

# Variáveis Locais
widgets_ids = []
caminho_imagem = None
contador_abas = 0

########## Criar um projeto/aba ##########
def novo_projeto(notebook, nome=None, x=None, y=None):
    global contador_abas
    # Cria a aba
    aba_canvas = tk.Frame(notebook, bg=cfg.bg)
    contador_abas += 1
    # Canvas
    if x and y:
        canvas = tk.Canvas(aba_canvas, width=x, height=y, bg='white', borderwidth=0, highlightthickness=0)
        canvas.pack()
        canvas.bind('<Button-1>', lambda e: adicionar_widget(e.x, e.y, canvas))
        canvas.bind('<Button-3>', lambda e: menu_contexto_canvas(e, canvas))
    else:
        canvas = tk.Canvas(aba_canvas, width=cfg.tamanho_x, height=cfg.tamanho_y, bg='white', borderwidth=0, highlightthickness=0)
        canvas.pack()
        canvas.bind('<Button-1>', lambda e: adicionar_widget(e.x, e.y, canvas))
        canvas.bind('<Button-3>', lambda e: menu_contexto_canvas(e, canvas))
    # Adiciona a aba ao notebook
    notebook.add(aba_canvas, text=nome if nome else f'Novo_Projeto_{contador_abas}')
    notebook.select(aba_canvas)  # foca na nova aba

    return canvas

########## Excluir um projeto/aba ##########
def excluir_aba_projeto(event, notebook):
    try:
        index = notebook.index(f"@{event.x},{event.y}")
        notebook.forget(index)
    except tk.TclError:
        pass

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

########## Funções auxiliares ##########
def alterar_tamanho_canvas(canvas):
    x_atual = canvas.winfo_width()
    y_atual = canvas.winfo_height()

    janela = tk.Toplevel()
    janela.resizable(False, False)

    tk.Label(janela, text='Insira o novo tamanho').pack(side='top')

    frame = tk.Frame(janela)
    x = tk.Entry(frame, width=10)
    x.pack(side='left')
    x.insert(0, x_atual)
    y = tk.Entry(frame, width=10)
    y.pack(side='left')
    y.insert(0, y_atual)
    frame.pack(pady=(0,5))

    tk.Button(janela, text='Aplicar', command=lambda:aplicar(x,y)).pack(side='bottom', pady=(0,5))

    def aplicar(x,y):
        canvas.config(width=x.get(), height=y.get())
        janela.destroy()

def inserir_imagem(canvas):
    global caminho_imagem
    caminho_imagem = filedialog.askopenfilename(
        filetypes=[('Imagens', '*.jpg;*.png;*.jpeg;*.gif'), ('Todos os arquivos', '*.*')],
        title='Abrir arquivo'
    )
    if not caminho_imagem:
        return
    canvas.image_ref = ImageTk.PhotoImage(Image.open(caminho_imagem))
    canvas.create_image(canvas.winfo_width()/2, canvas.winfo_height()/2, anchor='center', image=canvas.image_ref)

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
