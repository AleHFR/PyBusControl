########### Preâmbulo ###########
# Imports do python
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

# Imports do projeto
import custom_widgets as cw
import widget_manager as wm
import utils as ut

########## Criar um projeto/aba ##########
class Notebook:
    def __init__(self, root):
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(side='bottom',fill='both', expand=True)
    
    def add_aba(self, projeto, x=None, y=None):
        # Menu de contexto
        def menu_contexto(event, projeto):
            context_menu = tk.Menu(self.notebook, tearoff=0)
            context_menu.add_command(label='Inserir widget', command=lambda: wm.adicionar_widget(event, projeto))
            context_menu.add_separator()
            context_menu.add_command(label='Mudar nome', command=lambda: self.mudar_nome(projeto))
            context_menu.add_command(label='Alterar tamanho', command=lambda: self.alterar_tamanho_canvas(projeto, canvas))
            context_menu.add_command(label='Inserir imagem', command=lambda: self.inserir_imagem(projeto, canvas))
            context_menu.add_command(label='Excluir aba', command=lambda: self.del_aba(projeto))
            context_menu.post(event.x_root, event.y_root)

        # Pergunta o nome da aba
        nome_aba = cw.perguntarTexto('Nome da aba', 'Insira o nome da aba:', default_text='Nova Aba')

        # Tenta criar a aba no projeto
        operacao = projeto.add_aba(nome_aba, x, y)

        if operacao:
            # Cria a aba
            aba_canvas = ttk.Frame(self.notebook)
            if x and y:
                canvas = tk.Canvas(aba_canvas, width=x, height=y, bg='white', borderwidth=0, highlightthickness=0)
            else:
                x = 1280
                y = 780
                canvas = tk.Canvas(aba_canvas, width=x, height=y, bg='white', borderwidth=0, highlightthickness=0)
            canvas.pack()
            canvas.bind('<Button-3>', lambda e: menu_contexto(e, projeto))
            # Adiciona a aba ao notebook
            self.notebook.add(aba_canvas, text=nome_aba)
            self.notebook.select(aba_canvas)
    
    ########## Mudar o nome da aba ##########
    def mudar_nome(self, projeto):
        index = self.notebook.select()
        nome_aba = self.notebook.tab(index, 'text')
        novo_nome = cw.perguntarTexto('Novo nome', 'Insira o novo nome da aba')
        operacao = projeto.mudar_nome_aba(nome_aba, novo_nome)
        if operacao:
            self.notebook.tab(index, text=novo_nome)
            projeto.dados['notebook'][novo_nome] = projeto.dados['notebook'].pop(nome_aba)
    
    ########## Excluir um projeto/aba ##########
    def del_aba(self, projeto):
        index = self.notebook.select()
        nome_aba = self.notebook.tab(index, 'text')
        if nome_aba in projeto.dados['notebook']:
            if messagebox.askyesno("Confirmar", f"Deseja excluir a aba: '{nome_aba}'?"):
                self.notebook.forget(index)
                projeto.del_aba(nome_aba)
        else:
            messagebox.showerror("Erro", f"A aba '{nome_aba}' nao existe.")
            return

    ########## Alterar tamanho do canvas ##########
    def alterar_tamanho_canvas(self, projeto, canvas):
        x_atual = canvas.winfo_width()
        y_atual = canvas.winfo_height()

        janela = cw.janelaScroll('Alterar tamanho', geometry=(150,150), resizable=(False, False), scrollbar=False, command=lambda:aplicar(x,y))

        ttk.Label(janela, text='Altura em Pixel:').pack(padx=5, pady=5)
        x = ttk.Entry(janela, width=10)
        x.pack(padx=5, pady=5)
        x.insert(0, x_atual)
        ttk.Label(janela, text='Largura em Pixel:').pack(padx=5, pady=5)
        y = ttk.Entry(janela, width=10)
        y.pack(padx=5, pady=5)
        y.insert(0, y_atual)

        def aplicar(x,y):
            x = x.get()
            y = y.get()
            canvas.config(width=x, height=y)
            nome_aba = self.notebook.tab(self.notebook.select(), 'text')
            projeto.editar_aba(nome_aba, 'x', x)
            projeto.editar_aba(nome_aba, 'y', y)

    ########## Inserir imagem no canvas ##########
    def inserir_imagem(self, projeto, canvas):
        caminho_imagem = filedialog.askopenfilename(
            filetypes=[('Imagens', '*.jpg;*.png;*.jpeg;*.gif'), ('Todos os arquivos', '*.*')],
            title='Abrir arquivo'
        )
        if not caminho_imagem:
            return
        projeto.editar_aba(self.notebook.tab(self.notebook.select(), 'text'), 'imagem', caminho_imagem)
        canvas.image_ref = ImageTk.PhotoImage(Image.open(caminho_imagem))
        canvas.create_image(canvas.winfo_width()/2, canvas.winfo_height()/2, anchor='center', image=canvas.image_ref)