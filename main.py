########### Preâmbulo ###########
# Imports do python
import platform
import customtkinter as ctk
from tkinter import messagebox

# Imports do projeto
import customizados as ct
import managers.project_manager as pm
import managers.widget_manager as wm
import managers.server_manager as sm
import managers.file_manager as fm
########## Janela principal ##########
root = ctk.CTk()
root.title("PyBusControl")
ctk.set_appearance_mode("light")

########## Configura conforme o sistema operacional ##########
def maximizar_janela():
    system = platform.system()
    if system == "Windows":
        root.state("zoomed")
    else: # Funciona pra Linux e macOS
        root.attributes("-zoomed", True)

imagens = {}
widgets_originais = []

# Cria um notebook pra conter as abas de projeto e home e etc
notebook = ct.customNotebook(root)
notebook.pack(side="bottom", fill="both", expand=True)

def novo_projeto():
    # Pergunta o nome do projeto
    dialog = ct.customDialog("Novo Projeto", "Escolha um nome para o projeto", "entry")

    # Cria a aba do projeto
    root_projeto = ctk.CTkFrame(notebook, fg_color="transparent")
    root_projeto.pack(fill="x", expand=True)
    notebook.add(root_projeto, text=dialog.result)
    notebook.select(root_projeto) 

    # Abre um projeto
    projeto = pm.Projeto(root_projeto)

    # Cria a barra horizontal principal
    barra_principal = ctk.CTkFrame(root_projeto, fg_color="transparent")
    barra_principal.pack(side="top", anchor="nw", fill="x", padx=2, pady=2)

    # Cria frame para os botões de arquivo
    barra_arquivo = ct.customLabelFrame(barra_principal, text="Arquivo")
    barra_arquivo.pack(side="left", padx=2, pady=2)
    itens_arquivo = {
        "Salvar": {"command": lambda: fm.salvar_projeto(projeto), "icone": "save.png"},
        "Tela Cheia": {"command": lambda: tela_cheia(root_projeto), "icone": "tela_cheia.png"},
        "Fechar": {"command": lambda: fechar(projeto), "icone": "cancel.png"},
    }
    for nome_botao, cfg in itens_arquivo.items():
        ct.customIconButton(root=barra_arquivo, icone=cfg["icone"], tooltip=nome_botao, command=cfg["command"]).pack(side="left", padx=2, pady=5)

    # Cria frame para os botões de ferramentas
    barra_ferramentas = ct.customLabelFrame(barra_principal, text="Ferramentas")
    barra_ferramentas.pack(side="left", padx=10, pady=2)
    itens_ferramentas = {
        "Nova Aba": {"command": lambda: add_aba(projeto), "icone": "nova_aba.png"},
        "Configurar Aba": {"command": lambda: config_aba(projeto), "icone": "config.png"},
        "Configurar Servidores": {"command": lambda: sm.configurar_servidores(projeto), "icone": "servidores.png"},
        "Conectar Servidores": {"command": lambda: sm.conectar_servidores(projeto), "icone": "conectar.png"},
        "Adicionar Widget": {"command": lambda: wm.adicionar_widget(projeto), "icone": "widget.png"},
    }
    for nome_botao, cfg in itens_ferramentas.items():
        ct.customIconButton(root=barra_ferramentas, icone=cfg["icone"], tooltip=nome_botao, command=cfg["command"]).pack(side="left", padx=2, pady=5)

    projeto.add_aba("Nova_Aba_0")

def carregar_projeto(notebook):
    fm.carregar_projeto(notebook)
# Arrumar
def tela_cheia(root_projeto): # Coloca e tira da tela cheia
    global widgets_originais # Chama uma variável global de auxílio
    is_fullscreen = root_projeto.attributes("-fullscreen")

    if not is_fullscreen: # Oculta todos os widgets existentes
        for widget in root_projeto.winfo_children():
            if widget.winfo_class() in ["Menu","TLabelframe","CTkFrame"]: # Lista com os widgets que deverão ser ocultados
                widgets_originais.append(widget) # Salva os widgets
                widget.pack_forget()

        root_projeto.attributes("-fullscreen", True)
        root_projeto.bind("<Escape>", lambda e: tela_cheia(root_projeto))
    else: # Volta a exibir os widgets
        for widget in widgets_originais: # Restaura os widgets de acordo com seu tipo
            if widget.winfo_class() == "Menu":
                root_projeto.config(menu=widget)
            elif widget.winfo_class() == "TLabelframe" or widget.winfo_class() == "CTkFrame":
                widget.pack(side="top", anchor="nw", fill="x", padx=2, pady=2)
        
        # limpa a lista e tira o bind do esc
        widgets_originais = []
        root_projeto.attributes("-fullscreen", False)
        root_projeto.unbind("<Escape>")

def fechar(projeto): # Fecha o projeto
    dialog = ct.customDialog("Fechar Projeto", "Deseja fechar o projeto?", "yes_no")
    if dialog.result:
        frame = notebook.select()
        notebook.forget(frame)
        del projeto
    else: None

def add_aba(projeto): # Adiciona uma aba ao projeto
    qtd_abas = len(projeto.abas)
    nome = f"Nova_Aba_{qtd_abas}"
    if nome in projeto.abas.keys() and qtd_abas > 0:
        nome = f"Nova_Aba_{qtd_abas+1}"
    projeto.add_aba(nome)

def config_aba(projeto): # Altera as configurações da aba atual
    # Verifica se tem ao menos uma aba aberta
    if not projeto.abas.keys():
        messagebox.showerror("Erro", "Nenhuma aba existente")
        return
    
    # Funções auxiliares
    def aplicar():
        # Pega a chave e valor
        for chave, item in janela.itens.items():
            if chave == "Tamanho":
                x, y = item[0].get(), item[1].get()
                projeto.config_aba(chave.lower(), (int(x), int(y)))
            else:
                valor = item.get()
                projeto.config_aba(chave.lower(), valor)

    def del_aba():
        # Verifica se há abas existentes
        if not projeto.abas.keys():
            messagebox.showerror("Erro", "Nenhuma aba existente")
            return
        # Exclui a aba de fato
        pergunta = ct.customDialog("Excluir aba", f"Deseja excluir a aba '{nome}'?")
        if pergunta.result:
            projeto.del_aba()
            janela.destroy()

    # Cria a janela
    janela = ct.customTopLevel("Configurar Aba", geometry=(330, 300), resizable=(False, False), scrollbar=False, buttonName="Aplicar", command=aplicar)
    # Botão para deletar a aba
    ctk.CTkButton(janela.frame_botao, text="Deletar", command=del_aba).pack(side="left", padx=5)
    
    # Encontra a aba atual
    frame = projeto.root_projeto.select()
    nome = projeto.root_projeto.tab(frame, "text")
    aba = projeto.abas[nome]

    # Cria todos os campos de parâmetros dinamicamente
    params = {"Nome": nome, "Tamanho": aba.tamanho, "Imagem": aba.caminho_imagem}
    for param, value in params.items():
        # Cria as entrys de acordo com a propriedade
        if param == "Imagem": # Pra imagem cria um botão de busca
            janela.addItem(nome=param, item=ct.customBuscaArquivo, valor_inicial=value, tamanho=140)
        elif param == "Tamanho": # Para o tamanho cria um campo de entrada personalizado
            janela.addTupleItem(nome=param, item_1=ctk.CTkEntry, item_2=ctk.CTkEntry, valor_inicial_1=value[0], valor_inicial_2=value[1], tamanho=170)
        else: # Para outros parâmetros cria um campo de entrada padrão 
            janela.addItem(nome=param, item=ctk.CTkEntry, valor_inicial=value, tamanho=170)
# Arrumar
def preferencias():
    janela = ct.customTopLevel("Preferências", geometry=(300, 200), resizable=(False, False), buttonSet="Salvar")
    modos = ["Light", "Dark", "System"]
    janela.addItem("Modo de Aparência", item=ctk.CTkComboBox, value=ctk.get_appearance_mode(), values=modos, width=200)

# Adiciona a aba de home
home = ctk.CTkFrame(notebook, fg_color="transparent")
notebook.add(home, text="Home")

ctk.CTkLabel(home, text="Bem vindo ao PyBusControl", font=("Arial", 20)).pack(padx=10, pady=10)

frame_central = ctk.CTkFrame(home, fg_color="transparent")
frame_central.pack(pady=10)

frame_bt = ctk.CTkFrame(frame_central, fg_color="transparent")
frame_bt.pack(side="left", fill="both", expand=True)
ctk.CTkButton(frame_bt, text="Novo Projeto", command=novo_projeto).pack(padx=10, pady=10)
ctk.CTkButton(frame_bt, text="Carregar Projeto", command=lambda:carregar_projeto(notebook)).pack(padx=10, pady=10)
ctk.CTkLabel(frame_bt, text=" ").pack(fill="both", expand=True)
ctk.CTkButton(frame_bt, text="Preferências", command=preferencias).pack(padx=10, pady=10)

frame_recentes = ct.customLabelFrame(frame_central, text="Recentes")
frame_recentes.pack(side="left", fill="both", expand=True)
ctk.CTkTextbox(frame_recentes, width=200, height=200).pack(padx=10, pady=10)

# Deixa a tela maximizada
root.after(5, maximizar_janela)
root.mainloop()  