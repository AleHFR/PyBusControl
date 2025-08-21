########### Preâmbulo ###########
# Imports do python
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog, colorchooser
import pymodbus as mb
import serial.tools.list_ports

# Imports do projeto
import custom_widgets as cw
import scada_settings as ss

rtu_selecionaveis = {
    'Baudrate':{
        '9600': 9600,
        '19200': 19200,
        '38400': 38400,
        '57600': 57600,
        '115200': 115200,
    },
    'Paridade':{
        'Nenhum': 'N',
        'Par': 'P',
        'Impar': 'I',
    },
    'Bytesize':{
        '8': 8,
        '7': 7,
    },
    'Stopbits':{
        '1': 1,
        '2': 2,
    }
}

def criar_conexao(projeto):
    # Cria a janela
    janela = cw.janelaScroll('Conexão Modbus', geometry=(350, 450), resizable=(False, False))
    parametros_tcp = ['Nome', 'IP', 'Porta', 'Timeout (s)']
    parametros_rtu = ['Nome', 'Porta Serial', 'Baudrate', 'Paridade', 'Bytesize', 'Stopbits', 'Timeout (s)']
    conexao = tk.StringVar(value='TCP')

    # Extrai os servidores do projeto
    servidores = projeto.dados['servidores']

    # Frame para adicionar o servidor
    frame_servidores = ttk.LabelFrame(janela, text="Adicionar Servidor")
    frame_servidores.pack(fill='x', padx=5, pady=5)

    # Combobox para selecionar tipo de conexão
    combo_tipo = ttk.Combobox(frame_servidores, values=['TCP', 'RTU'], textvariable=conexao, state='readonly', width=10)
    combo_tipo.pack(padx=5, pady=2, side='top')

    # Frame para os campos dinâmicos
    frame_campos = ttk.Frame(frame_servidores)
    frame_campos.pack(fill='x', padx=5, pady=5)

    # Botão para adicionar o servidor
    btn_add = ttk.Button(frame_servidores, text="Adicionar", command=lambda:adicionar_servidor(projeto))
    btn_add.pack(padx=5, pady=5)

    # Tabela com os servidores adicionados
    frame_tree = ttk.LabelFrame(janela, text="Lista de Servidores")
    frame_tree.pack(side='bottom', fill='x', padx=5, pady=5)
    colunas = ['Nome', 'Tipo']
    tree = ttk.Treeview(frame_tree, columns=colunas, show='headings', height=8)
    scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y', padx=5, pady=5)
    tree.pack(side='left', fill="both", expand=True, padx=5, pady=5)
    tree.configure(yscrollcommand=scrollbar.set)
    for c in colunas:
        tree.heading(c, text=c)
    tree.pack(side='bottom', fill="x", expand=True, padx=5, pady=5)

    # Atualiza a tabela com os servidores já existentes do projeto
    for servidor in servidores.keys():
        tree.insert('', 'end', values=[servidor, servidores[servidor]['tipo']])

    def atualizar_campos(*args):
        # Limpa campos antigos
        for widget in frame_campos.winfo_children():
            widget.destroy()
        # Seleciona parâmetros conforme tipo
        if conexao.get() == 'TCP':
            parametros = parametros_tcp
        else:
            parametros = parametros_rtu
        # Cria campos
        for param in parametros:
            frame_temp = ttk.Frame(frame_campos)
            frame_temp.pack(fill='x', pady=2)
            ttk.Label(frame_temp, text=param).pack(side='left', padx=5)
            if param in rtu_selecionaveis.keys():
                values = list(rtu_selecionaveis[param].keys())
                entry = ttk.Combobox(frame_temp, values=values, state='readonly')
            elif param == 'Porta Serial':
                values = [port.device for port in serial.tools.list_ports.comports()]
                entry = ttk.Combobox(frame_temp, values=values, state='readonly')
            else:
                entry = ttk.Entry(frame_temp, width=23)
            entry.pack(side='right', padx=5)

    conexao.trace_add('write', atualizar_campos)
    atualizar_campos()

    def adicionar_servidor(projeto):
        # Verifica se tem algum campo em branco
        if '' in [i.winfo_children()[1].get() for i in frame_campos.winfo_children()]:
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
        # Preenche o dicionário com os parâmetros do servidor
        servidor = {}
        nome = None
        tipo = None
        # Seleciona parâmetros conforme tipo
        if conexao.get() == 'TCP':
            servidor['tipo'] = 'TCP'
            tipo = 'TCP'
        else:
            servidor['tipo'] = 'RTU'
            tipo = 'RTU'
        for i in frame_campos.winfo_children():
            label = i.winfo_children()[0].cget('text')
            value = i.winfo_children()[1].get()
            if label == 'Nome':
                nome = value
            servidor[label] = value
        # Verifica se existe um servidor com o mesmo nome
        if nome in servidores.keys():
            messagebox.showerror('Erro', 'Ja existe um servidor com esse nome')
            return
        servidores[nome] = servidor
        
        # Preenche a tabela com os parâmetros do servidor
        valores = [nome, tipo]
        tree.insert('', 'end', values=valores)  

        # Salva no projeto
        projeto.dados['servidores'] = servidores
        projeto.exibir()