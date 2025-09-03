########### Preâmbulo ###########
# Imports do python
import tkinter as tk
import customtkinter as ctk
from CTkColorPicker import AskColor
from tkinter import messagebox
from tkinter import filedialog

# Imports do projeto
import custom_widgets as cw
import dicts as dt

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
        cw.dica() # Reseta a dica
        # salva posição
        x, y = event.x, event.y
        # cria marcador
        r = 5
        marcador = canvas_atual.create_oval(x-r, y-r, x+r, y+r, outline="black", width=2)

        # Cria o widget e remove o marcador
        def ok(tipo):
            canvas_atual.delete(marcador)
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
    cw.dica('Clique na tela para definir a localização do widget')
    canvas_atual.bind("<Button-1>", click)

def visual_widget(projeto, wid):
    # Encontra o Widget
    nome_aba = projeto.notebook.tab(projeto.notebook.select(), 'text')
    widget = projeto.abas[nome_aba]['widgets'][wid]
    # Cria a janela
    janela = cw.customTopLevel('Configurar Visual', geometry=(450, 400), resizable=(False, False), command=lambda:salvar_widget(), closeWindow=False)

    def escolher_cor(entry_widget):
        cor = AskColor().get()
        if cor is not None:
            entry_widget.configure(fg_color=cor)
            entry_widget.configure(text=cor)
        
    def buscar_imagem(entry_widget):
        caminho_imagem = filedialog.askopenfilename()
        entry_widget.insert(0, caminho_imagem)

    # Cria todos os campos de parâmetros dinamicamente
    for param, value in widget['propriedades'].items():
        # Cria um frame temporário simplesmente pra organizar os campos
        frame_temp = ctk.CTkFrame(janela, fg_color='transparent')
        frame_temp.pack(fill='x', pady=2, padx=2)
        nome = dt.traducoes_parametros[param]
        ctk.CTkLabel(frame_temp, text=f'{nome}:').pack(side='left')

        # Cria as entrys de acordo com a propriedade
        entry = None
        if param in dt.parametros_especiais['cores']:
            cor_botao = value if value not in [None, 'transparent'] else '#000000'
            # Passa 'entry' como argumento no lambda
            entry = ctk.CTkButton(frame_temp, text=str(value), width=200, command=lambda e=entry: escolher_cor(e))
            entry.configure(fg_color=cor_botao)
            
        elif param in dt.parametros_especiais['pre-definidos'].keys():
            entry = ctk.CTkComboBox(frame_temp, values=dt.parametros_especiais['pre-definidos'][param], state='readonly', width=200)
            entry.set(value)
        
        elif param == 'image':
            entry = ctk.CTkEntry(frame_temp, width=170)
            # Passa 'entry' como argumento no lambda
            ctk.CTkButton(frame_temp, text='...', width=25, command=lambda e=entry: buscar_imagem(e)).pack(side='right', padx=(5, 0))
            entry.insert(0, str(value))
        
        else:
            entry = ctk.CTkEntry(frame_temp, width=200)
            entry.insert(0, str(value))
        
        entry.pack(side='right')

    # Função para salvar o widget
    def salvar_widget():
        # Pega a chave e valor
        for frame in janela .winfo_children():
            label_widget = frame.winfo_children()[0]
            entry_widget = frame.winfo_children()[1]
            # Trata os dados
            chave = label_widget.cget('text').replace(':', '')
            param = [k for k, v in dt.traducoes_parametros.items() if v == chave][0]
            valor = entry_widget.get()
            # Atualiza o widget
            projeto.config_widget(wid, param, valor)

def comando(projeto, wid):
    # Encontra o Widget
    nome_aba = projeto.notebook.tab(projeto.notebook.select(), 'text')
    widget = projeto.abas[nome_aba]['widgets'][wid]

    # Cria a janela
    janela = cw.customTopLevel('Configurar Comando', geometry=(300, 400), button_set=True, scrollbar=True, closeWindow=False, resizable=(False, False))

    # Combobox com as funções disponíveis
    ctk.CTkLabel(janela, text='Função:').pack(pady=5)
    combo_comando = ctk.CTkComboBox(janela, values=list(dt.funcoes.keys()), state='readonly', width=200, command=lambda e:atualizar_campos())
    combo_comando.pack(pady=5)

    # Frame para os parâmetros
    frame_parametros = ctk.CTkFrame(janela)
    frame_parametros.pack(side='right', fill='both', expand=True, padx=5, pady=5)
    ctk.CTkLabel(frame_parametros, text='Parâmetros').pack(pady=5, fill='x', anchor='nw')

    # Função para atualizar os parâmetros de acordo com a função selecionada
    def atualizar_campos():
    # Pega o valor do Combobox
        comando = combo_comando.get()
        nome_aba = projeto.notebook.tab(projeto.notebook.select(), 'text')
        projeto.abas[nome_aba]['widgets'][wid]['comando'] = comando
        
        # Limpa todos os widgets antigos do frame de parâmetros
        for child in frame_parametros.winfo_children()[1:]:
            child.destroy()

        # Cria todos os campos de parâmetros dinamicamente
        for param, value in dt.funcoes[comando]['parametros'].items():
            # Cria um frame temporário para organizar os campos
            frame_temp = ctk.CTkFrame(frame_parametros)
            frame_temp.pack(fill='x', pady=2, padx=2)
            frame_temp.configure(fg_color=frame_parametros.cget('fg_color'))
            
            # Cria as entradas de acordo com o parâmetro
            ctk.CTkLabel(frame_temp, text=f'{param}:').pack(side='left')
            entry = None
            if param == 'server':
                servidores = projeto.abas[nome_aba]['servidores'].keys()
                entry = ctk.CTkComboBox(frame_temp, values=list(servidores), state='readonly', width=100)
            else:
                entry = ctk.CTkEntry(frame_temp, width=100)
                entry.insert(0, str(value))
            entry.pack(side='right')
    
    def salvar_comando():
        # Pega a chave e valor
        for frame in janela.winfo_children()[2].winfo_children()[1:]:
            label_widget = frame.winfo_children()[0]
            entry_widget = frame.winfo_children()[1]
            # Trata os dados
            chave = label_widget.cget('text').replace(':', '')
            param = [k for k, v in dt.traducoes_parametros.items() if v == chave][0]
            valor = entry_widget.get()
            # Atualiza o widget
            widget['comando'] = combo_comando.get()