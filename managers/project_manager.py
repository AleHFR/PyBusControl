########### Preâmbulo ###########
# Imports do python
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

# Imports do projeto
import drivers.server_driver as sr
import drivers.widgets_driver as wd
import managers.widget_manager as wm
import customizados as ct

# Classe axiliar pra trabalhar com o projeto
class Aba:
    def __init__(self, tamanho:tuple):
        self.tamanho = tamanho
        self.caminho_imagem = None
        self.item = None
        self.canvas = None
        self.imagem = None
        self.widgets = {}

# Classe principal do projeto
class Projeto:
    def __init__(self, root):
        self.nome = "Novo Projeto"
        self.notebook = ct.customNotebook(root)
        self.notebook.pack(side="bottom", fill="both", expand=True)
        self.abas = {}
        self.servidores = {}

    #################### Trabalhando com as abas do Notebook ####################
    ########## Adiciona uma aba no notebook ##########
    def add_aba(self, nome):
        # Tamanho padrão
        x, y = 1280, 780
        # Adiciona uma aba
        frame = ctk.CTkFrame(self.notebook)
        canvas = tk.Canvas(frame, width=x, height=y, bg="white", borderwidth=2)
        canvas.pack()
        self.notebook.add(frame, text=nome)
        self.notebook.select(frame)
        # Guarda no projeto
        aba = Aba(tamanho=(x, y))
        aba.canvas = canvas
        aba.item = frame
        self.abas[nome] = aba

    ########## Configura uma aba no notebook ##########
    def config_aba(self, chave, valor):
        # Encontra a aba atual
        frame = self.notebook.select()
        nome_aba = self.notebook.tab(frame, "text")
        aba = self.abas[nome_aba]

        # Trata os dados de acordo com a propriedade
        if chave == "nome":
            # Verifica se já existe uma aba com esse nome e se o nome é diferente do atual
            if valor != nome_aba and valor in self.abas.keys():
                messagebox.showerror("Erro", "Já existe uma aba com esse nome.")
                return
            else:
                self.notebook.tab(frame, text=valor)
                self.abas[valor] = self.abas.pop(nome_aba)

        elif chave == "tamanho":
            x, y = valor
            aba.canvas.config(width=x, height=y)
            aba.tamanho = (x, y)

        elif chave == "imagem":
            aba.caminho_imagem = valor
            aba.imagem = ct.imagem(valor, para_tk=True)
            canvas = aba.canvas
            canvas.image_ref = aba.imagem
            canvas.create_image(
                canvas.winfo_width()/2,
                canvas.winfo_height()/2,
                image=aba.imagem,
                anchor="center"
            )

    ########## Deleta uma aba no notebook ##########
    def del_aba(self):
        # Encontra a aba atual
        frame = self.notebook.select()
        nome_aba = self.notebook.tab(frame, "text")
        # Deleta a aba e apaga do projeto
        self.notebook.forget(frame)
        del self.abas[nome_aba]

    #################### Trabalhando com os Servidores ####################
    ########## Adicionar um servidor ##########
    def add_servidor(self, nome_servidor):
        if nome_servidor not in self.servidores.keys():
            servidor = sr.Server()
            self.servidores[nome_servidor] = servidor

    ########## Mudar o nome do servidor ##########
    def novoNome_servidor(self, nome_servidor, novo_nome_servidor):
        if novo_nome_servidor not in self.servidores.keys():
            self.servidores[novo_nome_servidor] = self.servidores[nome_servidor]
            del self.servidores[nome_servidor]

    ########## Configurar o servidor ##########
    def config_servidor(self, nome_servidor, config, valor):
        servidor = self.servidores[nome_servidor]
        setattr(servidor, config, valor)

    ########## Deletar um servidor ##########
    def del_servidor(self, nome_servidor):
        if nome_servidor in self.servidores:
            del self.servidores[nome_servidor]

    ####################  Trabalhando com os Widgets das abas ####################
    ########## Adicionar um widget ##########
    def add_widget(self, classe, x, y):
        # Encontra os atributos necessários
        frame = self.notebook.select()
        nome_aba = self.notebook.tab(frame, "text")
        aba = self.abas[nome_aba]
        canvas = aba.canvas

        # Menu de contexto do Widget
        def menuContexto_widget(event):
            context_menu = ct.customMenu(canvas)
            context_menu.add_command(label="Mover", command=lambda:self.move_widget(wid))
            context_menu.add_command(label="Comando", command=lambda:wm.comando(self, wid))
            context_menu.add_command(label="Visual", command=lambda:wm.visual(self, wid))
            context_menu.add_separator()
            context_menu.add_command(label="Excluir", command=lambda:self.del_widget(wid))
            context_menu.post(event.x_root, event.y_root)

        # Cria objeto do widget
        widget = getattr(wd, classe)(canvas=canvas, posicao=(x, y))
        # Adiciona o widget na visualização
        widgetTk = widget.get() # Resgata o item do customtkinter
        widgetTk.bind("<Button-3>", lambda event: menuContexto_widget(event)) # Cria o bind do menu de contexto
        wid = canvas.create_window(x, y, window=widgetTk) # Adiciona o widget no canvas

        # Salva no projeto
        aba.widgets[wid] = widget
        return wid # Retorna o id do widget

    ########## Configurar o widget ##########
    def config_widget(self, wid, prop, novo_valor):
        # Encontra os atributos necessários
        frame = self.notebook.select()
        nome_aba = self.notebook.tab(frame, "text")
        aba = self.abas[nome_aba]
        widget = aba.widgets[wid]
        item = widget.item

        # Trata o valor se for imagem
        if prop == "image":
            widget.caminho_imagem = novo_valor # Salva o caminho da imagem
            imagem = ct.imagem(novo_valor)
            widget.image = imagem # Salva a referência da imagem
            item.configure(image=widget.image)
        # Trata o valor se for fonte
        elif prop == "font":
            fonte = ctk.CTkFont(family=novo_valor[0], size=int(novo_valor[1]))
            item.configure(font=fonte)
        # Demais valores
        else:
            item.configure(**{prop:novo_valor})

        # # Altera o widget no projeto
        widget.propriedades[prop] = novo_valor

    ########## Move o widget ##########
    def move_widget(self, wid):
        # Encontra os atributos necessários
        frame = self.notebook.select()
        nome_aba = self.notebook.tab(frame, "text")
        aba = self.abas[nome_aba]
        canvas = aba.canvas

        # posição inicial do item no canvas
        x0, y0 = canvas.coords(wid)
        # Dica
        dica = ct.customClickTooltip(canvas, text="Clique e arraste para mover o widget")
        dica.show_tooltip()

        # calcula offset entre clique e posição do widget
        def iniciar(event):
            dica.hide_tooltip()
            canvas._drag_data = {
                "item": wid,
                "dx": x0 - event.x,
                "dy": y0 - event.y
            }
            # Impede de ser arrastado novamente
            canvas.unbind("<Button-1>")
            # ativa arrastar
            canvas.bind("<Motion>", mover)
            canvas.bind("<ButtonRelease-1>", parar)

        def mover(event):
            # muda a posição do widget
            dx = canvas._drag_data["dx"]
            dy = canvas._drag_data["dy"]
            pos_x = event.x + dx
            pos_y = event.y + dy
            canvas.coords(wid, pos_x, pos_y)
            # Salva a posição no widget
            self.x = pos_x
            self.y = pos_y

        def parar(event):
            # Impede de ser arrastado novamente
            canvas.unbind("<Motion>")
            canvas.unbind("<ButtonRelease-1>")
            canvas._drag_data = {}

        # espera o clique esquerdo pra começar arrastar
        canvas.bind("<Button-1>", iniciar)
        
    ########## Deletar um widget ##########
    def del_widget(self, wid):
        # Encontra os atributos necessários
        frame = self.notebook.select()
        nome_aba = self.notebook.tab(frame, "text")
        aba = self.abas[nome_aba]
        widget = aba.widgets[wid].item
        canvas = aba.canvas

        # Deleta o widget
        widget.destroy()
        canvas.delete(wid)
        # Atualiza o projeto
        del aba.widgets[wid]
        