########### Preâmbulo ###########
# Imports do python
import customtkinter as ctk
from tkinter import messagebox
import asyncio

# Imports do projeto
import customizados as ct
from async_loop import loop

# Dicionário para salvar os icones das imagens
imagens = {}

def configurar_servidores(projeto):
    # Cria a janela
    janela = ct.customTopLevel("Conexão Modbus", geometry=(500, 400), buttonSet=False, scrollbar=False, resizable=(False, False))

    # Frame para os botões de edição
    frame_bt = ctk.CTkFrame(janela.frame_interno, fg_color="transparent")
    frame_bt.pack(side="top", fill="x", padx=2, pady=2)
    # Lista com os botões
    btns = {
        "Adicionar": {"command": lambda: adicionar_servidor(), "icone": "servidor.png"},
        "Mudar Nome": {"command": lambda:mudar_nome(), "icone": "edit.png"},
        "Salvar": {"command": lambda:salvar_servidor(), "icone": "save.png"},
        "Remover": {"command": lambda:remover_servidor(), "icone": "del.png"},
    }
    # Adiciona os botoes ao frame
    for key, value in btns.items():
        bt = ct.customIconButton(root=frame_bt, icone=value["icone"], tooltip=key, command=value["command"])
        if key == "Remover":
            bt.pack(side="right", padx=2, pady=2)
        else:
            bt.pack(side="left", padx=2, pady=2)

    # Pega os servidores existentes
    servidores = projeto.servidores
    server_sel = None # Servidor selecionado

    # Frame para os servidores
    frame_servidores = ctk.CTkFrame(janela.frame_interno, width=150, fg_color="transparent")
    frame_servidores.pack(side="left", fill="both", padx=5, pady=5)
        
    # Lista para os servidores
    lista = ctk.CTkScrollableFrame(frame_servidores, fg_color="transparent")
    lista.pack(fill="both", expand=True)
    # Coloca os servidores na lista
    for server in servidores.keys():
        ctk.CTkButton(master=lista, text=server, height=10, corner_radius=0, command=lambda s=server:atualizar_campos(s)).pack(fill="x")

    # Frame para os parâmetros
    frame_parametros = ctk.CTkFrame(janela.frame_interno, fg_color="transparent")
    frame_parametros.pack(side="right", fill="both", expand=True, padx=5, pady=5)
    ctk.CTkLabel(frame_parametros, text="Parâmetros").pack(pady=5, fill="x", anchor="nw")

    # Função para atualizar os parâmetros de acordo com o servidor selecionado
    def atualizar_campos(server):
        # Pega o servidor selecionado e suas configurações
        nonlocal server_sel
        server_sel = server
        configs = {i: k for i, k in vars(servidores[server_sel]).items() if i in ["ip", "porta", "timeout"]}

        # Verifica se tem algum servidor selecionado
        for bt in lista.winfo_children():
            if bt.cget("text") == server_sel:
                bt.configure(fg_color="lightblue",
                             text_color="black")
            else:
                bt.configure(fg_color=ctk.CTkButton(frame_bt).cget("fg_color"),
                             text_color=ctk.CTkButton(frame_bt).cget("text_color"))
                
        # Limpa todos os widgets antigos do frame de parâmetros
        for widget in frame_parametros.winfo_children()[1:]:
            widget.destroy()

        # Cria todos os campos de parâmetros dinamicamente
        for param, value in configs.items():
            janela.addItem(root=frame_parametros, nome=param, item=ctk.CTkEntry, tamanho=100, valor_inicial=str(value))

    # Função para adicionar um novo servidor
    def adicionar_servidor():
        nome = ctk.CTkInputDialog(text="Nome do Servidor:", title="Novo Servidor").get_input()
        if nome != "" and nome is not None:
            if nome not in projeto.servidores:
                projeto.add_servidor(nome)
                # Adiciona o servidor à lista
                ctk.CTkButton(master=lista, text=nome, height=10, corner_radius=0, command=lambda n=nome:atualizar_campos(n)).pack(fill="x")
        else:
            messagebox.showwarning("Erro", "Nome de servidor inválido")

    # Função para mudar o nome de um servidor
    def mudar_nome():
        nonlocal server_sel
        # Verifica se tem algum servidor selecionado
        if not server_sel:
            return
        
        novo_nome = ctk.CTkInputDialog(text="Novo nome:", title="Insira o novo nome do servidor").get_input()
        # Verifica se o novo nome é válido
        if novo_nome and novo_nome != server_sel and novo_nome not in projeto.servidores:
            projeto.novoNome_servidor(server_sel, novo_nome)
            for bt in lista.winfo_children():
                if bt.cget("text") == server_sel:
                    server_sel = novo_nome
                    bt.configure(text=novo_nome)
        else:
            messagebox.showwarning("Erro", "Nome inválido ou nome duplicado")

    # Função para salvar as configurações de um servidor
    def salvar_servidor():
        nonlocal server_sel
        # Verifica se tem algum servidor selecionado
        if not server_sel:
            return

        # Pega a chave e valor
        for frame in frame_parametros.winfo_children()[1:]:
            # O primeiro é o CTkLabel e o segundo é a entrada
            label_widget = frame.winfo_children()[0]
            entry_widget = frame.winfo_children()[1]

            # Salva as configurações
            chave = label_widget.cget("text").replace(":", "")
            valor = entry_widget.get()
            projeto.config_servidor(server_sel, chave, valor)

    # Função para remover um servidor
    def remover_servidor():
        nonlocal server_sel
        # Verifica se tem algum servidor selecionado
        if not server_sel:
            return
        
        # Remove o servidor
        dialog = ct.customDialog("Remover Servidor", f"Deseja remover o servidor {server_sel}?", "yes_no")
        if dialog.result:
            for bt in lista.winfo_children():
                if bt.cget("text") == server_sel:
                    bt.destroy()
            projeto.del_servidor(server_sel)
            
            for widget in frame_parametros.winfo_children()[1:]:
                widget.destroy()

# Função para conectar os servidores
def conectar_servidores(projeto):
    for servidor in projeto.servidores.values():
        asyncio.run_coroutine_threadsafe(servidor.conectar(),loop)