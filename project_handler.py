########### Preâmbulo ###########
# Imports do python
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
from pymodbus.client import AsyncModbusTcpClient, AsyncModbusSerialClient

# Imports do projeto
import widget_manager as wm
import custom_widgets as cw

class Projeto:
    def __init__(self, root):
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(side='bottom', fill='both', expand=True)
        self.abas = {}
        self.servidores = {}
    
    def exibir(self):
        print(self.abas)
        print(self.servidores)

    #################### Trabalhando com as abas do Notebook ####################
    ########## Adiciona uma aba no notebook ##########
    def add_aba(self, nome):
        if nome in self.abas.keys():
            messagebox.showerror('Erro', 'Já existe uma aba com esse nome.')
            return
        # Tamanho padrão
        x = 1280
        y = 780
        # Adiciona uma aba
        frame = ctk.CTkFrame(self.notebook)
        canvas = tk.Canvas(frame, width=x, height=y, bg='white', borderwidth=0, highlightthickness=0)
        canvas.pack()
        self.notebook.add(frame, text=nome)
        self.notebook.select(frame)
        # Guarda no projeto
        self.abas[nome] = {'canvas': canvas, 'widgets': {}, 'tamanho': (x, y), 'imagem': ''}

    ########## Configura uma aba no notebook ##########
    def config_aba(self, chave, valor):
        aba = self.notebook.select()
        if chave == 'nome':
            # Verifica se já existe uma aba com esse nome  e se o nome é diferente do atual
            aba = self.notebook.select()
            nome_antigo = self.notebook.tab(aba, 'text')
            if valor != nome_antigo and valor in self.abas.keys():
                messagebox.showerror('Erro', 'Já existe uma aba com esse nome.')
                return
            else:
                self.notebook.tab(aba, text=valor)
                self.abas[valor] = self.abas.pop(nome_antigo)
        elif chave == 'tamanho':
            nome = self.notebook.tab(aba, 'text')
            x, y = valor
            self.abas[nome]['canvas'].config(width=x, height=y)
        elif chave == 'imagem':
            if not valor:
                return
            nome = self.notebook.tab(aba, 'text')
            self.abas[nome]['imagem'] = valor
            imagem = cw.imagem(valor)
            self.abas[nome]['canvas'].image_ref = imagem
            self.abas[nome]['canvas'].create_image(self.abas[nome]['canvas'].winfo_width()/2,
                                                  self.abas[nome]['canvas'].winfo_height()/2,
                                                  image=self.abas[nome]['canvas'].image_ref,
                                                  anchor='center')

    ########## Deleta uma aba no notebook ##########
    def del_aba(self):
        aba = self.notebook.select()
        nome_aba = self.notebook.tab(aba, 'text')
        self.notebook.forget(aba)
        del self.abas[nome_aba]

    #################### Trabalhando com os Servidores ####################
    ########## Adicionar um servidor ##########
    def add_servidor(self, nome_servidor, conexao, configs):
        if nome_servidor not in self.servidores.keys():
            self.servidores[nome_servidor] = {'conexao':conexao, 'client':None, 'configs':configs}

    ########## Conecta a um servidor ##########
    def conectar_servidor(self, nome_servidor):
        if nome_servidor in self.servidores.keys():
            servidor = self.servidores[nome_servidor]
            configs = servidor['configs']
            conectar()
            async def conectar():
                if servidor['conexao'] == 'TCP':
                    servidor['client'] = AsyncModbusTcpClient(
                        host=configs['IP'],
                        port=configs['Porta'],
                        timeout=int(configs['Timeout (s)'])
                    )
                elif servidor['conexao'] == 'RTU':
                    servidor['client'] = AsyncModbusSerialClient(
                        port=configs['Porta Serial'],
                        baudrate=int(configs['Baudrate']),
                        bytesize=int(configs['Bytesize']),
                        parity=configs['Paridade'],
                        stopbits=int(configs['Stopbits']),
                        timeout=int(configs['Timeout (s)'])
                    )
                await servidor['client'].connect()
                return servidor['client'].connected
    
    ########## Desconecta um servidor ##########
    def desconectar_servidor(self, nome_servidor):
        servidor = self.servidores[nome_servidor]
        client = servidor['client']
        desconectar_servidor()
        async def desconectar_servidor():
            if client and client.connected:
                client.close()

    def command_servidor(self, nome_servidor, commando, address, value=None):
        servidor = self.servidores[nome_servidor]
        client = servidor['client']
        configs = servidor['configs']
        if commando == 'Read_Single_Coil':
            Read_Single_Coil()
        elif commando == 'Write_Single_Coil':
            Write_Single_Coil()
        elif commando == 'Read_Single_Register':
            Read_Single_Register()
        elif commando == 'Write_Single_Register':
            Write_Single_Register()
        
        async def Read_Single_Coil():
            if client and client.connected:
                valor = await client.read_coils(address=address, slave=configs['ID'], count=1)
                if not valor.isError():
                    return valor.bits[0]
            return None

        async def Write_Single_Coil():
            if client and client.connected:
                await client.write_coil(address=address, slave=configs['ID'], value=value)
                return True
            return False

        async def Read_Single_Register():
            if client and client.connected:
                valor = await client.read_holding_registers(address=address, slave=configs['ID'], count=1)
                if not valor.isError():
                    return valor.registers[0]
            return None

        async def Write_Single_Register():
            if client and client.connected:
                await client.write_register(address=address, slave=configs['ID'], value=value)
                return True
            return False

    ########## Mudar o nome do servidor ##########
    def novoNome_servidor(self, nome_servidor, novo_nome_servidor):
        if novo_nome_servidor not in self.servidores.keys():
            self.servidores[novo_nome_servidor] = self.servidores[nome_servidor]
            del self.servidores[nome_servidor]

    ########## Configurar o servidor ##########
    def config_servidor(self, nome_servidor, config, valor):
        servidor = self.servidores[nome_servidor]
        configs = servidor['configs']
        if config in configs.keys():
            configs[config] = valor

    ########## Deletar um servidor ##########
    def del_servidor(self, nome_servidor):
        if nome_servidor in self.servidores:
            del self.servidores[nome_servidor]

    ####################  Trabalhando com os Widgets das abas ####################
    ########## Adicionar um widget ##########
    def add_widget(self, classe, propriedades, x, y):
        # Encontra aba atual
        nome_aba = self.notebook.tab(self.notebook.select(), 'text')
        canvas_atual = self.abas[nome_aba]['canvas']
        # Menu de contexto do Widget
        def menuContexto_widget(event):
            context_menu = cw.customMenu(canvas_atual)
            context_menu.add_command(label='Mover', command=lambda:self.move_widget(wid))
            context_menu.add_command(label='Comando', command=lambda:wm.comando(self, wid))
            context_menu.add_command(label='Visual', command=lambda:wm.visual_widget(self, wid))
            context_menu.add_command(label='Excluir', command=lambda:self.del_widget(wid))
            context_menu.post(event.x_root, event.y_root)
        # Adiciona o widget na visualização
        classeCTk = getattr(ctk, classe)
        widget = classeCTk(canvas_atual, **propriedades)
        wid = canvas_atual.create_window(x, y, window=widget)
        # Cria o bind do menu de contexto
        widget.bind('<Button-3>', lambda event: menuContexto_widget(event))
        # Salva no projeto
        self.abas[nome_aba]['widgets'][wid] = {'item':widget, 'classe':classe, 'x':x, 'y':y, 'comando':None, 'propriedades':propriedades}
        
        return wid

    ########## Configurar o widget ##########
    def config_widget(self, wid, prop, novo_valor):
        print(f'Configurar widget {wid}: {prop} = {novo_valor}')
        # Encontra aba atual
        nome_aba = self.notebook.tab(self.notebook.select(), 'text')
        # Altera o widget no projeto
        props = self.abas[nome_aba]['widgets'][wid]['propriedades']
        props[prop] = novo_valor
        # Altera o widget na visualização
        widget = self.abas[nome_aba]['widgets'][wid]['item']
        if prop == 'image': # Trata o valor se for imagem
            novo_valor = cw.imagem(novo_valor)
        widget.configure(**props)

    ########## Move o widget ##########
    def move_widget(self, wid):
        # Dica
        cw.dica('Clique e arraste para mover o widget')
        # posição inicial do item no canvas
        nome_aba = self.notebook.tab(self.notebook.select(), 'text')
        canvas_atual = self.abas[nome_aba]['canvas']
        x0, y0 = canvas_atual.coords(wid)

        # calcula offset entre clique e posição do widget
        def iniciar(event):
            canvas_atual._drag_data = {
                "item": wid,
                "dx": x0 - event.x,
                "dy": y0 - event.y
            }
            # Impede de ser arrastado novamente
            canvas_atual.unbind('<Button-1>')
            # ativa arrastar
            canvas_atual.bind('<Motion>', mover)
            canvas_atual.bind('<ButtonRelease-1>', parar)

        def mover(event):
            # muda a posição do widget
            dx = canvas_atual._drag_data["dx"]
            dy = canvas_atual._drag_data["dy"]
            pos_x = event.x + dx
            pos_y = event.y + dy
            canvas_atual.coords(wid, pos_x, pos_y)
            # Salva a posição no widget
            self.x = pos_x
            self.y = pos_y

        def parar(event):
            # Impede de ser arrastado novamente
            canvas_atual.unbind('<Motion>')
            canvas_atual.unbind('<ButtonRelease-1>')
            canvas_atual._drag_data = {}
            cw.dica()

        # espera o clique esquerdo pra começar arrastar
        canvas_atual.bind('<Button-1>', iniciar)
        

    ########## Deletar um widget ##########
    def del_widget(self, wid):
        nome_aba = self.notebook.tab(self.notebook.select(), 'text')
        canvas_atual = self.abas[nome_aba]['canvas']
        widget = self.abas[nome_aba]['widgets'][wid]['item']
        widget.destroy()
        canvas_atual.delete(wid)
        