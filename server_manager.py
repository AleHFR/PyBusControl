########### Preâmbulo ###########
# Imports do python
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tktooltip import ToolTip
import serial.tools.list_ports

# Imports do projeto
import server_handler as mh
import custom_widgets as cw
import utils as ut

# Dicionário com as opções para os Combobox
selecionaveis = {
    'Conexão': ['TCP', 'RTU'],
    'Baudrate': ['9600', '19200', '38400', '57600', '115200'],
    'Paridade': ['N', 'P', 'I'],
    'Bytesize': [8, 7],
    'Stopbits': [1, 2]
}

# Estruturas padrão para cada tipo de servidor
estrutura_servidor = {
    'TCP': {'IP': '127.168.0.1', 'Porta': 502, 'Timeout (s)': 1},
    'RTU': {'Porta Serial': 'COM1', 'Baudrate': '9600', 'Paridade': 'N', 'Bytesize': 8, 'Stopbits': 1, 'Timeout (s)': 1}
}

# Dicionário para salvar os widgets das imagens
imagens = {}

def configurar_servidores(projeto):
    # Cria a janela
    janela = cw.janelaScroll('Conexão Modbus', geometry=(450, 400), resizable=(False, False), scrollbar=False)
    
    # Adiciona dados dos servidores
    if not projeto.servidores:
        projeto.add_servidor('Esp32', 'TCP', {'IP': '127.168.0.3', 'Porta': 1502, 'Timeout (s)': 1})
    servidores = projeto.servidores

    # Frame para os servidores
    frame_servidores = ttk.LabelFrame(janela, text="Configurar Servidor")
    frame_servidores.pack(side='left', anchor='n', fill='y', padx=5, pady=5)
    
    # Frame para os botões
    frame_serv_bt = ttk.Frame(frame_servidores)
    frame_serv_bt.pack(anchor='w', fill='x', padx=2, pady=2)
    # Lista com os botões
    btns = {
        'Adicionar': {'command': lambda: adicionar_servidor(), 'image': 'add.png'},
        'Mudar Nome': {'command': lambda: mudar_nome(), 'image': 'edit.png'},
        'Editar': {'command': lambda: editar_servidor(), 'image': 'config.png'},
        'Salvar': {'command': lambda: salvar_servidor(), 'image': 'save.png'},
        'Remover': {'command': lambda: remover_servidor(), 'image': 'del.png'},
    }
    # Adiciona os botoes ao frame
    for key, value in btns.items():
        imagens[key] = ut.imagem(value['image'], (15, 15))
        bt = ttk.Button(frame_serv_bt, command=value['command'], image=imagens[key])
        if key == 'Remover': # Coloca o botão de remover longe dos demais
            bt.pack(side='right', padx=2, pady=2)
        else:
            bt.pack(side='left', padx=2, pady=2)
        ToolTip(bt, msg=key)
    # Lista para os servidores
    lista = tk.Listbox(frame_servidores, height=20, width=30)
    lista.pack(fill='both', expand=True)
    # Define o evento para chamar a atualização em modo de visualização
    lista.bind('<<ListboxSelect>>', lambda e:atualizar_campos())
    # Coloca os servidores na lista
    for server in servidores.keys():
        lista.insert('end', server)

    # Frame para os parâmetros
    frame_parametros = ttk.LabelFrame(janela, text="Parâmetros")
    frame_parametros.pack(side='right', fill='both', expand=True, padx=5, pady=5)

    # Função para atualizar os parâmetros de acordo com o servidor selecionado
    def atualizar_campos():
        # Verifica se tem algum servidor selecionado
        selecao = lista.curselection()
        if not selecao: return
        nome_servidor = lista.get(selecao[0])
        servidor_selecionado = servidores.get(nome_servidor)

        # Limpa todos os widgets antigos do frame de parâmetros
        for widget in frame_parametros.winfo_children():
            widget.destroy()

        # Cria todos os campos de parâmetros dinamicamente
        for param, value in servidor_selecionado.modbus.items():
            print(param, value)
            # Cria um frame temporário simplesmente pra organizar os campos
            frame_temp = ttk.Frame(frame_parametros)
            frame_temp.pack(fill='x', pady=2, padx=2)
            ttk.Label(frame_temp, text=f'{param}:').pack(side='left')
            # Cria as combobox de acordo com o parâmetro
            entry = None
            if param in selecionaveis.keys():
                # Adiciona as portas seriais de acordo com o sistema operacional
                if param == 'Porta Serial':
                    portas = list(serial.tools.list_ports.comports())
                    entry = ttk.Combobox(frame_temp, values=portas, width=17)
                else:
                    entry = ttk.Combobox(frame_temp, values=selecionaveis[param], width=17)
                entry.set(value)
            else:
                entry = ttk.Entry(frame_temp, width=20)
                entry.insert(0, value)
            # Desabilita os campos por padrão
            if entry:
                entry.config(state='disabled')
                entry.pack(side='right')

    def adicionar_servidor():
        janela = cw.janelaScroll('Adicionar Servidor', geometry=(200, 200), resizable=(False, False), scrollbar=False, command=lambda:aplicar(nome, conexao))
        ttk.Label(janela, text='Insira o nome do servidor').pack(pady=5)
        nome = ttk.Entry(janela, width=20)
        nome.pack(pady=5)
        ttk.Label(janela, text='Selecione o tipo de conexão').pack(pady=5)
        conexao = ttk.Combobox(janela, values=['TCP', 'RTU'], width=17, state='readonly')
        conexao.pack(pady=5)
        def aplicar(nome, conexao):
            nome = nome.get()
            conexao = conexao.get()
            if nome != ''and nome not in projeto.servidores:
                if conexao:
                    projeto.add_servidor(nome, conexao, estrutura_servidor[conexao].copy())
                else:
                    messagebox.showwarning('Erro', 'Selecione uma conexão')
                    return
                lista.insert('end', nome)
                lista.selection_clear(0, 'end')
                lista.selection_set('end')
                lista.event_generate("<<ListboxSelect>>")
                editar_servidor()
            else:
                messagebox.showwarning('Erro', 'Nome de servidor inválido')

    def salvar_servidor():
        selecao = lista.curselection()
        # Verifica se tem algum servidor selecionado
        if not selecao:
            return
        
        # Usar a seleção atual
        nome_servidor = lista.get(selecao[0])
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
            entry_widget.config(state='disabled')
        projeto.exibir()

    def mudar_nome():
        selecao = lista.curselection()
        if selecao:
            nome_antigo = lista.get(selecao[0])
            novo_nome = cw.perguntarTexto('Novo nome', 'Insira o novo nome do servidor', default_text=nome_antigo)
            if novo_nome and novo_nome != nome_antigo and novo_nome not in projeto.servidores:
                projeto.novoNome_servidor(nome_antigo, novo_nome)
                projeto.exibir()
                lista.delete(selecao[0])
                lista.insert(selecao[0], novo_nome)
                lista.selection_set(selecao[0])
            else:
                messagebox.showwarning('Erro', 'Nome inválido ou nome duplicado')

    def editar_servidor():
        for frame in frame_parametros.winfo_children():
            widget = frame.winfo_children()[1] # O segundo widget é sempre o de entrada
            if isinstance(widget, ttk.Entry):
                widget.config(state='normal')
            elif isinstance(widget, ttk.Combobox):
                widget.config(state='readonly')

    def remover_servidor():
        selecao = lista.curselection()
        if selecao:
            if messagebox.askyesno('Confirmar', 'Deseja excluir o servidor?'):
                nome_servidor = lista.get(selecao[0])
                lista.delete(selecao[0])
                projeto.del_servidor(nome_servidor)
                projeto.exibir()
                
                for widget in frame_parametros.winfo_children():
                    widget.destroy()

def conectar_servidores(projeto):
    for server in projeto.servidores:
        nome = server
        conexao = projeto.servidores[server]['Conexão']
        servidor = mh.Servidor(nome, conexao)
        for key, value in projeto.servidores[server].items():
            servidor.config(key, value)
        servidor.conectar()