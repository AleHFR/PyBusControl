########### Preâmbulo ###########
# Imports do python
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox

# Imports do projeto
import handlers.server as sh
import handlers.widget as wh
import dicts as dt

class Projeto:
    def __init__(self, root):
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(side='bottom', fill='both', expand=True)
        self.abas = {}
        self.servidores = {}

    #################### Trabalhando com as abas do Notebook ####################
    ########## Adiciona uma aba no notebook ##########
    def add_aba(self, nome):
        if nome in self.abas.keys():
            messagebox.showerror('Erro', 'Já existe uma aba com esse nome.')
            return
        # Tamanho padrão
        x = 1280
        y = 780
        # Adiciona uma aba
        frame = ctk.CTkFrame(self.notebook)
        canvas = tk.Canvas(frame, width=x, height=y, bg='white', borderwidth=0, highlightthickness=0)
        canvas.pack()
        self.notebook.add(frame, text=nome)
        self.notebook.select(frame)
        # Guarda no projeto
        self.abas[nome] = {'canvas': canvas, 'widgets': {}, 'tamanho': (x, y), 'imagem': ''}

    ########## Configura uma aba no notebook ##########
    def config_aba(self, chave, valor):
        aba = self.notebook.select()
        if chave == 'nome':
            # Verifica se já existe uma aba com esse nome  e se o nome é diferente do atual
            aba = self.notebook.select()
            nome_antigo = self.notebook.tab(aba, 'text')
            if valor != nome_antigo and valor in self.abas.keys():
                messagebox.showerror('Erro', 'Já existe uma aba com esse nome.')
                return
            else:
                self.notebook.tab(aba, text=valor)
                self.abas[valor] = self.abas.pop(nome_antigo)
        elif chave == 'tamanho':
            nome = self.notebook.tab(aba, 'text')
            x, y = valor
            self.abas[nome]['canvas'].config(width=x, height=y)
        elif chave == 'imagem':
            if not valor:
                return
            nome = self.notebook.tab(aba, 'text')
            self.abas[nome]['img'] = ut.imagem(valor)
            self.abas[nome]['canvas'].image_ref = self.abas[nome]['img']
            self.abas[nome]['canvas'].create_image(self.abas[nome]['canvas'].winfo_width()/2,
                                                  self.abas[nome]['canvas'].winfo_height()/2,
                                                  image=self.abas[nome]['canvas'].image_ref,
                                                  anchor='center')

    ########## Deleta uma aba no notebook ##########
    def del_aba(self):
        aba = self.notebook.select()
        nome_aba = self.notebook.tab(aba, 'text')
        if messagebox.askyesno("Confirmar", f"Deseja excluir a aba: '{nome_aba}'?"):
            self.notebook.forget(aba)
            del self.abas[nome_aba]

    #################### Trabalhando com os Servidores ####################
    ########## Adicionar um servidor ##########
    def add_servidor(self, nome_servidor, conexao, configs):
        if nome_servidor not in self.servidores.keys():
            servidor = sh.Servidor(nome_servidor, conexao)
            for key, value in configs.items():
                servidor.config(key, value)
            self.servidores[nome_servidor] = servidor

    ########## Conecta a um servidor ##########
    def conectar_servidor(self, nome_servidor):
        if nome_servidor in self.servidores.keys():
            self.servidores[nome_servidor].conectar()

    ########## Mudar o nome do servidor ##########
    def novoNome_servidor(self, nome_servidor, novo_nome_servidor):
        if novo_nome_servidor not in self.servidores.keys():
            self.servidores[novo_nome_servidor] = self.servidores[nome_servidor]
            del self.servidores[nome_servidor]

    ########## Configurar o servidor ##########
    def config_servidor(self, nome_servidor, config, valor):
        servidor = self.servidores[nome_servidor]
        if config in servidor.modbus.keys():
            servidor.config(config, valor)

    ########## Deletar um servidor ##########
    def del_servidor(self, nome_servidor):
        if nome_servidor in self.servidores:
            del self.servidores[nome_servidor]

    ####################  Trabalhando com os Widgets das abas ####################
    ########## Adicionar um widget ##########
    def add_widget(self, classe, dados_widget, x, y):
        # Encontra aba atual
        nome_aba = self.notebook.tab(self.notebook.select(), 'text')
        canvas_atual = self.abas[nome_aba]['canvas']
        # Adiciona o widget na visualização
        widget = wh.Widget(canvas_atual, classe, dados_widget, x, y)
        # Salva no projeto
        self.abas[nome_aba]['widgets'][widget.id] = widget
        
        return widget

    ########## Configurar o widget ##########
    def config_widget(self, wid, prop, novo_valor):
        # Encontra aba atual
        nome_aba = self.notebook.tab(self.notebook.select(), 'text')
        canvas_atual = self.abas[nome_aba]['canvas']
        # Altera o widget na visualização
        widget = canvas_atual.nametowidget(canvas_atual.itemcget(wid, 'window'))
        widget.config(**{prop: novo_valor})
        # Altera o widget no projeto
        widget = self.abas[nome_aba].widgets[wid]
        widget.propriedades[prop] = novo_valor
        

    ########## Deletar um widget ##########
    def del_widget(self, wid):
        nome_aba = self.notebook.tab(self.notebook.select(), 'text')
        canvas_atual = self.abas[nome_aba]['canvas']
        widget = canvas_atual.nametowidget(canvas_atual.itemcget(wid, 'window'))
        widget.destroy()
        canvas_atual.delete(wid)
        