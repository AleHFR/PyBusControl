########### Preâmbulo ###########
# Imports do python
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
from tktooltip import ToolTip
import serial.tools.list_ports

# Imports do projeto
import custom_widgets as cw
import utils as ut

# Dicionário com as opções para os Combobox
selecionaveis = {
    'Conexão': ['TCP', 'RTU'],
    'Baudrate': ['9600', '19200', '38400', '57600', '115200'],
    'Paridade': ['N', 'P', 'I'],
    'Bytesize': ['8', '7'],
    'Stopbits': ['1', '2']
}

# Estruturas padrão para cada tipo de servidor
estrutura_servidor = {
    'TCP': {'IP': '127.168.0.1', 'Porta': 502, 'Timeout (s)': 1},
    'RTU': {'Porta Serial': 'COM1', 'Baudrate': '9600', 'Paridade': 'N', 'Bytesize': 8, 'Stopbits': 1, 'Timeout (s)': 1}
}

# Dicionário para salvar os icones das imagens
imagens = {}

def configurar_servidores(projeto):
    # Cria a janela
    janela = cw.janelaScroll('Conexão Modbus', geometry=(300, 300), button_set=False)

    # Pega os servidores existentes
    servidores = projeto.servidores
    servidor_selecionado = None

    # Frame para os servidores
    frame_servidores = ctk.CTkFrame(janela, width=150)
    frame_servidores.pack(side='left', fill='both', padx=5, pady=5)
    
    # Frame para os botões
    frame_bt = ctk.CTkFrame(frame_servidores)
    frame_bt.pack(anchor='w', fill='x', padx=2, pady=2)
    # Lista com os botões
    btns = {
        'Adicionar TCP': {'command': lambda: adicionar_servidor('TCP'), 'image': 'tcp.png'},
        'Adicionar RTU': {'command': lambda: adicionar_servidor('RTU'), 'image': 'rtu.png'},
        'Adicionar Gateway': {'command': lambda: adicionar_servidor('GATEWAY'), 'image': 'gateway.png'},
        'Mudar Nome': {'command': lambda: mudar_nome(), 'image': 'edit.png'},
        'Editar': {'command': lambda: editar_servidor(), 'image': 'config.png'},
        'Salvar': {'command': lambda: salvar_servidor(), 'image': 'save.png'},
        'Remover': {'command': lambda: remover_servidor(), 'image': 'del.png'},
    }
    # Adiciona os botoes ao frame
    for key, value in btns.items():
        imagens[key] = ut.imagem(value['image'], (15, 15))
        bt = ctk.CTkButton(frame_bt,text='', width=0, fg_color='#FFFFFF', hover_color='gray', command=value['command'], image=imagens[key])
        bt.pack(side='left', padx=2, pady=2)
        ToolTip(bt, msg=key)
        
    # Lista para os servidores
    lista = ctk.CTkScrollableFrame(frame_servidores)
    lista.pack(fill='both', expand=True)
    # Coloca os servidores na lista
    for server in servidores.keys():
        ctk.CTkButton(master=lista, text=server, corner_radius=0, command=lambda s=server:atualizar_campos(s)).pack(fill='x')

    # Frame para os parâmetros
    frame_parametros = ctk.CTkFrame(janela)
    frame_parametros.pack(side='right', fill='both', expand=True, padx=5, pady=5)
    ctk.CTkLabel(frame_parametros, text='Parâmetros', text_color='black').pack(pady=5, fill='x', anchor='nw')

    # Função para atualizar os parâmetros de acordo com o servidor selecionado
    def atualizar_campos(server):
        nonlocal servidor_selecionado
        # Verifica se tem algum servidor selecionado
        servidor_selecionado = servidores.get(server)
        for bt in lista.winfo_children():
            if bt.cget('text') == servidor_selecionado.nome:
                bt.configure(fg_color='lightblue',
                             text_color='black')
            else:
                bt.configure(fg_color=ctk.CTkButton(frame_bt).cget('fg_color'),
                             text_color=ctk.CTkButton(frame_bt).cget('text_color'))
        # Limpa todos os widgets antigos do frame de parâmetros
        for widget in frame_parametros.winfo_children()[1:]:
            widget.destroy()

        # Cria todos os campos de parâmetros dinamicamente
        for param, value in servidor_selecionado.modbus.items():
            # Cria um frame temporário simplesmente pra organizar os campos
            frame_temp = ctk.CTkFrame(frame_parametros)
            frame_temp.pack(fill='x', pady=2, padx=2)
            ctk.CTkLabel(frame_temp, text=f'{param}:').pack(side='left')
            # Cria as combobox de acordo com o parâmetro
            entry = None
            if param in selecionaveis.keys() or param == 'Porta Serial':
                # Adiciona as portas seriais de acordo com o sistema operacional
                if param == 'Porta Serial':
                    portas = [p.device for p in serial.tools.list_ports.comports()]
                    entry = ctk.CTkComboBox(frame_temp, values=portas, width=100)
                else:
                    entry = ctk.CTkComboBox(frame_temp, values=selecionaveis[param], width=100)
                entry.set(value)
            else:
                entry = ctk.CTkEntry(frame_temp, width=100)
                entry.insert(0, value)
            # Desabilita os campos por padrão
            if entry:
                entry.configure(state='disabled')
                entry.pack(side='right')

    # Função para adicionar um novo servidor
    def adicionar_servidor(tipo):
        nome = ctk.CTkInputDialog(text='Nome do Servidor:', title='Novo Servidor').get_input()
        def aplicar(nome, tipo): # Função para criar um servidor usando as configs padrão
            if nome != ''and nome not in projeto.servidores:
                if tipo:
                    projeto.add_servidor(nome, tipo, estrutura_servidor[tipo].copy())
                else:
                    messagebox.showwarning('Erro', 'Selecione uma conexão')
                    return
                # Adiciona o servidor à lista
                ctk.CTkButton(master=lista, text=nome, corner_radius=0, command=lambda n=nome:atualizar_campos(n)).pack(fill='x')
                editar_servidor()
            else:
                messagebox.showwarning('Erro', 'Nome de servidor inválido')
        aplicar(nome, tipo)

    # Função para mudar o nome de um servidor
    def mudar_nome():
        nonlocal servidor_selecionado
        novo_nome = ctk.CTkInputDialog(text='Novo nome:', title='Insira o novo nome do servidor').get_input()
        # Verifica se o novo nome é válido
        if novo_nome and novo_nome != servidor_selecionado.nome and novo_nome not in projeto.servidores:
            projeto.novoNome_servidor(servidor_selecionado.nome, novo_nome)
            for bt in lista.winfo_children():
                if bt.cget('text') == servidor_selecionado.nome:
                    bt.configure(text=novo_nome)
        else:
            messagebox.showwarning('Erro', 'Nome inválido ou nome duplicado')

    # Função para editar um servidor
    def editar_servidor():
        # Procura os campos e os habilita
        for frame in frame_parametros.winfo_children():
            widget = frame.winfo_children()[1] # O segundo widget é sempre o de entrada
            if isinstance(widget, ctk.CTkEntry):
                widget.configure(state='normal')
            elif isinstance(widget, ctk.CTkComboBox):
                widget.configure(state='readonly')

    def salvar_servidor():
        nonlocal servidor_selecionado
        # Verifica se tem algum servidor selecionado
        if not servidor_selecionado:
            return
        
        # Usar a seleção atual
        nome_servidor = servidor_selecionado.nome
        # Pega a chave e valor
        for frame in frame_parametros.winfo_children():
            label_widget = frame.winfo_children()[0]
            entry_widget = frame.winfo_children()[1]
            # Trata os dados
            chave = label_widget.cget('text').replace(':', '')
            valor = entry_widget.get()
            # Atualiza o dicionário no projeto
            projeto.config_servidor(nome_servidor, chave, valor)
            # Desabilita o campo após salvar
            entry_widget.configure(state='disabled')
        projeto.exibir()

    # Função para remover um servidor
    def remover_servidor():
        nonlocal servidor_selecionado
        if servidor_selecionado:
            nome_servidor = servidor_selecionado.nome
            if cw.ask_yes_no('Remover Servidor', f'Deseja remover o servidor {nome_servidor}?') == 'Remover':
                for bt in lista.winfo_children():
                    if bt.cget('text') == nome_servidor:
                        bt.destroy()
                projeto.del_servidor(nome_servidor)
                
                for widget in frame_parametros.winfo_children()[1:]:
                    widget.destroy()

# Função para conectar os servidores
def conectar_servidores(projeto):
    for server in projeto.servidores.keys():
        projeto.conectar_servidor(server)