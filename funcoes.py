import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import colorchooser
import json
import config as cfg

# Variáveis Locais
item_selecionado = None
modo_edicao = False
widgets_ids = []
contador_abas = 0

def salvar_projeto(canvas):
    from tkinter import filedialog
    import json

    # Pergunta onde salvar
    caminho = filedialog.asksaveasfilename(
        defaultextension='.json',
        filetypes=[('Arquivos JSON', '*.json'), ('Todos os arquivos', '*.*')],
        title='Salvar arquivo como'
    )
    if not caminho:
        return

    # Cria dicionário reverso: {tk.Button: 'Botão', ...}
    classe_para_tipo = {v['classe']: k for k, v in cfg.tipos_widgets.items()}

    # Percorre os widgets do canvas
    widgets_canvas = []
    for item_id in canvas.find_all():
        if canvas.type(item_id) == 'window':
            widget = canvas.nametowidget(canvas.itemcget(item_id, 'window'))
            x, y = canvas.coords(item_id)

            # Pega a classe e resolve o nome do tipo
            classe = widget.__class__
            tipo = classe_para_tipo.get(classe)
            if not tipo:
                print(f"Tipo desconhecido para classe: {classe}")
                continue

            # Pega propriedades
            props = {prop: widget.cget(prop) for prop in widget.config()}

            widgets_canvas.append({
                'tipo': tipo,
                'x': x,
                'y': y,
                'propriedades': props
            })

    # Salva tudo em JSON
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump({'widgets': widgets_canvas}, f, indent=4, ensure_ascii=False)
        
def carregar_projeto(notebook):
    global widgets_ids
    widgets_ids = []
    # Procura o arquivo
    caminho = filedialog.askopenfile(
        defaultextension='.json',
        filetypes=[('Arquivos JSON', '*.json'), ('Todos os arquivos', '*.*')],
        title='Abrir arquivo'
    )
    if not caminho:
        return

    # Área de desenho
    nome = caminho.name.split('/')[-1].replace('.json','')
    canvas = novo_projeto(notebook, nome=nome)
    
    # Lê o arquivo com os widgets
    with open(caminho.name, 'r', encoding='utf-8') as arquivo:
        widgets = json.load(arquivo)
    for widget in widgets:
        tipo = widget['tipo']
        x = widget['x']
        y = widget['y']
        item_id = adicionar_widget(x, y, canvas, widget)
        widgets_ids.append([tipo,item_id])

def novo_projeto(notebook, nome=None):
    global modo_edicao, contador_abas
    # Cria a aba
    aba_canvas = tk.Frame(notebook, bg=cfg.bg)
    contador_abas += 1
    # Canvas
    canvas = tk.Canvas(aba_canvas, width=cfg.tamanho_x, height=cfg.tamanho_y, relief='groove', bd=1, bg='white')
    canvas.pack(side='top')
    canvas.bind('<Button-1>', lambda e: adicionar_widget(e.x, e.y, canvas))
    canvas.bind('<Button-3>', lambda e: menu_contexto_canvas(e, canvas))
    # Adiciona a aba ao notebook
    notebook.add(aba_canvas, text=nome if nome else f'Novo_Projeto_{contador_abas}')
    notebook.select(aba_canvas)  # foca na nova aba

    return canvas

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

########## Funções de edição de widgets ##########
def adicionar_widget(x, y, canvas, widget):
    global widgets_ids
    if isinstance(widget, dict):
        props = {}
        for prop in widget.config():
            props[prop] = widget.cget(prop)
            classe = widget.__class__
    else:
        widget = cfg.tipos_widgets.get(widget)
        props = widget.get('propriedades', {})
        classe = widget['classe']
        
    # Cria o widget e insere no canvas
    w = classe(canvas, **props)
    item_id = canvas.create_window(x, y, window=w, anchor='nw')
    widgets_ids.append([classe.__name__,item_id])
    w.bind('<Button-3>', lambda e, i=item_id: menu_contexto_widget(e, i, canvas))

    return item_id

########## Funções Auxiliares ##########
def menu_contexto_canvas(event, canvas):
    context_menu_canvas = tk.Menu(canvas, tearoff=0)
    context_submenu_canvas = tk.Menu(canvas, tearoff=0)
    x = event.x
    y = event.y
    for widget, classe in cfg.tipos_widgets.items():
        context_submenu_canvas.add_command(
            label=widget,
            command=lambda w=widget: adicionar_widget(x, y, canvas, w)
        )
    context_menu_canvas.add_cascade(label='Inserir Widget',menu=context_submenu_canvas)
    context_menu_canvas.add_command(label='Alterar tamanho')
    context_menu_canvas.add_command(label='Imagem de fundo')
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

def propiedades_widget(item_id, canvas):
    for i, (tipo, id) in enumerate(widgets_ids):
        if id == item_id:
            widget = canvas.nametowidget(canvas.itemcget(item_id, 'window'))
            def aplicar():
                valor = entrada.get()
                widget.config(**{prop: valor})
                janela.destroy()

            janela = tk.Toplevel()
            tk.Label(janela, text=f'Novo valor para {prop}:').pack(pady=5)
            entrada = tk.Entry(janela)
            entrada.pack(pady=5)
            tk.Button(janela, text='Aplicar', command=aplicar).pack(pady=5)
            janela.grab_set()
            break

def excluir(item_id, canvas):
    # Remove o widget do canvas e da lista de ids
    global widgets_ids
    for i, (tipo, id) in enumerate(widgets_ids):
        if id == item_id:
            widget = canvas.nametowidget(canvas.itemcget(item_id, 'window'))
            widget.destroy()
            canvas.delete(item_id)
            widgets_ids.remove(i)