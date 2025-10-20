import json
import customtkinter as ctk
from tkinter import filedialog

import managers.project_manager as pm
import managers.server_manager as sm
import managers.widget_manager as wm

def salvar_projeto(projeto):
    # Variáveis auxiliares
    objetos_proibidos = ["item","canvas", "image", "imagem", "classe", "classeCTk", "valor_interno",
                         "textvariable", "client", "tarefas"]
    dados_projeto = {}

    # Serializar as abas
    abas_dict = {}
    for nome_aba, aba_objeto in projeto.abas.items():
        # Copia todos os atributos do objeto da aba
        aba_dados = {atributo: valor for atributo, valor in vars(aba_objeto).items() if atributo not in objetos_proibidos}
        # Serializa os widgets da aba, se existirem
        if hasattr(aba_objeto, "widgets"):
            widgets_dict = {}
            for nome_widget, widget_objeto in aba_objeto.widgets.items():
                # Serializa o widget, ignorando referências de objetos
                widget_dados = {atributo: valor for atributo, valor in vars(widget_objeto).items() if atributo not in objetos_proibidos}
                if "textvariable" in widget_dados["propriedades"]: widget_dados["propriedades"].pop("textvariable")
                widgets_dict[nome_widget] = widget_dados
            aba_dados["widgets"] = widgets_dict
        abas_dict[nome_aba] = aba_dados

    # Serializar os servidores
    servidores_dict = {}
    for nome_servidor, servidor_objeto in projeto.servidores.items():
        # Vars() para obter todas as propriedades do objeto do servidor
        servidor = {"parametros":{atributo: valor for atributo, valor in vars(servidor_objeto).items()
                                  if atributo not in objetos_proibidos}}
        servidores_dict[nome_servidor] = servidor

    # Concatena tudo no projeto
    dados_projeto["abas"] = abas_dict
    dados_projeto["servidores"] = servidores_dict
    print(dados_projeto)

    # Salva o projeto
    # nome_projeto = ct.customDialog("Salvar projeto", "Qual o nome do projeto?")
    caminho_escolhido = filedialog.asksaveasfilename(title="Salvar projeto", defaultextension=".pbc", filetypes=[("PBC Files", "*.pbc")])
    if caminho_escolhido:
        # Cria/modifica um arquivo.json pra salvar o projeto
        with open(caminho_escolhido, "w") as f:
            json.dump(dados_projeto, f, ensure_ascii=False, indent=4, default=str)

def carregar_projeto(notebook):
    # Seleciona o arquivo do projeto
    caminho = filedialog.askopenfilename(
        title="Abrir projeto",
        filetypes=[("Projetos PyBusControl", "*.pbc")]
    )
    if not caminho:
        return None  # usuário cancelou

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except Exception as e:
        print(f"[ERRO] Falha ao abrir o projeto: {e}")
        return None
 
    # Instancia o projeto
    root_projeto = ctk.CTkFrame(notebook, fg_color="transparent")
    root_projeto.pack(fill="x", expand=True)
    projeto = pm.Projeto(root_projeto)
    # Cria a aba do projeto
    nome_projeto = caminho.split("/")[-1].replace(".pbc", "")
    notebook.add(root_projeto, text=nome_projeto)
    notebook.select(root_projeto)

    # ======== CARREGA SERVIDORES ========
    servidores = dados.get("servidores")
    for nome_serv, info_serv in servidores.items():
        parametros = info_serv.get("parametros")
        projeto.add_servidor(nome_serv)
        for param, valor in parametros.items():
            projeto.config_servidor(nome_serv, param, valor)
    
    sm.conectar_servidores(projeto)

    # ======== CARREGA ABAS ========
    abas = dados.get("abas",)
    for nome_aba, info_aba in abas.items():
        projeto.add_aba(nome_aba)
        aba = projeto.abas[nome_aba]

        # Tamanho
        tamanho = info_aba.get("tamanho")
        projeto.config_aba("tamanho", tamanho)

        # Imagem de fundo
        caminho_img = info_aba.get("caminho_imagem")
        if caminho_img:
            projeto.config_aba("imagem", caminho_img)

        # ======== CARREGA WIDGETS ========
        widgets = info_aba.get("widgets")
        for id_widget, info_widget in widgets.items():
            nome = info_widget.get("nome")
            props = info_widget.get("propriedades")
            pos = info_widget.get("posicao")

            # Garante que fonte seja tupla
            if isinstance(props.get("font"), list):
                fonte = props["font"]
                props["font"] = (fonte[0], int(fonte[1]))

            # Cria o widget na posição correta
            wid = projeto.add_widget(nome, pos[0], pos[1])
            widget = aba.widgets[wid]

            # Aplica as propriedades
            for prop, valor in props.items():
                projeto.config_widget(wid, prop, valor)

            # Aplica comando (Modbus, etc.)
            comando = info_widget.get("comando")
            if comando:
                widget.comando = comando
                try:
                    widget.item.configure(command=lambda: wm.executar_comando(projeto, widget))
                except:
                    wm.executar_comando(projeto, widget)

            # Caminho de imagem (se houver)
            if info_widget.get("caminho_imagem"):
                widget.caminho_imagem = info_widget["caminho_imagem"]

    print(f"[OK] Projeto '{projeto.nome}' carregado com sucesso!")
    return projeto