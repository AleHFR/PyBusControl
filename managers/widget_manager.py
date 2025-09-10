########### Preâmbulo ###########
# Imports do python
import customtkinter as ctk
from CTkColorPicker import AskColor
from tkinter import messagebox
from tkinter import filedialog
import asyncio

# Imports do projeto
import PyBusControl.interface.personalized as cw
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
    aba = projeto.notebook.tab(projeto.notebook.select(), 'text')
    canvas_atual = projeto.abas[aba]['canvas']
    
    # Habilita o click na tela pra definir onde o widget vai ficar
    def click(event):
        # Muda o cursor pra seta
        canvas_atual.config(cursor="arrow")
        dica.hide_tooltip()
        # salva posição
        x, y = event.x, event.y

        # Cria o widget e remove o marcador
        def ok(tipo):
            classe = dt.widgets_padrao[tipo]['classe']
            propriedades = dt.widgets_padrao[tipo]['propriedades']
            projeto.add_widget(classe, propriedades, x, y)

        # Seleciona o widget
        context_menu = cw.customMenu(canvas_atual)
        for tipo in dt.widgets_padrao.keys():
            context_menu.add_command(label=tipo, command=lambda t=tipo:ok(t))
        context_menu.post(event.x_root, event.y_root)
        context_menu.config()

        # Desabilita o bind
        canvas_atual.unbind("<Button-1>")
        
    # Muda o cursor pra cruz
    canvas_atual.config(cursor="tcross")
    # Chama o bind e escreve a dica
    dica = cw.ClickTooltip(canvas_atual, text='Clique para adicionar um widget')
    dica.show_tooltip()
    canvas_atual.bind("<Button-1>", lambda e:click(e))

def configurar_comando(projeto, wid):
    # Encontra o que for preciso
    nome_aba = projeto.notebook.tab(projeto.notebook.select(), 'text')
    widget = projeto.abas[nome_aba]['widgets'][wid]
    servidores = projeto.servidores

    # Cria a janela
    janela = cw.customTopLevel('Configurar Comando', geometry=(300, 400), buttonSet=True, scrollbar=True, resizable=(False, False), command=lambda:salvar_comando())

    # Combobox com as funções disponíveis
    ctk.CTkLabel(janela.frame_interno, text='Modbus:').pack(pady=5)
    frame_1 = ctk.CTkFrame(janela.frame_interno)
    frame_1.pack(fill='x', pady=2, padx=2)
    ctk.CTkLabel(frame_1, text='Servidor:').pack(side='left', padx=5)
    combo_server = ctk.CTkComboBox(frame_1, values=list(projeto.servidores.keys()), state='readonly', width=170, command=lambda e:atualizar_campos())
    combo_server.pack(side='right')
    frame_2 = ctk.CTkFrame(janela.frame_interno)
    frame_2.pack(fill='x', pady=2, padx=2)
    ctk.CTkLabel(frame_2, text='Comando:').pack(side='left', padx=5)
    combo_comando = ctk.CTkComboBox(frame_2, values=list(dt.funcoes_modbus.keys()), state='readonly', width=170, command=lambda e:atualizar_campos())
    combo_comando.pack(side='right')

    # Frame para os parâmetros
    frame_parametros = ctk.CTkFrame(janela.frame_interno)
    frame_parametros.pack(side='right', fill='both', expand=True, padx=5, pady=5)
    ctk.CTkLabel(frame_parametros, text='Parâmetros').pack(pady=5, fill='x', anchor='nw')

    # Função para atualizar os parâmetros de acordo com a função selecionada
    def atualizar_campos():
        if not combo_comando.get() or not combo_server.get():
            return
        
        # Pega o valor dos Combobox
        server = combo_server.get()
        comando = combo_comando.get()
        
        # Limpa todos os widgets antigos do frame de parâmetros
        for child in frame_parametros.winfo_children()[1:]:
            child.destroy()

        # Cria todos os campos de parâmetros dinamicamente
        for param, value in dt.funcoes_modbus[comando]['parametros'].items():
            # Cria um frame temporário para organizar os campos
            frame_temp = ctk.CTkFrame(frame_parametros)
            frame_temp.pack(fill='x', pady=2, padx=2)
            frame_temp.configure(fg_color=frame_parametros.cget('fg_color'))
            
            # Cria as entradas de acordo com o parâmetro
            ctk.CTkLabel(frame_temp, text=f'{param}:').pack(side='left')
            entry = None
            if type(value) == list:
                entry = ctk.CTkComboBox(frame_temp, values=value, state='readonly', width=100)
                entry.set(value[0])
            else:
                entry = ctk.CTkEntry(frame_temp, width=100)
                entry.insert(0, value)
            entry.pack(side='right')
    
    def salvar_comando():
        if not combo_comando.get() or not combo_server.get():
            return
        
        # Pega o valor dos Combobox
        server = combo_server.get()
        server_idx = str(servidores[server]['configs']['ID'])
        comando = combo_comando.get()
        # Dicionário com as informações
        comando_dict = {'servidor': server, 'servidor_idx': server_idx, 'funcao': comando, 'parametros': {}}
        # Pega a chave e valor
        for frame in frame_parametros.winfo_children()[1:]:
            label_widget = frame.winfo_children()[0]
            entry_widget = frame.winfo_children()[1]
            chave = label_widget.cget('text').replace(':', '')
            valor = entry_widget.get()
            # Atualiza o widget
            comando_dict['parametros'][chave] = valor
        widget['comando'] = comando_dict
        item = widget['item']
        item.configure(command=lambda:executar_comando(projeto, widget['comando']))

def executar_comando(projeto, comando_dict):
    operacao = asyncio.run_coroutine_threadsafe(comando(projeto, comando_dict),loop)
async def comando(projeto, comando_dict):
    nome_servidor = comando_dict['servidor']
    comando = comando_dict['funcao']
    address = comando_dict['parametros']['address']
    value = comando_dict['parametros']['value'] if 'value' in comando_dict['parametros'].keys() else None
    await asyncio.gather(projeto.command_servidor(nome_servidor, comando, address, value))

def configurar_visual(projeto, wid):
    # Encontra o Widget
    nome_aba = projeto.notebook.tab(projeto.notebook.select(), 'text')
    widget = projeto.abas[nome_aba]['widgets'][wid]
    # Cria a janela
    janela = cw.customTopLevel('Configurar Visual', geometry=(450, 400), resizable=(False, False), command=lambda:salvar_widget())
    # Funções auxiliares
    def escolher_cor(bt_cor):
        cor = AskColor().get()
        if cor is not None:
            bt_cor.configure(fg_color=cor)
    def buscar_imagem(entry_img):
        caminho_imagem = filedialog.askopenfilename()
        entry_img.insert(0, caminho_imagem)
        
    # Cria todos os campos de parâmetros dinamicamente
    for param, value in widget['propriedades'].items():
        # Cria um frame temporário simplesmente pra organizar os campos
        frame_temp = ctk.CTkFrame(janela.frame_interno, fg_color='transparent')
        frame_temp.pack(fill='x', pady=2, padx=2)
        nome = dt.traducoes_parametros[param]
        ctk.CTkLabel(frame_temp, text=f'{nome}:').pack(side='left')

        # Cria as entrys de acordo com a propriedade
        if param in dt.parametros_especiais['cores']:
            bt_cor = ctk.CTkButton(frame_temp, text='', width=200, fg_color=value)
            bt_cor.pack(side='right')
            bt_cor.configure(command=lambda bt=bt_cor:escolher_cor(bt))
        elif param in dt.parametros_especiais['numericos']: # Parametros numericos
            spinbox = cw.customSpinbox(frame_temp, initial_value=value, max_value=255, width=200)
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

    # Função para salvar o widget
    def salvar_widget():
        # Pega a chave e valor
        for frame in janela.frame_interno.winfo_children():
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
            elif param == 'image':
                valor = frame.winfo_children()[1].get()
            else:
                valor = frame.winfo_children()[1].get()
            # Atualiza o widget
            print(f'{param}: {valor}')
            projeto.config_widget(wid, param, valor)