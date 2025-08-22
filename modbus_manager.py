########### Preâmbulo ###########
# Imports do python
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tktooltip import ToolTip
import serial.tools.list_ports

# Imports do projeto
import custom_widgets as cw
import utils as ut

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

imagens = {}

def configurar_servidores(projeto):
    # Cria a janela
    janela = cw.janelaScroll('Conexão Modbus', geometry=(800, 450), resizable=(False, False), scrollbar=False)
    parametros_tcp = ['Nome', 'IP', 'Porta', 'Timeout (s)']
    parametros_rtu = ['Nome', 'Porta Serial', 'Baudrate', 'Paridade', 'Bytesize', 'Stopbits', 'Timeout (s)']
    conexao = tk.StringVar(value='TCP')

    # Extrai os servidores do projeto
    servidores = projeto.dados['servidores']
    servidores['teste_rtu'] = {'tipo':'RTU', 'porta':'COM1', 'baudrate':9600, 'paridade':'N', 'bytesize':8, 'stopbits':1, 'timeout':1}
    servidores['teste_tcp'] = {'tipo':'TCP', 'ip':'237.84.2.178', 'porta':502, 'timeout':1}

    # Frame para os servidores
    frame_servidores = ttk.LabelFrame(janela, text="Configurar Servidor")
    frame_servidores.pack(side='left', anchor='w', fill='both', expand=True, padx=5, pady=5)
    frame_serv_bt = ttk.Frame(frame_servidores)
    frame_serv_bt.pack(padx=5, pady=5)
    btns = {
        'Adicionar':{
            'command':lambda:adicionar_servidor(projeto, lista),
            'image':'add.png',
        },
        'Remover':{
            'command':lambda:remover_servidor(projeto, lista),
            'image':'del.png',
        }
    }
    # Adiciona os botoes ao frame
    for key, value in btns.items():
        imagens[key] = ut.imagem(value['image'], (15, 15))
        bt = ttk.Button(frame_serv_bt, command=value['command'], image=imagens[key])
        bt.pack(side='left', padx=5, pady=5)
        ToolTip(bt, msg=key)
    lista = tk.Listbox(frame_servidores, height=20)
    lista.pack(fill='both')
    lista.bind('<<ListboxSelect>>', lambda e:atualizar_campos())
    # Adiciona os servidores existentes na lista
    for server in servidores.keys():
        lista.insert('end', server)

    # Frame para os parâmetros
    frame_parametros = ttk.LabelFrame(janela, text="Parâmetros")
    frame_parametros.pack(side='right', fill='both', expand=True, padx=5, pady=5)
    # Adiciona os parametros conforme o tipo de conexão
    conexao = tk.StringVar()
    conexao.trace_add('write', atualizar_campos)
    def atualizar_campos(*args):
        # Limpa campos antigos
        for widget in frame_parametros.winfo_children():
            widget.destroy()
        # Seleciona parâmetros conforme tipo
        tipo = servidores[lista.get(lista.curselection()[0])]['tipo']
        if tipo == 'TCP':
            parametros = parametros_tcp
        else:
            parametros = parametros_rtu
        # Cria campos
        ttk.Combobox(frame_temp, values=['TCP', 'RTU'], textvariable=conexao, state='readonly').pack(anchor='w', padx=5, pady=5)
        ttk.Label(frame_temp, text=param).pack(side='left', padx=5)
        for param in parametros:
            frame_temp = ttk.Frame(frame_parametros)
            frame_temp.pack(fill='x', pady=2)
            ttk.Label(frame_temp, text='Tipo de Conexão:').pack(anchor='w', padx=5, pady=5)
            if param in rtu_selecionaveis.keys():
                values = list(rtu_selecionaveis[param].keys())
                entry = ttk.Combobox(frame_temp, values=values, state='readonly')
            elif param == 'Porta Serial':
                values = [port.device for port in serial.tools.list_ports.comports()]
                entry = ttk.Combobox(frame_temp, values=values, state='readonly')
            else:
                entry = ttk.Entry(frame_temp, width=23)
            entry.pack(side='right', padx=5)

def adicionar_servidor(projeto, lista):
    nome = cw.perguntarTexto('Nome', 'Insira o nome do servidor')
    if nome != '':
        lista.insert('end', nome)

def remover_servidor(projeto, lista):
    if lista.curselection():
        if messagebox.askyesno('Confirmar', 'Deseja excluir o servidor?'):
            lista.delete(lista.curselection())