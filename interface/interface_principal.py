########### Preâmbulo ###########
# Imports do python
import customtkinter as ctk
from tktooltip import ToolTip
from tkinter import messagebox, filedialog

# Imports do projeto
import interface.personalized as ps
import managers.project_manager as pj
import managers.widget_manager as wm
import managers.server_manager as sm

imagens = {}
widgets_originais = []

def novo_projeto(root):
    # Limpa o root
    for widget in root.winfo_children():
        # Destroi apenas os widgets não necessários
        if widget.winfo_class() not in ['LabelFrame', 'Menu']:
            widget.destroy()
    # Instancia o projeto principal
    projeto = pj.Projeto(root)
    # Adiciona dois server de testes
    projeto.add_servidor('Esp32_1', 'TCP', {'ID':1, 'IP': '192.168.0.200', 'Porta': 1502, 'Timeout (s)': 1})
    projeto.add_servidor('Esp32_2', 'TCP', {'ID':2, 'IP': '192.168.0.201', 'Porta': 1502, 'Timeout (s)': 1})
    # Cria a barra de edição
    barra_ferramentas = ps.customLabelFrame(root, text='Novo Projeto')
    barra_ferramentas.pack(side='top', anchor='nw', fill='x', padx=2, pady=2)
    # Botões da aba
    itens = {
        'Nova Aba':{'command': lambda:add_aba(projeto),'icone': 'nova_aba.png',},
        'Configurar Aba':{'command': lambda:config_aba(projeto),'icone': 'config.png',},
        'Configurar Servidores':{'command': lambda:sm.configurar_servidores(projeto),'icone': 'servidor.png',},
        'Conectar Servidores':{'command': lambda:sm.conectar_servidores(projeto),'icone': 'conectar.png',},
        'Adicionar Widget':{'command': lambda:wm.adicionar_widget(projeto),'icone': 'widget.png',},
        'Tela Cheia':{'command': lambda:tela_cheia(root),'icone': 'tela_cheia.png',},
        'Exibir':{'command': lambda:projeto.exibir(),'icone': 'save.png',}
    }
    # Cria os botões
    for nome_botao, cfg in itens.items():
        imagens[nome_botao] = ps.imagem(cfg['icone'], (15, 15))
        bt = ctk.CTkButton(
            barra_ferramentas,
            text='',
            width=0,
            fg_color='#FFFFFF',
            hover_color='gray',
            command=cfg['command'],
            image=imagens[nome_botao],
        )
        bt.pack(side='left', padx=1, pady=2)
        ToolTip(bt, msg=nome_botao)

def add_aba(projeto):
    nome = ctk.CTkInputDialog(text='Nova Aba:', title='Insira o nome da aba').get_input()
    if nome != '' and nome not in projeto.abas.keys():
        projeto.add_aba(nome)

def config_aba(projeto):
    # Verifica se tem ao menos uma aba aberta
    if not projeto.abas.keys():
        messagebox.showerror('Erro', 'Nenhuma aba existente')
        return
    
    # Funções auxiliares
    def aplicar():
        # Pega a chave e valor
        for chave, item in janela.itens.items():
            # Trata os dados
            valor = item.get()
            if chave == 'tamanho':
                x, y = valor.split('x')
                projeto.config_aba(chave, (int(x), int(y)))
            else:
                projeto.config_aba(chave, valor)

    def del_aba():
        # Verifica se há abas existentes
        if not projeto.abas.keys():
            messagebox.showerror('Erro', 'Nenhuma aba existente')
            return
        # Exclui a aba de fato
        if ps.customDialog('Excluir aba', f'Deseja excluir a aba "{nome}"?'):
            projeto.del_aba()
            janela.destroy()

    # Cria a janela
    janela = ps.customTopLevel('Configurar Aba', geometry=(300, 300), buttonName='Aplicar', command=lambda: aplicar())
    # Botão para deletar a aba
    ctk.CTkButton(janela.frame_interno, text='Deletar', command=lambda:del_aba()).pack(fill='y', side='bottom', pady=5, padx=5)
    
    # Encontra a aba atual
    frame = projeto.notebook.select()
    nome = projeto.notebook.tab(frame, 'text')
    aba = projeto.abas[nome]

    # Cria todos os campos de parâmetros dinamicamente
    params = {'nome': nome, 'tamanho': aba.tamanho, 'imagem': aba.caminho_imagem}
    for param, value in params.items():
        # Cria as entrys de acordo com a propriedade
        if param == 'imagem': # Pra imagem cria um botão de busca
            entry = None
            def buscar(entry):
                caminho_imagem = filedialog.askopenfilename()
                entry.delete(0, ctk.END)
                entry.insert(0, caminho_imagem)
            entry = janela.addButtonItem(nome=param, tamanho=150, valor_inicial=value, comando=lambda: buscar(entry))
        elif param == 'tamanho': # Para o tamanho cria um campo de entrada personalizado
            janela.addItem(nome=param, tamanho=150, item=ctk.CTkEntry, valor_inicial=f'{value[0]}x{value[1]}')
        else: # Para outros parâmetros cria um campo de entrada padrão 
            janela.addItem(nome=param, tamanho=150, item=ctk.CTkEntry, valor_inicial=value)

def tela_cheia(root):
    global widgets_originais
    is_fullscreen = root.attributes('-fullscreen')

    if not is_fullscreen:
        # Oculta todos os widgets existentes
        for widget in root.winfo_children():
            if widget.winfo_class() in ['Menu','TLabelframe']:
                widgets_originais.append(widget)
                widget.pack_forget()

        root.attributes('-fullscreen', True)
        root.bind('<Escape>', lambda e: tela_cheia(root))
    else:
        for widget in widgets_originais:
            if widget.winfo_class() == 'Menu':
                root.config(menu=widget)
            elif widget.winfo_class() == 'TLabelframe':
                widget.pack(side='top', anchor='nw', fill='x', padx=2, pady=2)
            
        widgets_originais = []
        root.attributes('-fullscreen', False)
        root.unbind('<Escape>')

# Arrumar
def preferencias():
    janela = ps.customTopLevel('Preferências', geometry=(300, 200), resizable=(False, False), buttonSet='Salvar')
    modos = ['Light', 'Dark', 'System']
    janela.addItem('Modo de Aparência', item=ctk.CTkComboBox, value=ctk.get_appearance_mode(), values=modos, width=200)