########### Preâmbulo ############
# Imports do python
import inspect
import customtkinter as ctk
from tkinter import messagebox

# Imports do projeto
import customizados as ct
import drivers.widgets_driver as wd
import dicts as dt

# Dicionário para salvar os icones das imagens
imagens = {}

#################### Adicionar um widget ####################
def adicionar_widget(projeto):
    # Verifica se tem ao menos uma aba aberta
    if not projeto.notebook.tabs():
        messagebox.showerror("Erro", "Nenhuma aba existente")
        return

    # Procura a aba e o canvas
    frame = projeto.notebook.select()
    nome_aba = projeto.notebook.tab(frame, "text")
    aba = projeto.abas[nome_aba]
    canvas = aba.canvas
    
    # Habilita o click na tela pra definir onde o widget vai ficar
    def click(event):
        # Muda o cursor pra seta
        canvas.config(cursor="arrow")
        dica.hide_tooltip()
        # salva posição
        x, y = event.x, event.y

        # Cria o widget e remove o marcador
        def ok(tipo):
            projeto.add_widget(tipo, x, y)

        # Encontra as classes de widgets
        classes_encontradas = [name for name, obj in inspect.getmembers(wd, inspect.isclass)
                               if obj.__module__ == wd.__name__ and name != "Widget"]
        # Cria um minimeu pra selecionar o widget
        context_menu = ct.customMenu(canvas)
        for tipo in classes_encontradas:
            context_menu.add_command(label=tipo, command=lambda t=tipo:ok(t))
        context_menu.post(event.x_root, event.y_root)
        context_menu.config()

        # Desabilita o bind
        canvas.unbind("<Button-1>")
        
    # Muda o cursor pra cruz
    canvas.config(cursor="tcross")
    # Chama o bind e escreve a dica
    dica = ct.customClickTooltip(canvas, text="Clique para adicionar um widget")
    dica.show_tooltip()
    canvas.bind("<Button-1>", lambda e:click(e))

def comando(projeto, wid):
    # Verifica se existe algum servidor cadastrado
    if not projeto.servidores:
        messagebox.showerror("Erro", "Nenhum servidor cadastrado")
        return
    # Localiza os objetos do projeto
    frame_atual = projeto.notebook.select()
    nome_aba = projeto.notebook.tab(frame_atual, "text")
    aba = projeto.abas[nome_aba]
    widget = aba.widgets[wid]
    item = widget.item

    # Estrutura de dados
    parametros_widget = {}
    comandos_modbus = list(dt.funcoes_modbus.keys())
    servidores = list(projeto.servidores.keys())

    # Cria a janela
    janela = ct.customTopLevel("Comando", geometry=(400, 400), buttonSet=True, resizable=(False, False), command=lambda: salvar())
    
    # Montagem da janela
    valor_inicial = widget.comando.get("comando")
    comando_sel = janela.addItem(
        root=janela.frame_interno, nome="comando",
        item=ctk.CTkComboBox, tamanho=200,
        valores=comandos_modbus, valor_inicial=valor_inicial
    )
    janela.itens["comando"].configure(command=lambda event: atualizar())

    frame_comando = ctk.CTkFrame(janela.frame_interno, fg_color="transparent")
    frame_comando.pack(fill="x")

    # Filtro de atributos que não devem ser exibidos
    atributos_proibidos = {
        "classe", "posicao", "caminho_imagem", "classeCTk", "canvas",
        "item", "imagem", "image", "nome", "propriedades", "comando", "valor_interno"
    }

    # Atributos do widget válidos
    atributos_widget = {
        chave: valor for chave, valor in vars(widget).items()
        if chave not in atributos_proibidos
    }

    # Função: Atualiza os parâmetros do comando
    def atualizar():
        nonlocal parametros_widget

        # Limpa parâmetros antigos
        for child in frame_comando.winfo_children():
            child.destroy()

        # Puxa o comando atual e relaciona os parâmetros
        comando_atual = comando_sel.get()
        parametros_comando = widget.comando["parametros"] if widget.comando["parametros"] != {} else dt.funcoes_modbus[comando_atual]["parametros"].copy()
        
        # Determina parâmetros conforme o tipo do comando
        if "Read" in comando_atual or "Write" in comando_atual:
            parametros_widget = {"servidor": servidores, **parametros_comando, **atributos_widget}
        else:
            parametros_widget = {**parametros_comando, **atributos_widget}

        # Cria os widgets de entrada para cada parâmetro
        for param, valor in parametros_widget.items():
            if isinstance(valor, list):
                janela.addItem(root=frame_comando, nome=param, item=ctk.CTkComboBox, tamanho=200, valores=valor, valor_inicial=valor[0])
            else:
                janela.addItem(root=frame_comando, nome=param, item=ctk.CTkEntry, tamanho=200, valor_inicial=str(valor))

    # Função: Salva alterações
    def salvar():
        comando_atual = comando_sel.get()
        widget.comando["comando"] = comando_atual
        widget.comando["parametros"] = {}

        for param in parametros_widget:
            valor = janela.itens[param].get()
            if param in atributos_widget:
                set = getattr(widget, f"set_{param}")
                set(valor)
            else:
                widget.comando["parametros"][param] = valor
        try:
            item.configure(command=lambda: executar_comando(projeto, widget))
        except:
            executar_comando(projeto, widget)

    # Inicialização
    if valor_inicial != " ":
        atualizar()

def visual(projeto, wid):
    # Encontra od atributos necessários
    frame = projeto.notebook.select()
    nome_aba = projeto.notebook.tab(frame, "text")
    aba = projeto.abas[nome_aba]
    widget = aba.widgets[wid]

    # Cria a janela
    janela = ct.customTopLevel("Propriedades", geometry=(400, 400), buttonSet=True, resizable=(False, False), command=lambda:salvar())

    # Funções auxiliares
    def salvar():
        # Puxa as informaçoes referentes ao visual
        for param in widget.propriedades.keys():
            if param in dt.parametros_nao_visuais:continue
            param_rev = dt.traducoes_parametros[param] # Traduz o parâmetro
            # Trabalha as atribuições dependendo do parametro
            valor = None
            if param in dt.parametros_especiais["cores"]:
                valor = janela.itens[param_rev].cget("fg_color")
            elif param == "font":
                valor = (janela.itens[param_rev][0].get(), janela.itens[param_rev][1].get())
            else:
                valor = janela.itens[param_rev].get()
            # Atualiza o widget
            projeto.config_widget(wid, param, valor)

    # Cria todos os campos de parâmetros dinamicamente
    for param, value in widget.propriedades.items():
        # Pula algumas propriedades não pertinentes
        if param in dt.parametros_nao_visuais:continue
        # Trada o parâmetro para português
        nome = dt.traducoes_parametros[param]

        # Cria as entrys de acordo com a propriedade
        if param in dt.parametros_especiais["cores"]:
            janela.addItem(root=janela.frame_interno, nome=nome, item=ct.customSelecionaCor, valor_inicial=value)
        elif param in dt.parametros_especiais["numericos"]: # Parametros numericos
            janela.addItem(root=janela.frame_interno, nome=nome, item=ct.customSpinbox, valor_inicial=value)
        elif param in dt.parametros_especiais["pre-definidos"].keys():
            janela.addItem(root=janela.frame_interno, nome=nome, item=ctk.CTkComboBox, valor_inicial=value, valores=dt.parametros_especiais["pre-definidos"][param])
        elif param == "font": # Trata se é fonte, coloca estilo e tamnho separados
            style, size = value[0], value[1]
            janela.addTupleItem(root=janela.frame_interno, nome=nome, tamanho=200,
                                item_1=ctk.CTkComboBox, valores_1=dt.parametros_especiais["font"]["styles"], valor_inicial_1=style,
                                item_2=ctk.CTkComboBox, valores_2=dt.parametros_especiais["font"]["sizes"], valor_inicial_2=size)
        elif param == "image": # Trata se é imagem
            janela.addItem(root=janela.frame_interno, nome=nome, tamanho=170, item=ct.customBuscaArquivo, valor_inicial=value)
        else: # Parametro de texto
            janela.addItem(root=janela.frame_interno, nome=nome, item=ctk.CTkEntry, valor_inicial=value)

def executar_comando(projeto, widget):
    # Funcões de callback
    def atualizar_display(valor):
        try:
            widget.atualizar(valor)
        except:
            None
    def callback(valor):
        widget.item.after(0, atualizar_display, valor)

    comando_dict = widget.comando
    comando = comando_dict["comando"]
    parametros = comando_dict["parametros"]
    # Verifica se é um comando modbus
    if "Read" in comando or "Write" in comando:
        # Solicita o comando ao servidor
        servidor = projeto.servidores[parametros["servidor"]]
        servidor.addPolling(comando_dict, callback)
    # Se não, lida com os demais comandos
    else:
        if comando == "Trocar Aba":
            nomes = [projeto.notebook.tab(tab_id, "text") for tab_id in projeto.notebook.tabs()]
            indice = nomes.index(parametros["aba"])
            projeto.notebook.select(indice)