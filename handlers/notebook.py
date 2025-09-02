########### Preâmbulo ###########
import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image

class Aba:
    def __init__(self, notebook):
        self.notebook = notebook
        self.idx = None
        self.tamanho = (0,0) # (x, y)
        self.canvas = None
        self.imagem = ''
        self.widgets = {}
    
    ########## Adiciona uma aba no notebook ##########
    def add(self, x=None, y=None):
        # Tamanho padrão
        x = x or 1280
        y = y or 780
        # Cria frame/canvas
        aba_canvas = ctk.CTkFrame(self.notebook)
        canvas = tk.Canvas(aba_canvas, width=x, height=y, bg='white', borderwidth=0, highlightthickness=0)
        canvas.pack()
        # Altera as infos
        self.tamanho = (x, y)
        self.canvas = canvas
        # Bind menu contexto
        # canvas.bind('<Button-3>', lambda event: menuContexto_aba(event))
        # Retorna o frame
        return aba_canvas

    ########## Mudar o nome da aba ##########
    def novoNome(self, novo_nome):
        self.notebook.tab(self.idx, text=novo_nome)
    
    ########## Alterar tamanho da aba (do canvas) ##########
    def novoTamanho(self, novo_tamanho):
        x, y = novo_tamanho
        self.canvas.config(width=x, height=y)
        self.tamanho = (x, y)

    ########## Inserir imagem na aba (no canvas) ##########
    def novaImagem(self, caminho_imagem=None):
        if not caminho_imagem:
            return
        self.canvas.image_ref = ImageTk.PhotoImage(Image.open(caminho_imagem))
        self.canvas.create_image(
            self.canvas.winfo_width()/2,
            self.canvas.winfo_height()/2,
            image=self.canvas.image_ref,
            anchor='center')
        self.imagem = caminho_imagem

    ########## Excluir um projeto/aba ##########
    def delete(self):
        self.notebook.forget(self.idx)