########### Preâmbulo ###########
# Imports do python
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

# Imports do projeto
import widget_manager as wm
import file_handler as fh
import custom_widgets as cw
import modbus_settings as ms
import scada_settings as ss
import utils as ut

# Variáveis Locais
caminho_imagem = None

########## Criar um projeto/aba ##########
def novo_projeto(root, projeto):
    # Cria a barra de edição
    barra_ferramentas = ttk.LabelFrame(root, text='Novo Projeto')
    barra_ferramentas.pack(side='top', anchor='nw', fill='x', padx=2, pady=2)
    ttk.Button(barra_ferramentas, text='Nova Aba', command=lambda:nova_aba(notebook, projeto)).pack(side='left', padx=5, pady=2)
    ttk.Button(barra_ferramentas, text='Configurar Servidores', command=lambda:ms.criar_conexao(projeto)).pack(side='left', padx=5, pady=2)
    ttk.Button(barra_ferramentas, text='Tela Cheia', command=lambda:ut.tela_cheia()).pack(side='left', padx=5, pady=2)

    # Cria o notebook principalpil
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)
    notebook.bind('<Button-2>', lambda e: excluir_aba(e, notebook, projeto))
    notebook.bind("<Button-3>", lambda e: menu_contexto_aba(e, notebook, projeto))

    # Cria a primeira aba
    canvas = nova_aba(notebook, projeto)
    return canvas
    
def nova_aba(notebook, projeto, x=None, y=None):
    # Cria a aba
    aba_canvas = ttk.Frame(notebook)
    # Canvas
    if x and y:
        canvas = tk.Canvas(aba_canvas, width=x, height=y, bg='white', borderwidth=0, highlightthickness=0)
    else:
        canvas = tk.Canvas(aba_canvas, width=1280, height=780, bg='white', borderwidth=0, highlightthickness=0)
    canvas.pack()
    canvas.bind('<Button-3>', lambda e: menu_contexto_canvas(e, canvas, notebook, projeto))

    # Pergunta o nome da aba
    nome = cw.perguntarTexto('Nome da aba', 'Insira o nome da aba:', default_text='Nova Aba')
    # aba_canvas.configure(text=nome)

    # Atualiza o projeto
    operacao = projeto.add_aba(nome, canvas.winfo_width(), canvas.winfo_height())

    # Adiciona a aba ao notebook
    if operacao:
        notebook.add(aba_canvas, text=nome)
        notebook.select(aba_canvas)

    projeto.exibir() 

    return canvas

# Menu de Contexto da aba
def menu_contexto_aba(event, notebook, projeto):
    context_menu = tk.Menu(notebook, tearoff=0)
    context_menu.add_command(label='Mudar nome', command=lambda: mudar_nome(event, notebook, projeto))
    context_menu.add_command(label='Excluir aba', command=lambda: excluir_aba(event, notebook, projeto))
    context_menu.post(event.x_root, event.y_root)

# Menu de Contexto da aba
def menu_contexto_canvas(event, canvas, notebook, projeto):
    context_menu_canvas = tk.Menu(canvas, tearoff=0)
    context_menu_canvas.add_command(label='Inserir Widget',command=lambda:wm.adicionar_widget(event.x, event.y, canvas, projeto))
    context_menu_canvas.add_command(label='Alterar tamanho',command=lambda:alterar_tamanho_canvas(canvas, notebook, projeto))
    context_menu_canvas.add_command(label='Imagem de fundo',command=lambda:inserir_imagem(canvas, notebook, projeto))
    context_menu_canvas.post(event.x_root, event.y_root)

def mudar_nome(event, notebook, projeto):
    index = notebook.index(f"@{event.x},{event.y}")
    nome_aba = notebook.tab(index, 'text')
    novo_nome = cw.perguntarTexto('Novo nome', 'Insira o novo nome da aba')
    operacao = projeto.mudar_nome_aba(nome_aba, novo_nome)
    if operacao:
        notebook.tab(index, text=novo_nome)
    projeto.exibir()

########## Excluir um projeto/aba ##########
def excluir_aba(event, notebook, projeto):
    try:
        index = notebook.index(f"@{event.x},{event.y}")
        nome_aba = notebook.tab(index, 'text')
        projeto.del_aba(nome_aba)
        notebook.forget(index)
        projeto.exibir()
    except tk.TclError:
        pass

########## Funções auxiliares ##########
def alterar_tamanho_canvas(canvas, notebook, projeto):
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

def inserir_imagem(canvas, notebook, projeto):
    global caminho_imagem
    caminho_imagem = filedialog.askopenfilename(
        filetypes=[('Imagens', '*.jpg;*.png;*.jpeg;*.gif'), ('Todos os arquivos', '*.*')],
        title='Abrir arquivo'
    )
    if not caminho_imagem:
        return
    projeto.editar_aba(notebook.tab(notebook.select(), 'text'), 'imagem', caminho_imagem)
    canvas.image_ref = ImageTk.PhotoImage(Image.open(caminho_imagem))
    canvas.create_image(canvas.winfo_width()/2, canvas.winfo_height()/2, anchor='center', image=canvas.image_ref)