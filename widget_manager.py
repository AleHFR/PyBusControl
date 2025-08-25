########### Preâmbulo ###########
# Imports do python
from tkinter import ttk
from tkinter import messagebox

# Imports do projeto
import custom_widgets as cw

# Variáveis Locais
tipos_widgets = {
    'Texto': {
        'classe': 'Label',
        'propriedades': {
            'text': 'Texto',
            'image': '',
        }
    },
    'Botão': {
        'classe': 'Button',
        'função': '',
        'propriedades': {
            'text': 'Botão',
            'width': 10,
            'image': '',
        }
    },
    'Indicador': {
        'classe': 'Label',
        'função': '',
        'propriedades': {
            'text': '0.00',
        }
    },
    'Slider': {
        'classe': 'Scale',
        'função': '',
        'propriedades': {
            'from_': 0,
            'to': 100,
            'orient': 'horizontal',
            'length': 100,
        }
    },
}

canvas_atual = None
########## Adicionar um widget ##########
def adicionar_widget(projeto):
    # Verifica se tem uma aba ativa
    if projeto.notebook == {}:
        messagebox.showerror('Erro','Nenhuma aba existente')
        return
    # Janela para selecionar e configurar o widget
    janela = cw.janelaScroll('Adicionar Widget', resizable=(False, False))
    # Frame pra selecionar o tipo de widget
    frame_tipo = ttk.Frame(janela)
    frame_tipo.pack(padx=5, pady=5, fill='x')
    ttk.Label(frame_tipo, text='Widget:').pack(side='left')
    combo_tipo = ttk.Combobox(frame_tipo, values=list(tipos_widgets.keys()), state='readonly')
    combo_tipo.pack(side='right')
    combo_tipo.bind('<<ComboboxSelected>>', lambda event:atualizar_tipo())

    # Frame pra configurar o widget
    frame_propriedades = ttk.LabelFrame(janela, text='Propriedades')
    frame_propriedades.pack(padx=5, pady=5, fill='both')

    def atualizar_tipo():
        for widget in frame_propriedades.winfo_children():
            widget.destroy()

        for key, value in tipos_widgets[combo_tipo.get()]['propriedades'].items():
            ttk.Label(frame_propriedades, text=key).pack(anchor='w', padx=5, pady=2)
            ttk.Entry(frame_propriedades, textvariable=value).pack(anchor='w', padx=5, pady=2)

    # def canvas_by_tab(tab_name):
    # # pega o frame pelo nome
    # for tab_id in notebook.tabs():
    #     if notebook.tab(tab_id, "text") == tab_name:
    #         frame = notebook.nametowidget(tab_id)
    #         # pega o primeiro canvas dentro desse frame
    #         for child in frame.winfo_children():
    #             if isinstance(child, tk.Canvas):
    #                 return child
    # return None

    # def criar_widget(event):
        
    
def props_modbus(janela=None):
    if not janela:
        janela = cw.janelaScroll('', resizable=(False, False), scrollbar=False)

# ########## Funções de menu de contexto do widget ##########
# def menu_contexto_widget(event, item_id, canvas):
#     context_menu = tk.Menu(canvas, tearoff=0)
#     context_menu.add_command(label='Mover',command=lambda e=event:mover_widget(item_id, canvas))
#     context_menu.add_command(label='Propriedades',command=lambda:propriedades_widget(item_id, canvas))
#     context_menu.add_command(label='Personalizar',command=lambda:personalizar_widget(item_id, canvas))
#     context_menu.add_command(label='Excluir', command=lambda: excluir(item_id, canvas))

#     context_menu.post(event.x_root, event.y_root)

# ########## Função de propriedades do widget ##########
# def propriedades_widget(canvas, widget=None):
#     janela = cw.menuPropriedades('Configuração do widget', geometry=(300, 500), resizable=(False, False), command=lambda:criar_widget)
#     widget_selecionado = tk.StringVar(value='Botão')

#     if widget is None:
#         # Frame para o combobox
#         frame_selecao = ttk.LabelFrame(janela, text="Selecione o widget:")
#         frame_selecao.pack(padx=5, pady=5, fill='x', anchor='w')

#         lista_widgets = list(tipos_widgets.keys())
#         combo_widgets = ttk.Combobox(frame_selecao, textvariable=widget_selecionado, values=lista_widgets,state='readonly')
#         combo_widgets.pack(padx=5)

#     frame_propriedades = ttk.LabelFrame(janela, text="Propriedades:")
#     frame_propriedades.pack(padx=5, pady=5, fill='both')
#     for key, value in tipos_widgets[widget_selecionado.get()]['propriedades'].keys():
#         ttk.Label(frame_propriedades, text=key).pack(anchor='w', padx=5)
#         ttk.Entry(frame_propriedades, textvariable=value).pack(anchor='w', padx=5)
    
#     def atualizar_campos(*args):
#         # Limpa campos antigos
#         for widget in frame_propriedades.winfo_children():
#             widget.destroy()
#         # Cria campos
#         for w in lista_widgets:
#             ttk.Label(frame_propriedades, text=w).pack(side='left', padx=5)
#             entry = ttk.Entry(frame_propriedades, width=23)
#             entry.pack(side='right', padx=5)

#     widget_selecionado.trace_add('write', atualizar_campos)
#     atualizar_campos()
    
#     def criar_widget():
#         nome_escolhido = widget_selecionado.get()
#         widget_info = tipos_widgets[nome_escolhido]
        
#         # Chama a função para adicionar o widget, passando as informações necessárias
#         # A posição do widget (100, 100) é um exemplo, pode ser alterada.
#         adicionar_widget(100, 100, canvas, widget_info) 
        
#         janela.destroy() # Fecha a janela após a criação

# ########## Função de personalizar a aparencia do widget ##########
# def personalizar_widget(item_id, canvas):
#     tk.messagebox.showinfo('', 'Em desenvolvimento...')

# ########## Mover widget ##########
# def mover_widget(item_id, canvas):
#     canvas._drag_data = {'item': item_id}

#     def mover(event):
#         canvas.coords(item_id, event.x, event.y)

#     def parar(event):
#         canvas.unbind('<Motion>')
#         canvas.unbind('<Button-1>')
#         canvas._drag_data = {}

#     canvas.bind('<Motion>', mover)
#     canvas.bind('<Button-1>', parar)

# ########## Excluir widget ##########
# def excluir(item_id, canvas):
#     # Remove o widget do canvas e da lista de ids
#     global widgets_ids
#     for tipo, id in widgets_ids:
#         if id == item_id:
#             widget = canvas.nametowidget(canvas.itemcget(item_id, 'window'))
#             widget.destroy()
#             canvas.delete(item_id)
#             widgets_ids.remove([tipo, id])