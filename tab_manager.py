import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import widget_manager as wm
import custom_widgets as cw
import modbus as mb
import config as cfg

# Variáveis Locais
caminho_imagem = None

########## Criar um projeto/aba ##########
def novo_projeto(root):
    # Cria o notebook principal
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)
    notebook.bind("<Button-3>", lambda e: menu_contexto_aba(e, notebook))

    # Configura os servidores
    servidores = mb.criar_conexao()

    # Cria a primeira aba
    canvas = nova_aba(notebook)
    return canvas
    
def nova_aba(notebook, x=None, y=None):
    # Cria a aba
    aba_canvas = ttk.Frame(notebook)
    # Canvas
    if x and y:
        canvas = tk.Canvas(aba_canvas, width=x, height=y, bg='white', borderwidth=0, highlightthickness=0)
    else:
        canvas = tk.Canvas(aba_canvas, width=cfg.tamanho_x, height=cfg.tamanho_y, bg='white', borderwidth=0, highlightthickness=0)
    canvas.pack()
    canvas.bind('<Button-3>', lambda e: wm.menu_contexto_canvas(e, canvas))

    # Adiciona a aba ao notebook
    notebook.add(aba_canvas, text='Nova aba')
    notebook.select(aba_canvas)  # foca na nova aba

    return canvas

def menu_contexto_aba(event, notebook):
    context_menu = tk.Menu(notebook, tearoff=0)
    context_menu.add_command(label='Mudar nome', command=lambda: mudar_nome(event, notebook))
    context_menu.add_command(label='Excluir aba', command=lambda: excluir_aba_projeto(event, notebook))
    context_menu.post(event.x_root, event.y_root)

def mudar_nome(event, notebook):
    index = notebook.index(f"@{event.x},{event.y}")
    nome = cw.perguntarTexto('Novo nome', 'Insira o novo nome da aba')
    notebook.tab(index, text=nome)

########## Excluir um projeto/aba ##########
def excluir_aba_projeto(event, notebook):
    try:
        index = notebook.index(f"@{event.x},{event.y}")
        notebook.forget(index)
    except tk.TclError:
        pass

########## Funções auxiliares ##########
def alterar_tamanho_canvas(canvas):
    x_atual = canvas.winfo_width()
    y_atual = canvas.winfo_height()

    janela = tk.Toplevel()
    janela.resizable(False, False)

    ttk.Label(janela, text='Insira o novo tamanho').pack(side='top')

    frame = ttk.Frame(janela)
    x = ttk.Entry(frame, width=10)
    x.pack(side='left')
    x.insert(0, x_atual)
    y = ttk.Entry(frame, width=10)
    y.pack(side='left')
    y.insert(0, y_atual)
    frame.pack(pady=(0,5))

    ttk.Button(janela, text='Aplicar', command=lambda:aplicar(x,y)).pack(side='bottom', pady=(0,5))

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