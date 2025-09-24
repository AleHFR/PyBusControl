########### Preâmbulo ############
# Imports do python
import tkinter as tk
import customtkinter as ctk
from CTkColorPicker import AskColor
from tkinter import messagebox
from tkinter import filedialog
import asyncio
import inspect

# Imports do projeto
import interface.customizados as ct
import drivers.widgets_driver as wd
import dicts as dt
from async_loop import loop

# Dicionário para salvar os icones das imagens
imagens = {}

#################### Adicionar um widget ####################
def adicionar_widget(projeto):
    # Verifica se tem ao menos uma aba aberta
    if not projeto.notebook.tabs():
        messagebox.showerror('Erro', 'Nenhuma aba existente')
        return

    # Procura a aba e o canvas
    frame = projeto.notebook.select()
    nome_aba = projeto.notebook.tab(frame, 'text')
    aba = projeto.abas[nome_aba]
    canvas = aba.canvas
    
    # Habilita o click na tela pra definir onde o widget vai ficar
    def click(event):
        # Muda o cursor pra seta
        canvas.config(cursor="arrow")
        dica.hide_tooltip()
        # salva posição
        x, y = event.x, event.y

        # Cria o widget e remove o marcador
        def ok(tipo):
            classe = dt.widgets_padrao[tipo]['classe']
            propriedades = dt.widgets_padrao[tipo]['visual'].copy()
            projeto.add_widget(classe, propriedades, x, y)

        # Encontra as classes de widgets
        classes_encontradas = list(dt.widgets_padrao.keys())
        # Cria um minimeu pra selecionar o widget
        context_menu = ct.customMenu(canvas)
        for tipo in classes_encontradas:
            context_menu.add_command(label=tipo, command=lambda t=tipo:ok(t))
        context_menu.post(event.x_root, event.y_root)
        context_menu.config()

        # Desabilita o bind
        canvas.unbind("<Button-1>")
        
    # Muda o cursor pra cruz
    canvas.config(cursor="tcross")
    # Chama o bind e escreve a dica
    dica = ct.ClickTooltip(canvas, text='Clique para adicionar um widget')
    dica.show_tooltip()
    canvas.bind("<Button-1>", lambda e:click(e))

def propriedades(projeto, wid):
    # Encontra od atributos necessários
    frame = projeto.notebook.select()
    nome_aba = projeto.notebook.tab(frame, 'text')
    aba = projeto.abas[nome_aba]
    widget = aba.widgets[wid]
    item = widget.item
    classe = widget.__class__.__name__

    # Cria a janela
    janela = ct.customTopLevel('Propriedades', geometry=(400, 400), buttonSet=True, resizable=(False, False), Notebook=True, command=lambda:salvar())

    # Funções auxiliares
    def escolher_cor(bt_cor):
        cor = AskColor().get()
        if cor is not None:
            bt_cor.configure(fg_color=cor)
    def buscar_imagem(entry_img):
        caminho_imagem = filedialog.askopenfilename()
        entry_img.delete(0, ctk.END)
        entry_img.insert(0, caminho_imagem)
    def salvar():
        # Verifica se o widget pode ter comando
        nonlocal comando
        if comando != []:
            # Puxa as informaçoes referentes ao comando
            server = server_sel.get()
            comando = comando_sel.get()
            if server and comando:
                # Cria o dicionário
                comando_dict = {'servidor': server, 'comando': comando, 'parametros': {}}
                # Itera dentro da janela
                for frame in frame_comando.winfo_children():
                    label_widget = frame.winfo_children()[0]
                    entry_widget = frame.winfo_children()[1]
                    chave = label_widget.cget('text').replace(':', '')
                    valor = entry_widget.get()
                    # Insere no dicionário
                    comando_dict['parametros'][chave] = valor
                widget.comando = comando_dict
                servidor = projeto.servidores[server].client
                try:
                    item.configure(command=lambda:executar_comando(projeto, widget))
                except:
                    executar_comando(projeto, widget)

        # Puxa as informaçoes referentes ao visual
        for frame in aba_visual.winfo_children():
            label = frame.winfo_children()[0].cget('text').replace(':', '')
            param = dt.traducoes_reverse[label]
            valor = None
            if param in dt.parametros_especiais['cores']:
                valor = frame.winfo_children()[1].cget('fg_color')
            elif param in dt.parametros_especiais['numericos']:
                valor = frame.winfo_children()[1].get()
            elif param in dt.parametros_especiais['pre-definidos'].keys():
                valor = frame.winfo_children()[1].get()
            elif param == 'font':
                valor = (frame.winfo_children()[2].get(), frame.winfo_children()[1].get())
            else:
                valor = frame.winfo_children()[1].get()
            # Atualiza o widget
            projeto.config_widget(wid, param, valor)

    # Configura a aba de visual
    aba_visual = janela.addTab('Visual')
    # Cria todos os campos de parâmetros dinamicamente
    for param, value in widget.propriedades.items():
        # Pula algumas propriedades não pertinentes
        if param in ['textvariable']:continue
        # Cria um frame temporário simplesmente pra organizar os campos
        frame_temp = ctk.CTkFrame(aba_visual, fg_color='transparent')
        frame_temp.pack(fill='x', pady=2, padx=2)
        nome = dt.traducoes_parametros[param]
        ctk.CTkLabel(frame_temp, text=f'{nome}:').pack(side='left')

        # Cria as entrys de acordo com a propriedade
        if param in dt.parametros_especiais['cores']:
            bt_cor = ctk.CTkButton(frame_temp, text='', width=200, fg_color=value)
            bt_cor.pack(side='right')
            bt_cor.configure(command=lambda bt=bt_cor:escolher_cor(bt))
        elif param in dt.parametros_especiais['numericos']: # Parametros numericos
            spinbox = ct.customSpinbox(frame_temp, initial_value=value, max_value=255, width=200)
            spinbox.pack(side='right')
        elif param in dt.parametros_especiais['pre-definidos'].keys():
            combo = ctk.CTkComboBox(frame_temp, values=dt.parametros_especiais['pre-definidos'][param], state='readonly', width=200)
            combo.pack(side='right')
            combo.set(value)
        elif param == 'font': # Trata se é fonte, coloca estilo e tamnho separados
            style, size = value[0], value[1]
            entry_size = ctk.CTkComboBox(frame_temp, values=dt.parametros_especiais['font']['sizes'], state='readonly', width=95)
            entry_size.pack(side='right')
            entry_size.set(str(size))
            entry_style = ctk.CTkComboBox(frame_temp, values=dt.parametros_especiais['font']['styles'], state='readonly', width=95)
            entry_style.pack(side='right', padx=(0,10))
            entry_style.set(style)
        elif param == 'image': # Trata se é imagem
            entry_img = ctk.CTkEntry(frame_temp, width=170)
            entry_img.pack(side='right')
            ctk.CTkButton(frame_temp, text='...', width=25, command=lambda e=entry_img:buscar_imagem(e)).pack(side='right', padx=(0,5))
            entry_img.delete(0, ctk.END)
            entry_img.insert(0, str(value))
        else: # Parametro de texto 
            entry = ctk.CTkEntry(frame_temp, width=200)
            entry.insert(0, str(value))
            entry.pack(side='right')
    
    # Configura a aba de comando se houver
    comando = dt.widgets_padrao[classe]['comando']
    if comando != []:
        aba_comando = janela.addTab('Comando')

        servidores = list(projeto.servidores.keys())
        server_sel = janela.addItem(root=aba_comando, nome='Servidor', item=ctk.CTkComboBox, state='readonly', command=lambda event:atualizar(), values=servidores, tamanho=200)
        comando_sel = janela.addItem(root=aba_comando, nome='Comando', item=ctk.CTkComboBox, state='readonly', command=lambda event:atualizar(), values=comando, tamanho=200)

        frame_comando = ctk.CTkFrame(aba_comando, fg_color='transparent')
        frame_comando.pack(fill='x')
        def atualizar():
            if server_sel.get() and comando_sel.get():
                # Limpa os parâmetros
                for frame in frame_comando.winfo_children():
                    frame.destroy()
                # Pega os parâmetros
                parametros = dt.funcoes_modbus[comando_sel.get()]['parametros']
                for param, value in parametros.items():
                    if type(value) == list:
                        janela.addItem(root=frame_comando, nome=f'{param}:', item=ctk.CTkComboBox, state='readonly', values=value, tamanho=200)
                    else:
                        janela.addItem(root=frame_comando, nome=f'{param}:', item=ctk.CTkEntry, tamanho=200, valor_inicial=value)

def executar_comando(projeto, widget):
    # Funcões de callback
    def atualizar_display(valor):
        widget.atualizar(valor)

    def callback(valor):
        tk._default_root.after(0, atualizar_display, valor)

    # Solicita o comando ao servidor
    servidor = projeto.servidores[widget.comando['servidor']]
    comando_dict = widget.comando
    servidor.addPolling(comando_dict, callback)