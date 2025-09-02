########### Preâmbulo ###########
# Imports do python
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
from tktooltip import ToolTip
from tkinter import filedialog

# Imports do projeto
import custom_widgets as cw
import utils as ut

# Dicionário para salvar os icones das imagens
imagens = {}

#################### Adicionar um widget ####################
def adicionar_widget(projeto):
    # Verifica se tem ao menos uma aba aberta
    if not projeto.notebook.tabs():
        messagebox.showerror('Erro', 'Nenhuma aba existente')
        return

    # Procura a aba e o canvas
    canvas_atual = projeto.find('canvas')
    
    # Habilita o click na tela pra definir onde o widget vai ficar
    def click(event):
        # Muda o cursor pra seta
        canvas_atual.config(cursor="arrow")
        ut.dica() # Reseta a dica
        # salva posição
        x, y = event.x, event.y
        # cria marcador
        r = 5
        marcador = canvas_atual.create_oval(x-r, y-r, x+r, y+r, outline="red", width=2)

        # Depois de criar o widget, remove o marcador, muda o cursor e chama a janela de configuração
        def ok():
            canvas_atual.delete(marcador)
            classe = ut.widgets_padrao[combobox_classe.get()]['classe']
            propriedades = ut.widgets_padrao[combobox_classe.get()]['propriedades']
            widget = projeto.add_widget(classe, propriedades, x, y)
            propriedades_widget(widget)

        # criar o widget:
        janela = cw.janelaScroll('Adicionar widget', geometry=(150, 100), resizable=(False, False), command=lambda:ok())
        ttk.Label(janela, text='Selecione a classe do widget').pack(pady=5)
        combobox_classe = ttk.Combobox(janela, values=list(ut.widgets_padrao.keys()), width=17, state='readonly')
        combobox_classe.pack(pady=5)
        combobox_classe.current(0) # Seleciona a primeira opção por padrão
        # Desabilita o bind
        canvas_atual.unbind("<Button-1>")
        
    # Muda o cursor pra cruz
    canvas_atual.config(cursor="tcross")
    # Chama o bind e escreve a dica
    ut.dica('Clique na tela para definir a localização do widget')
    canvas_atual.bind("<Button-1>", click)

def propriedades_widget(widget):
    # Cria a janela
    janela = cw.janelaScroll('Configurar Widgets', geometry=(220, 220), resizable=(False, False), scrollbar=False)
    # Frame para os botões
    frame_serv_bt = ttk.LabelFrame(janela, text="Configuração")
    frame_serv_bt.pack(side='top', fill='x', padx=2, pady=2)
    # Lista com os botões
    btns = {
        'Editar': {'command': lambda: editar_widget(), 'image': 'config.png'},
        'Salvar': {'command': lambda: salvar_widget(), 'image': 'save.png'},
    }
    # Adiciona os botoes ao frame
    for key, value in btns.items():
        imagens[key] = ut.imagem(value['image'], (15, 15))
        bt = ttk.Button(frame_serv_bt, command=value['command'], image=imagens[key])
        bt.pack(side='left', padx=2, pady=2)
        ToolTip(bt, msg=key)

    # Frame para os parâmetros
    frame_propriedades = ttk.LabelFrame(janela, text="Propriedades")
    frame_propriedades.pack(side='bottom', fill='both', expand=True, padx=5, pady=5)

    # Cria todos os campos de parâmetros dinamicamente
    for param, value in widget.propriedades.items():
        # Cria um frame temporário simplesmente pra organizar os campos
        frame_temp = ttk.Frame(frame_propriedades)
        frame_temp.pack(fill='x', pady=2, padx=2)
        ctk.CTkLabel(frame_temp, text=f'{param}:').pack(side='left')
        # Cria as entrys de acordo com a propriedade
        entry = None
        if param == 'image': # Pra imagem cria um botão de busca
            entry = ctk.CTkEntry(frame_temp, width=16)
            ctk.CTkButton(frame_temp, text='...', width=2, state='disabled', command=lambda:buscar()).pack(side='right', padx=2, pady=2)
            def buscar():
                caminho_imagem = filedialog.askopenfilename()
                entry.insert(0, caminho_imagem)
        else:
            entry = ctk.CTkEntry(frame_temp, width=200)
            entry.insert(0, value)
        entry.configure(state='disabled')
        entry.pack(side='right')

    # Função para editar o widget
    def editar_widget():
        # Procura os campos
        for frame in frame_propriedades.winfo_children():
            entry = frame.winfo_children()[1] # O segundo entry é sempre o de entrada
            if isinstance(entry, ttk.Entry):
                entry.config(state='normal')
                # Se o frame tiver um botão de busca, habilita ele
                if len(frame.winfo_children()) > 2:
                    frame.winfo_children()[2].config(state='normal')

    # Função para salvar o widget
    def salvar_widget():
        # Pega a chave e valor
        for frame in frame_propriedades.winfo_children():
            label_widget = frame.winfo_children()[0]
            entry_widget = frame.winfo_children()[1]
            # Trata os dados
            chave = label_widget.cget('text').replace(':', '')
            valor = entry_widget.get()
            # Atualiza o widget
            widget.propriedades[chave] = valor
            widget.config(chave,valor)
            # Desabilita o campo após salvar
            entry_widget.config(state='disabled')