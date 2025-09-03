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

        # Depois de criar o widget, remove o marcador, muda o cursor e chama a janela de configuração
        def ok(tipo):
            canvas_atual.delete(marcador)
            classe = dt.widgets_padrao[tipo]['classe']
            propriedades = dt.widgets_padrao[tipo]['propriedades']
            widget = projeto.add_widget(classe, propriedades, x, y)
            visual_widget(widget)

        # criar o widget:
        context_menu = tk.Menu(canvas_atual,
                               bg=ctk.ThemeManager.theme["CTkButton"]["fg_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme["CTkButton"]["fg_color"][1],
                               fg=ctk.ThemeManager.theme["CTkButton"]["text_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme["CTkButton"]["text_color"][1],
                               activebackground=ctk.ThemeManager.theme["CTkButton"]["hover_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme["CTkButton"]["hover_color"][1],
                               activeforeground=ctk.ThemeManager.theme["CTkButton"]["text_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme["CTkButton"]["text_color"][1],
                               tearoff=0)
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

def visual_widget(widget):
    # Cria a janela
    janela = cw.janelaScroll('Configurar Visual', geometry=(450, 400), resizable=(False, False), buttonName='Aplicar', command=lambda:salvar_widget(), closeWindow=False)

    def escolher_cor(entry_widget):
        cor = AskColor().get()
        if cor is not None:
            entry_widget.configure(fg_color=cor)
            entry_widget.configure(text=cor)
        
    def buscar_imagem(entry_widget):
        caminho_imagem = filedialog.askopenfilename()
        entry_widget.insert(0, caminho_imagem)

    # Cria todos os campos de parâmetros dinamicamente
    for param, value in widget.propriedades.items():
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
            entry = ctk.CTkEntry(frame_temp, width=175)
            # Passa 'entry' como argumento no lambda
            ctk.CTkButton(frame_temp, text='...', width=15, command=lambda e=entry: buscar_imagem(e)).pack(side='right', padx=(5, 0))
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
            widget.propriedades[param] = valor
            widget.config(param,valor)

def funcao(widget):
    # Cria a janela
    janela = cw.janelaScroll('Conexão Modbus', geometry=(400, 400), button_set=False, scrollbar=False, resizable=(False, False))

    # Combobox com as funções disponíveis
    ctk.CTkLabel(janela, text='Função:').pack(pady=5)
    combo_funcao = ctk.CTkComboBox(janela, values=list(dt.funcoes.keys()), state='readonly', width=200)
    combo_funcao.pack(pady=5)
    combo_funcao.bind('<<ComboboxSelected>>', lambda:atualizar_campos())

    # Frame para os parâmetros
    frame_parametros = ctk.CTkFrame(janela)
    frame_parametros.pack(side='right', fill='both', expand=True, padx=5, pady=5)
    ctk.CTkLabel(frame_parametros, text='Parâmetros').pack(pady=5, fill='x', anchor='nw')

    # Função para atualizar os parâmetros de acordo com a função selecionada
    def atualizar_campos():
        # Pega o valor do Combobox
        funcao_selecionada = combo_funcao.get()
        
        # Limpa todos os widgets antigos do frame de parâmetros
        for child in frame_parametros.winfo_children()[1:]:
            child.destroy()

        # Cria todos os campos de parâmetros dinamicamente
        for param, value in dt.funcoes[funcao_selecionada]['parametros'].items():
            # Cria um frame temporário simplesmente pra organizar os campos
            frame_temp = ctk.CTkFrame(frame_parametros)
            frame_temp.pack(fill='x', pady=2, padx=2)
            frame_temp.configure(fg_color=frame_parametros.cget('fg_color'))
            ctk.CTkLabel(frame_temp, text=f'{param}:').pack(side='left')
            
            # Cria as entrys de acordo com o parâmetro
            entry = ctk.CTkEntry(frame_temp, width=100)
            entry.insert(0, str(value))
            entry.pack(side='right')