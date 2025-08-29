########### Preâmbulo ###########
# Imports do python
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tktooltip import ToolTip

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
    aba_atual = projeto.notebook.nametowidget(projeto.notebook.select())
    canvas_atual = next(
        (child for child in aba_atual.winfo_children() if isinstance(child, tk.Canvas)),
        None
    )
    
    # Habilita o click na tela pra definir onde o widget vai ficar
    def click(event):
        # Muda o cursor pra seta
        canvas_atual.config(cursor="arrow")

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
            wid = projeto.add_widget(classe, propriedades, x, y)
            propriedades_widget(projeto, wid)

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

def propriedades_widget(projeto, wid):
    # Verifica se tem ao menos uma aba aberta
    if not projeto.notebook.tabs():
        messagebox.showerror('Erro', 'Nenhuma aba existente')
        return

    # Cria a janela
    janela = cw.janelaScroll('Configurar Widgets', geometry=(200, 200), resizable=(False, False), scrollbar=False)

    # Pega os widgets existentes
    widgets = projeto.abas[projeto.notebook.tab(projeto.notebook.select(), 'text')].widgets
    # Pega o widget selecionado
    widget_selecionado = widgets.get(wid)

    # Frame para os botões
    frame_serv_bt = ttk.LabelFrame(janela, text="Configuração")
    frame_serv_bt.pack(side='top', fill='x', padx=2, pady=2)
    # Lista com os botões
    btns = {
        'Editar': {'command': lambda: editar_widget(), 'image': 'config.png'},
        'Salvar': {'command': lambda: salvar_widget(), 'image': 'save.png'},
        'Remover': {'command': lambda: remover_widget(), 'image': 'del.png'},
    }
    # Adiciona os botoes ao frame
    for key, value in btns.items():
        imagens[key] = ut.imagem(value['image'], (15, 15))
        bt = ttk.Button(frame_serv_bt, command=value['command'], image=imagens[key])
        if key == 'Remover': # Coloca o botão de remover longe dos demais
            bt.pack(side='right', padx=2, pady=2)
        else:
            bt.pack(side='left', padx=2, pady=2)
        ToolTip(bt, msg=key)

    # Frame para os parâmetros
    frame_propriedades = ttk.LabelFrame(janela, text="Propriedades")
    frame_propriedades.pack(side='bottom', fill='both', expand=True, padx=5, pady=5)

    # Cria todos os campos de parâmetros dinamicamente
    for param, value in widget_selecionado.propriedades.items():
        # Cria um frame temporário simplesmente pra organizar os campos
        frame_temp = ttk.Frame(frame_propriedades)
        frame_temp.pack(fill='x', pady=2, padx=2)
        ttk.Label(frame_temp, text=f'{param}:').pack(side='left')
        # Cria as entrys de acordo com a propriedade
        entry = ttk.Entry(frame_temp, width=20)
        entry.insert(0, value)
        entry.config(state='disabled')
        entry.pack(side='right')

    def salvar_widget():
        # Pega a chave e valor
        for frame in frame_propriedades.winfo_children():
            label_widget = frame.winfo_children()[0]
            entry_widget = frame.winfo_children()[1]
            # Trata os dados
            chave = label_widget.cget('text').replace(':', '')
            valor = entry_widget.get()
            # Atualiza o dicionário no projeto
            projeto.config_widget(wid, chave, valor)
            # Desabilita o campo após salvar
            entry_widget.config(state='disabled')
        projeto.exibir()

    def editar_widget():
        for frame in frame_propriedades.winfo_children():
            widget = frame.winfo_children()[1] # O segundo widget é sempre o de entrada
            if isinstance(widget, ttk.Entry):
                widget.config(state='normal')
            elif isinstance(widget, ttk.Combobox):
                widget.config(state='readonly')

    def remover_widget():
        if messagebox.askyesno('Confirmar', 'Deseja excluir o widget?'):
            projeto.del_widget(wid)