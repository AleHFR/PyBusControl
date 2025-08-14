import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from widget_manager import *
from utils import *
import config as cfg

# Variáveis Locais
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