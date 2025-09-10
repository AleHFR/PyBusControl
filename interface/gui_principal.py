########### Preâmbulo ###########
# Imports do python
import customtkinter as ctk
from tktooltip import ToolTip
from tkinter import messagebox, filedialog

# Imports do projeto
import PyBusControl.interface.personalized as cw
import handlers.project_handler as pj
import managers.widget_manager as wm
import managers.server_manager as sm

imagens = {}

def novo_projeto(root):
    # Limpa o root
    for widget in root.winfo_children():
        # Destroi apenas os widgets não necessários
        if widget.winfo_class() not in ['LabelFrame', 'Menu']:
            widget.destroy()
    # Instancia o projeto principal
    projeto = pj.Projeto(root)
    # Cria a barra de edição
    barra_ferramentas = cw.customLabelFrame(root, text='Novo Projeto')
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
            'command': lambda:tela_cheia(root),
            'icone': 'tela_cheia.png',
        },
        'Exibir':{
            'command': lambda:projeto.exibir(),
            'icone': 'save.png',
        }
    }
    # Cria os botões
    for nome_botao, cfg in itens.items():
        imagens[nome_botao] = cw.imagem(cfg['icone'], (15, 15))
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

    # Adiciona um server de testes
    projeto.add_servidor('Esp32', 'TCP', {'ID':1, 'IP': '192.168.0.200', 'Porta': 1502, 'Timeout (s)': 1})

def add_aba(projeto):
    nome = ctk.CTkInputDialog(text='Nova Aba:', title='Insira o nome da aba').get_input()
    if nome != '' and nome not in projeto.abas.keys():
        projeto.add_aba(nome)

def config_aba(projeto):
    # Verifica se tem ao menos uma aba aberta
    if not projeto.abas.keys():
        messagebox.showerror('Erro', 'Nenhuma aba existente')
        return

    # Cria a janela
    janela = cw.customTopLevel('Configurar Aba', geometry=(300, 300), buttonName='Aplicar', command=lambda: aplicar())
    
    # Encontra a aba atual
    aba = projeto.notebook.select()
    nome = projeto.notebook.tab(aba, 'text')

    # Cria todos os campos de parâmetros dinamicamente
    params = {'nome': nome, 'tamanho': projeto.abas[nome]['tamanho'], 'imagem': projeto.abas[nome]['imagem']}
    for param, value in params.items():
        # Cria um frame temporário simplesmente pra organizar os campos
        frame_temp = ctk.CTkFrame(janela.frame_interno)
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
                entry.delete(0, ctk.END)
                entry.insert(0, caminho_imagem)
        elif param == 'tamanho': # Para o tamanho cria um campo de entrada personalizado
            entry = ctk.CTkEntry(frame_temp, width=150)
            entry.insert(0, f'{value[0]}x{value[1]}')
        else: # Para outros parâmetros cria um campo de entrada padrão 
            entry = ctk.CTkEntry(frame_temp, width=150)
            entry.insert(0, value)
        entry.pack(side='right')
    # Botão para deletar a aba
    ctk.CTkButton(janela.frame_interno, text='Deletar', command=lambda:del_aba()).pack(side='bottom', pady=5, padx=5)

    def aplicar():
        # Pega a chave e valor
        for frame in janela.frame_interno.winfo_children():
            # Pega a chave e valor
            label_aba = frame.winfo_children()[0]
            entry_aba = frame.winfo_children()[1]
            chave = label_aba.cget('text').replace(':', '')
            valor = entry_aba.get()
            # Trata os dados
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
        if cw.customDialog('Excluir aba', f'Deseja excluir a aba "{nome}"?'):
            projeto.del_aba()
            janela.destroy()

def tela_cheia(root):
    is_fullscreen = root.attributes('-fullscreen')
    root.attributes('-fullscreen', not is_fullscreen)
    # Adiciona ou remove o binding do ESC quando entra/sai do modo tela cheia
    if not is_fullscreen:
        root.bind('<Escape>', lambda e: tela_cheia(root))
    else:
        root.unbind('<Escape>')

# Arrumar
def preferencias():
    janela = cw.customTopLevel('Preferências', geometry=(300, 200), resizable=(False, False), buttonSet='Salvar', command=lambda: salvar())
    frame_modo = ctk.CTkFrame(janela.frame_interno)
    frame_modo.pack(pady=2, padx=2, fill="x")

    ctk.CTkLabel(frame_modo, text='Modo de Aparência:').pack(padx=10, pady=5, side='left')
    modos = ['Light', 'Dark', 'System']
    modo_sel = ctk.CTkComboBox(frame_modo, values=modos, state='readonly', width=120)
    modo_sel.pack(padx=10, pady=5, side='right')
    modo_sel.set(ctk.get_appearance_mode()) # Pega o modo atual e define no ComboBox