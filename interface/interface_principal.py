########### Preâmbulo ###########
# Imports do python
import customtkinter as ctk
from TkToolTip import ToolTip
from tkinter import messagebox, filedialog
import json

# Imports do projeto
import interface.customizados as ct
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
    projeto.add_servidor('Esp32_1', 'TCP', {'ID':1, 'IP': '10.83.206.64', 'Porta': 1502, 'Timeout (s)': 1})
    projeto.add_servidor('Esp32_2', 'TCP', {'ID':2, 'IP': '192.168.0.201', 'Porta': 1502, 'Timeout (s)': 1})

    # Cria a barra de edição
    barra_ferramentas = ct.customLabelFrame(root, text='Novo Projeto')
    barra_ferramentas.pack(side='top', anchor='nw', fill='x', padx=2, pady=2)
    
    itens = { # Botões da aba
        'Nova Aba':{'command': lambda:add_aba(projeto),'icone': 'nova_aba.png',},
        'Configurar Aba':{'command': lambda:config_aba(projeto),'icone': 'config.png',},
        'Configurar Servidores':{'command': lambda:sm.configurar_servidores(projeto),'icone': 'servidor.png',},
        'Conectar Servidores':{'command': lambda:sm.conectar_servidores(projeto),'icone': 'conectar.png',},
        'Adicionar Widget':{'command': lambda:wm.adicionar_widget(projeto),'icone': 'widget.png',},
        'Exibir':{'command': lambda:projeto.exibir(),'icone': 'save.png',}
    }
    
    for nome_botao, cfg in itens.items(): # Cria os botões
        imagens[nome_botao] = ct.imagem(cfg['icone'], (15, 15)) # Chama a imagem no formato compatível
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
        ToolTip(bt, msg=nome_botao, delay=0.5) # Cria uma tooltip com

def abrir_projeto(root):
    caminho_projeto = filedialog.askopenfilename()
    if caminho_projeto != '':
        # Lê o arquivo json
        with open(caminho_projeto, 'r') as f:
            arquivos_projeto = json.load(f)
        print(arquivos_projeto)

def add_aba(projeto): # Adiciona uma aba ao projeto
    # Pergunta um nome pra aba
    nome = ctk.CTkInputDialog(text='Nova Aba:', title='Insira o nome da aba').get_input()
    if nome != '' and nome not in projeto.abas.keys(): # Verifica se o nome já existe ou não é um texto vazio
        if nome is not None:
            projeto.add_aba(nome)
    else:
        messagebox.showwarning('Erro', 'Nome de aba inválido')

def config_aba(projeto): # Altera as configurações da aba atual
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
            elif chave == 'imagem':
                imagem = item.get()
                projeto.config_aba(chave, imagem)
            else:
                projeto.config_aba(chave, valor)
    def del_aba():
        # Verifica se há abas existentes
        if not projeto.abas.keys():
            messagebox.showerror('Erro', 'Nenhuma aba existente')
            return
        # Exclui a aba de fato
        pergunta = ct.customDialog('Excluir aba', f'Deseja excluir a aba "{nome}"?')
        if pergunta.result:
            projeto.del_aba()
            janela.destroy()

    # Cria a janela
    janela = ct.customTopLevel('Configurar Aba', geometry=(300, 300), buttonName='Aplicar', command=aplicar)
    # Botão para deletar a aba
    ctk.CTkButton(janela.frame_interno, text='Deletar', command=del_aba).pack(side='bottom', pady=5, padx=5)
    
    # Encontra a aba atual
    frame = projeto.notebook.select()
    nome = projeto.notebook.tab(frame, 'text')
    aba = projeto.abas[nome]

    # Cria todos os campos de parâmetros dinamicamente
    params = {'nome': nome, 'tamanho': aba.tamanho, 'imagem': aba.caminho_imagem}
    for param, value in params.items():
        # Cria as entrys de acordo com a propriedade
        if param == 'imagem': # Pra imagem cria um botão de busca
            btentry = ct.customBuscaArquivo(root=janela.frame_interno, valor_inicial=value, tamanho=150)
            janela.addItem(nome=param, tamanho=150, item=btentry)
        elif param == 'tamanho': # Para o tamanho cria um campo de entrada personalizado
            janela.addItem(nome=param, tamanho=150, item=ctk.CTkEntry, valor_inicial=f'{value[0]}x{value[1]}')
        else: # Para outros parâmetros cria um campo de entrada padrão 
            janela.addItem(nome=param, tamanho=150, item=ctk.CTkEntry, valor_inicial=value)

def tela_cheia(root): # Coloca e tira da tela cheia
    global widgets_originais # Chama uma variável global de auxílio
    is_fullscreen = root.attributes('-fullscreen')

    if not is_fullscreen: # Oculta todos os widgets existentes
        for widget in root.winfo_children():
            if widget.winfo_class() in ['Menu','TLabelframe']: # Lista com os widgets que deverão ser ocultados
                widgets_originais.append(widget) # Salva os widgets
                widget.pack_forget()

        root.attributes('-fullscreen', True)
        root.bind('<Escape>', lambda e: tela_cheia(root))
    else: # Volta a exibir os widgets
        for widget in widgets_originais: # Restaura os widgets de acordo com seu tipo
            if widget.winfo_class() == 'Menu':
                root.config(menu=widget)
            elif widget.winfo_class() == 'TLabelframe':
                widget.pack(side='top', anchor='nw', fill='x', padx=2, pady=2)
        
        # limpa a lista e tira o bind do esc
        widgets_originais = []
        root.attributes('-fullscreen', False)
        root.unbind('<Escape>')

def salvar_projeto(projeto):
    caminho_projeto = filedialog.askopenfilename()
    if caminho_projeto != '':
        # Cria um arquivo.json pra salvar o projeto
        with open(caminho_projeto, 'w') as f:
            json.dump(projeto.toDict(), f)

# Arrumar
def preferencias():
    janela = ct.customTopLevel('Preferências', geometry=(300, 200), resizable=(False, False), buttonSet='Salvar')
    modos = ['Light', 'Dark', 'System']
    janela.addItem('Modo de Aparência', item=ctk.CTkComboBox, value=ctk.get_appearance_mode(), values=modos, width=200)