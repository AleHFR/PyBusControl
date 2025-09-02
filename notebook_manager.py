########### Preâmbulo ###########
# Imports do python
from tkinter import ttk
import customtkinter as ctk
from tktooltip import ToolTip
from tkinter import messagebox, filedialog

# Imports do projeto
import custom_widgets as cw
import project_handler as pj
import widget_manager as wm
import server_manager as sm
import utils as ut

imagens = {}

def novo_projeto(root, nome=None):
    # Limpa o root
    for widget in root.winfo_children():
        # Destroi apenas os widgets não necessários
        if widget.winfo_class() not in ['LabelFrame', 'Menu']:
            widget.destroy()
    # Instancia o projeto principal
    projeto = pj.Projeto(root)
    # Cria a barra de edição
    barra_ferramentas = ttk.LabelFrame(root, text='Novo Projeto')
    barra_ferramentas.pack(side='top', anchor='nw', fill='x', padx=2, pady=2)
    # Botões da aba
    itens = {
        'Nova Aba': {
            'command': lambda:add_aba(projeto),
            'icone': 'nova_aba.png',
        },
        'Configurar Aba': {
            'command': lambda:config_aba(projeto),
            'icone': 'config.png',
        },
        'Deletar Aba': {
            'command': lambda:del_aba(projeto),
            'icone': 'del.png',
        },
        'Configurar Servidores': {
            'command': lambda:sm.configurar_servidores(projeto),
            'icone': 'servidor.png',
        },
        'Conectar Servidores':{
            'command': lambda:sm.conectar_servidores(projeto),
            'icone': 'conectar.png',
        },
        'Adicionar Widget': {
            'command': lambda:wm.adicionar_widget(projeto),
            'icone': 'widget.png',
        },
        'Tela Cheia':{
            'command': lambda:ut.tela_cheia(),
            'icone': 'tela_cheia.png',
        },
    }
    # Cria os botões
    for nome_botao, cfg in itens.items():
        imagens[nome_botao] = ut.imagem(cfg['icone'], (15, 15))
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

    # Cria um texto de suporte
    ctk.CTkLabel(barra_ferramentas, text='Nenhuma Atividade').pack(side='right', padx=5)

    # Adiciona umas coias para testes
    projeto.add_servidor('Esp32', 'TCP', {'IP': '127.168.0.3', 'Porta': 1502, 'Timeout (s)': 1})
    projeto.add_servidor('ArdUNO', 'RTU', {'Porta Serial': 'COM1', 'Baudrate': '9600', 'Paridade': 'N', 'Bytesize': 8, 'Stopbits': 1, 'Timeout (s)': 1})

def add_aba(projeto):
    nome = ctk.CTkInputDialog(text='Nova Aba:', title='Insira o nome da aba').get_input()
    if nome != '' and nome not in projeto.abas.keys():
        projeto.add_aba(nome)

def config_aba(projeto):
    # Verifica se tem ao menos uma aba aberta
    if not projeto.notebook.tabs():
        messagebox.showerror('Erro', 'Nenhuma aba existente')
        return

    # Cria a janela
    janela = cw.janelaScroll('Configurar Aba', geometry=(300, 300), buttonName='Aplicar', closeWindow=False, command=lambda: aplicar())
    
    # Encontra a aba atual
    aba = projeto.find('aba')

    # Cria todos os campos de parâmetros dinamicamente
    # junta dois dicionarios
    params = {'nome': projeto.find('nome_aba'),**aba.__dict__}
    for param, value in params.items():
        # Ignora os parâmetros desnecessários
        if param in ['notebook', 'idx', 'canvas', 'widgets']: continue
        # Cria um frame temporário simplesmente pra organizar os campos
        frame_temp = ctk.CTkFrame(janela)
        frame_temp.pack(fill='x', pady=2, padx=2)
        ctk.CTkLabel(frame_temp, text=f'{param}:').pack(side='left')
        # Cria as entrys de acordo com a propriedade
        entry = None
        if param == 'imagem': # Pra imagem cria um botão de busca
            entry = ctk.CTkEntry(frame_temp, width=116)
            ctk.CTkButton(frame_temp, text='...', width=30, command=lambda:buscar()
                          ).pack(side='right', padx=2, pady=2)
            def buscar():
                caminho_imagem = filedialog.askopenfilename()
                entry.insert(0, caminho_imagem)
        elif param == 'tamanho': # Para o tamanho cria um campo de entrada personalizado
            entry = ctk.CTkEntry(frame_temp, width=150)
            entry.insert(0, f'{value[0]}x{value[1]}')
        else: # Para outros parâmetros cria um campo de entrada padrão 
            entry = ctk.CTkEntry(frame_temp, width=150)
            entry.insert(0, value)
        entry.pack(side='right')

    def aplicar():
        # Pega a chave e valor
        for frame in janela.winfo_children():
            # Pega a chave e valor
            label_aba = frame.winfo_children()[0]
            entry_aba = frame.winfo_children()[1]
            chave = label_aba.cget('text').replace(':', '')
            valor = entry_aba.get()
            # Trata os dados
            if chave == 'tamanho':
                x, y = valor.split('x')
                projeto.config_aba(aba, chave, (int(x), int(y)))
            else:
                projeto.config_aba(aba, chave, valor)

def del_aba(projeto):
    # Verifica se há abas existentes
    if not projeto.notebook.tabs():
        messagebox.showerror('Erro', 'Nenhuma aba existente')
        return
    # Encontra a aba atual e a exclui
    aba = projeto.find('aba')
    projeto.del_aba(aba)