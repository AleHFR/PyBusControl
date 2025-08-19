import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
import tab_manager as tm
import file_handler as fh
import custom_widgets as cw
import utils as ut
import scada_settings as ss

# Variáveis Locais
widgets_ids = []

########## Funções de menu de contexto do canvas ##########
def menu_contexto_canvas(event, canvas):
    context_menu_canvas = tk.Menu(canvas, tearoff=0)
    context_menu_canvas.add_command(label='Inserir Widget',command=lambda:adicionar_widget(event.x, event.y, canvas))
    context_menu_canvas.add_command(label='Alterar tamanho',command=lambda:tm.alterar_tamanho_canvas(canvas))
    context_menu_canvas.add_command(label='Imagem de fundo',command=lambda:tm.inserir_imagem(canvas))
    context_menu_canvas.post(event.x_root, event.y_root)

def menu_contexto_widget(event, item_id, canvas):
    context_menu = tk.Menu(canvas, tearoff=0)
    context_menu.add_command(label='Mover',command=lambda e=event:mover_widget(item_id, canvas))
    context_menu.add_command(label='Propriedades',command=lambda:propriedades_widget(item_id, canvas))
    context_menu.add_command(label='Personalizar',command=lambda:personalizar_widget(item_id, canvas))
    context_menu.add_command(label='Excluir', command=lambda: excluir(item_id, canvas))

    context_menu.post(event.x_root, event.y_root)

########## Adicionar um widget ##########
def adicionar_widget(x, y, canvas):
    global widgets_ids

    widget = propriedades_widget(canvas)

    # Encontra as caracteristicas do widget
    classe = getattr(ttk, widget['classe'])
    props = widget.get('propriedades', {})
        
    # Cria o widget e insere no canvas
    w = classe(canvas, **props)
    item_id = canvas.create_window(x, y, window=w, anchor='nw')
    widgets_ids.append([classe.__name__,item_id])
    w.bind('<Button-3>', lambda e, i=item_id: menu_contexto_widget(e, i, canvas))

    return item_id

########## Função de propriedades do widget ##########
def propriedades_widget(canvas, widget=None):
    janela = cw.menuPropriedades('Configuração do widget', geometry=(300, 500), resizable=(False, False), command=lambda:criar_widget)
    widget_selecionado = tk.StringVar(value='Botão')

    if widget is None:
        # Frame para o combobox
        frame_selecao = ttk.LabelFrame(janela, text="Selecione o widget:")
        frame_selecao.pack(padx=5, pady=5, fill='x', anchor='w')

        lista_widgets = list(ss.tipos_widgets.keys())
        combo_widgets = ttk.Combobox(frame_selecao, textvariable=widget_selecionado, values=lista_widgets,state='readonly')
        combo_widgets.pack(padx=5)

    frame_propriedades = ttk.LabelFrame(janela, text="Propriedades:")
    frame_propriedades.pack(padx=5, pady=5, fill='both')
    for key, value in ss.tipos_widgets[widget_selecionado.get()]['propriedades'].keys():
        ttk.Label(frame_propriedades, text=key).pack(anchor='w', padx=5)
        ttk.Entry(frame_propriedades, textvariable=value).pack(anchor='w', padx=5)
    
    def atualizar_campos(*args):
        # Limpa campos antigos
        for widget in frame_propriedades.winfo_children():
            widget.destroy()
        # Cria campos
        for w in lista_widgets:
            ttk.Label(frame_propriedades, text=w).pack(side='left', padx=5)
            entry = ttk.Entry(frame_propriedades, width=23)
            entry.pack(side='right', padx=5)

    widget_selecionado.trace_add('write', atualizar_campos)
    atualizar_campos()
    
    def criar_widget():
        """Função chamada ao clicar no botão 'Criar'."""
        nome_escolhido = widget_selecionado.get()
        widget_info = ss.Configuracao.Widgets.tipos_widgets[nome_escolhido]
        
        # Chama a função para adicionar o widget, passando as informações necessárias
        # A posição do widget (100, 100) é um exemplo, pode ser alterada.
        adicionar_widget(100, 100, canvas, widget_info) 
        
        janela.destroy() # Fecha a janela após a criação

########## Função de personalizar a aparencia do widget ##########
def personalizar_widget(item_id, canvas):
    print('em desenvolvimento...')

########## Mover widget ##########
def mover_widget(item_id, canvas):
    canvas._drag_data = {'item': item_id}

    def mover(event):
        canvas.coords(item_id, event.x, event.y)

    def parar(event):
        canvas.unbind('<Motion>')
        canvas.unbind('<Button-1>')
        canvas._drag_data = {}

    canvas.bind('<Motion>', mover)
    canvas.bind('<Button-1>', parar)

########## Excluir widget ##########
def excluir(item_id, canvas):
    # Remove o widget do canvas e da lista de ids
    global widgets_ids
    for tipo, id in widgets_ids:
        if id == item_id:
            widget = canvas.nametowidget(canvas.itemcget(item_id, 'window'))
            widget.destroy()
            canvas.delete(item_id)
            widgets_ids.remove([tipo, id])