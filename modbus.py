import tkinter as tk
from tkinter import ttk
import pymodbus as mb
import serial.tools.list_ports
import custom_widgets as cw
import config as cfg

def criar_conexao(servidores=None, servidor_id=None):
    # Cria a janela
    janela = cw.menuPropriedades('Conexão Modbus', geometry=(350, 400), resizable=(False, False))
    parametros_tcp = ['Nome', 'IP', 'Porta', 'ID', 'Timeout (s)']
    parametros_rtu = ['Nome', 'Porta Serial', 'Baudrate', 'Paridade', 'Bytesize', 'Stopbits', 'Timeout (s)']
    conexao = tk.StringVar(value='TCP')
    if servidores is None:
        servidores = {}
    if servidor_id is None:
        servidor_id = 1

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
    btn_add = ttk.Button(frame_servidores, text="Adicionar", command=lambda:adicionar_servidor(servidor_id))
    btn_add.pack(padx=5, pady=5)

    # Tabela com os servidores adicionados
    frame_tree = ttk.LabelFrame(janela, text="Lista de Servidores")
    frame_tree.pack(side='bottom', fill='x', padx=5, pady=5)
    config_servidor = ['Nome', 'ID', 'Tipo']
    tree = ttk.Treeview(frame_tree, columns=config_servidor, show='headings', height=3)
    for c in config_servidor:
        tree.heading(c, text=c)
    tree.pack(side='bottom', fill="x", expand=True, padx=5, pady=5)

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
            if param in cfg.rtu_selecionaveis.keys():
                values = list(cfg.rtu_selecionaveis[param].keys())
                entry = ttk.Combobox(frame_temp, values=values, state='readonly')
            else:
                if param == 'Porta Serial':
                    values = [port.device for port in serial.tools.list_ports.comports()]
                    entry = ttk.Combobox(frame_temp, values=values, state='readonly')
                else:
                    entry = ttk.Entry(frame_temp, width=23)
            entry.pack(side='right', padx=5)

    conexao.trace_add('write', atualizar_campos)
    atualizar_campos()

    def adicionar_servidor(servidor_id):
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
        servidores[f'server_{servidor_id}'] = servidor
        servidor_id += 1
        
        # Preenche a tabela com os parâmetros do servidor
        valores = [nome, f'server_{servidor_id}', tipo]
        tree.insert('', 'end', values=valores)  

    return servidores