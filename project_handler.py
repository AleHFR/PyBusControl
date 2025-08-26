########### Preâmbulo ###########
# Imports do python
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox, filedialog

# Imports do projeto
import server_handler as sh
import custom_widgets as cw

class Widget: 
    def __init__(self, classe):
        self.classe = getattr(tk, classe)
        self.id = None
        self.x = 0
        self.y = 0
        self.comando = None
        self.propriedades = {}

class Aba:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.canvas = None
        self.imagem = ''
        self.widgets = {}

class Projeto:
    def __init__(self, root):
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(side='bottom',fill='both', expand=True)
        self.abas = {}
        self.servidores = {}

    # Função auxiliar
    def exibir(self):
        None

    #################### Trabalhando com as abas do Notebook ####################

    ########## Adiciona uma aba no notebook ##########
    def add_aba(self, x=None, y=None):
        # Menu de contexto
        def menuContexto_aba(event):
            context_menu = tk.Menu(self.notebook, tearoff=0)
            context_menu.add_command(label='Mudar nome', command=lambda:self.novoNome_aba())
            context_menu.add_command(label='Alterar tamanho', command=lambda:self.novoTamanho_aba(canvas))
            context_menu.add_command(label='Inserir imagem', command=lambda:self.imagem_aba(canvas))
            context_menu.add_separator()
            context_menu.add_command(label='Excluir aba', command=lambda: self.del_aba())
            context_menu.post(event.x_root, event.y_root)
        # Tamanho padrão
        x = x or 1280
        y = y or 780
        # Pergunta o nome da aba
        nome_aba = cw.perguntarTexto('Nome da aba', 'Insira o nome da aba:', default_text='Nova Aba')
         # Cria frame/canvas
        aba_canvas = ttk.Frame(self.notebook)
        canvas = tk.Canvas(aba_canvas, width=x, height=y, bg='white', borderwidth=0, highlightthickness=0)
        canvas.pack()
        # Cria objeto Aba
        aba = Aba()
        aba.x = x
        aba.y = y
        aba.canvas = canvas
        # Bind menu contexto
        canvas.bind('<Button-3>', lambda event: menuContexto_aba(event))
        # Adiciona no notebook
        self.notebook.add(aba_canvas, text=nome_aba)
        self.notebook.select(aba_canvas)
        # Guarda no projeto
        self.abas[nome_aba] = aba
        self.exibir()

    ########## Mudar o nome da aba ##########
    def novoNome_aba(self):
        index = self.notebook.select()
        novo_nome = cw.perguntarTexto('Novo nome', 'Insira o novo nome da aba')
        if novo_nome not in self.abas.keys():
            self.notebook.tab(index, text=novo_nome)
            self.abas[novo_nome] = self.abas.pop(self.notebook.tab(index, 'text'))
            self.exibir()

    ########## Excluir um projeto/aba ##########
    def del_aba(self):
        index = self.notebook.select()
        nome_aba = self.notebook.tab(index, 'text')
        if messagebox.askyesno("Confirmar", f"Deseja excluir a aba: '{nome_aba}'?"):
            self.notebook.forget(index)
            del self.abas[nome_aba]
            self.exibir()

    ########## Alterar tamanho da aba (do canvas) ##########
    def novoTamanho_aba(self, canvas):
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
            x = int(x.get())
            y = int(y.get())
            canvas.config(width=x, height=y)
            index = self.notebook.select()
            nome_aba = self.notebook.tab(index, 'text')
            self.abas[nome_aba].x = x
            self.abas[nome_aba].y = y
            self.exibir()

    ########## Inserir imagem na aba (no canvas) ##########
    def imagem_aba(self, canvas):
        caminho_imagem = filedialog.askopenfilename(
            filetypes=[('Imagens', '*.jpg;*.png;*.jpeg;*.gif'), ('Todos os arquivos', '*.*')],
            title='Abrir arquivo'
        )
        if not caminho_imagem:
            return
        
        canvas.image_ref = ImageTk.PhotoImage(Image.open(caminho_imagem))
        canvas.create_image(canvas.winfo_width()/2, canvas.winfo_height()/2, anchor='center', image=canvas.image_ref)
        index = self.notebook.select()
        nome_aba = self.notebook.tab(index, 'text')
        self.abas[nome_aba].imagem = caminho_imagem
        self.exibir()

    #################### Trabalhando com os Servidores ####################

    ########## Adicionar um servidor ##########
    def add_servidor(self, nome_servidor, conexao, configs):
        if nome_servidor not in self.servidores.keys():
            servidor = sh.Servidor(nome_servidor, conexao)
            for key, value in configs.items():
                servidor.config(key, value)
            self.servidores[nome_servidor] = servidor
        self.exibir()

    ########## Mudar o nome do servidor ##########
    def novoNome_servidor(self, nome_servidor, novo_nome_servidor):
        if novo_nome_servidor not in self.servidores.keys():
            self.servidores[novo_nome_servidor] = self.servidores[nome_servidor]
            del self.servidores[nome_servidor]
        self.exibir()

    ########## Configurar o servidor ##########
    def config_servidor(self, nome_servidor, config, valor):
        if config in self.servidores[nome_servidor].modbus.keys():
            servidor = self.servidores[nome_servidor]
            servidor.config(config, valor)
        self.exibir()

    ########## Deletar um servidor ##########
    def del_servidor(self, nome_servidor):
        if nome_servidor in self.servidores:
            del self.servidores[nome_servidor]
        self.exibir()

    ####################  Trabalhando com os Widgets das abas ####################

    ########## Adicionar um widget ##########
    def add_widget(self, classe, dados_widget, x, y):
        # Menu de contexto do Widget
        def menuContexto_widget(event, wid):
            context_menu = tk.Menu(canvas_atual, tearoff=0)
            context_menu.add_command(label='Mover', command=lambda:self.mover_widget(wid))
            context_menu.add_command(label='Excluir', command=lambda:self.del_widget(wid))
            context_menu.post(event.x_root, event.y_root)
        # Encontra aba atual
        index = self.notebook.select()
        nome_aba = self.notebook.tab(index, 'text')
        canvas_atual = self.abas[nome_aba].canvas
        # Cria o widget
        widget = Widget(classe)
        widget_tk = widget.classe(canvas_atual, **dados_widget)
        # Pega id do canvas
        widget.id = canvas_atual.create_window(x, y, window=widget_tk)
        # Cria o bind do menu de contexto
        widget_tk.bind('<Button-3>', lambda event, wid=widget.id: menuContexto_widget(event, wid))
        # Salva no projeto
        self.abas[nome_aba].widgets[widget.id] = widget
        self.exibir()

    def config_widget(self, nome_aba, nome_widget, config, novo_valor):
        widget = self.abas[nome_aba].widgets[nome_widget]
        widget.propriedades[config] = novo_valor
        self.exibir()
    
    def mover_widget(self, wid):
        # posição inicial do item no canvas
        index = self.notebook.select()
        nome_aba = self.notebook.tab(index, 'text')
        canvas_atual = self.abas[nome_aba].canvas
        x0, y0 = canvas_atual.coords(wid)

        # calcula offset entre clique e posição do widget
        def iniciar(event):
            canvas_atual._drag_data = {
                "item": wid,
                "dx": x0 - event.x,
                "dy": y0 - event.y
            }
            # ativa arrastar
            canvas_atual.bind('<Motion>', mover)
            canvas_atual.bind('<ButtonRelease-1>', parar)

        def mover(event):
            dx = canvas_atual._drag_data["dx"]
            dy = canvas_atual._drag_data["dy"]
            canvas_atual.coords(wid, event.x + dx, event.y + dy)

        def parar(event):
            canvas_atual.unbind('<Motion>')
            canvas_atual.unbind('<ButtonRelease-1>')
            canvas_atual._drag_data = {}

        # espera o clique esquerdo pra começar arrastar
        canvas_atual.bind('<Button-1>', iniciar)

    def del_widget(self, wid):
        index = self.notebook.select()
        nome_aba = self.notebook.tab(index, 'text')
        canvas_atual = self.abas[nome_aba].canvas
        widget = canvas_atual.nametowidget(canvas_atual.itemcget(wid, 'window'))
        widget.destroy()
        canvas_atual.delete(wid)