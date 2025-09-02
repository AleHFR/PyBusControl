########### Preâmbulo ###########
# Imports do python
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import ImageTk, Image
from tkinter import messagebox, filedialog
from pymodbus.client import AsyncModbusTcpClient

# Imports do projeto
import widget_manager as wm
import custom_widgets as cw
import utils as ut

class Servidor:
    def __init__(self, nome, conexao):
        self.nome = nome
        self.conexao = conexao
        self.client = None
        self.modbus = {}
        if self.conexao == 'TCP':
            self.modbus['IP'] = None
            self.modbus['Porta'] = None
            self.modbus['Timeout (s)'] = None
        elif self.conexao == 'RTU':
            self.modbus['Porta Serial'] = None
            self.modbus['Baudrate'] = None
            self.modbus['Paridade'] = None
            self.modbus['Bytesize'] = None
            self.modbus['Stopbits'] = None
            self.modbus['Timeout (s)'] = None

    def config(self, key, value):
        self.modbus[key] = value

    async def conectar(self):
        if self.conexao == 'TCP':
            client = AsyncModbusTcpClient(
                host=self.modbus['IP'],
                port=self.modbus['Porta'],
                timeout=self.modbus['Timeout (s)']
            )
            self.client = client
            await self.client.connect()
        elif self.conexao == 'RTU':
            None

    async def desconectar(self):
        if self.client and self.client.connected:
            self.client.close()

    async def read_coil(self, address, device_id):
        if self.conexao == 'TCP':
            if self.client.connected:
                valor = await self.client.read_coils(address=address, device_id=device_id, count=1)
                return valor.bits[0]
        elif self.conexao == 'RTU':
            None 

    async def write_coil(self, address, device_id, value):
        if self.conexao == 'TCP':
            if self.client.connected:
                await self.client.write_coil(address=address, device_id=device_id, value=value)
        elif self.conexao == 'RTU':
            None 

    async def read_hreg(self, address, device_id):
        if self.conexao == 'TCP':
            if self.client.connected:
                valor = await self.client.read_holding_registers(address=address, device_id=device_id, count=1)
                return valor.registers[0]
        elif self.conexao == 'RTU':
            None 

    async def write_hreg(self, address, device_id, value):
        if self.conexao == 'TCP':
            if self.client.connected:
                await self.client.write_register(address=address, device_id=device_id, value=value)
        elif self.conexao == 'RTU':
            None

class Widget: 
    def __init__(self, canvas, classe, propriedades, x, y):
        # Salva as infos na classe
        self.canvas = canvas
        self.classe = getattr(ctk, classe)
        self.widget = self.classe(self.canvas, **propriedades)
        self.id = self.canvas.create_window(x, y, window=self.widget)
        self.x = x
        self.y = y
        self.propriedades = propriedades
        self.comando = None
        # Menu de contexto do Widget
        def menuContexto_widget(event):
            context_menu = tk.Menu(self.canvas, tearoff=0)
            context_menu.add_command(label='Mover', command=lambda:self.move(self.id))
            context_menu.add_command(label='Propriedades', command=lambda:wm.propriedades_widget(self))
            context_menu.add_command(label='Excluir', command=lambda:self.delete(self.id))
            context_menu.post(event.x_root, event.y_root)
        # Cria o bind do menu de contexto
        self.widget.bind('<Button-3>', lambda event: menuContexto_widget(event))
        self.return_id()
    
    def return_id(self):
        return self.id

    def config(self, prop, novo_valor):
        if prop == 'image':
            novo_valor = ut.imagem(novo_valor)
        self.widget.config(**{prop: novo_valor})

    def move(self, wid):
        # Dica
        ut.dica('Clique e arraste para mover o widget')
        # posição inicial do item no canvas
        x0, y0 = self.canvas.coords(wid)

        # calcula offset entre clique e posição do widget
        def iniciar(event):
            self.canvas._drag_data = {
                "item": wid,
                "dx": x0 - event.x,
                "dy": y0 - event.y
            }
            # Impede de ser arrastado novamente
            self.canvas.unbind('<Button-1>')
            # ativa arrastar
            self.canvas.bind('<Motion>', mover)
            self.canvas.bind('<ButtonRelease-1>', parar)

        def mover(event):
            # muda a posição do widget
            dx = self.canvas._drag_data["dx"]
            dy = self.canvas._drag_data["dy"]
            pos_x = event.x + dx
            pos_y = event.y + dy
            self.canvas.coords(wid, pos_x, pos_y)
            # Salva a posição no widget
            self.x = pos_x
            self.y = pos_y

        def parar(event):
            # Impede de ser arrastado novamente
            self.canvas.unbind('<Motion>')
            self.canvas.unbind('<ButtonRelease-1>')
            self.canvas._drag_data = {}
            ut.dica()

        # espera o clique esquerdo pra começar arrastar
        self.canvas.bind('<Button-1>', iniciar)

    def delete(self, wid):
        self.widget.destroy()
        self.canvas.delete(wid)

class Aba:
    def __init__(self, notebook):
        self.notebook = notebook
        self.idx = None
        self.tamanho = (0,0) # (x, y)
        self.canvas = None
        self.imagem = ''
        self.widgets = {}
    
    ########## Adiciona uma aba no notebook ##########
    def add(self, x=None, y=None):
        # Menu de contexto
        def menuContexto_aba(event):
            context_menu = tk.Menu(self.notebook, tearoff=0)
            context_menu.add_command(label='Adicionar widget', command=lambda:wm.adicionar_widget(self))
            context_menu.add_separator()
            context_menu.add_command(label='Excluir aba', command=lambda: self.delete())
            context_menu.post(event.x_root, event.y_root)
        # Tamanho padrão
        x = x or 1280
        y = y or 780
        # Cria frame/canvas
        aba_canvas = ttk.Frame(self.notebook)
        canvas = tk.Canvas(aba_canvas, width=x, height=y, bg='white', borderwidth=0, highlightthickness=0)
        canvas.pack()
        # Altera as infos
        self.tamanho = (x, y)
        self.canvas = canvas
        # Bind menu contexto
        # canvas.bind('<Button-3>', lambda event: menuContexto_aba(event))
        # Retorna o frame
        return aba_canvas

    ########## Mudar o nome da aba ##########
    def novoNome(self, novo_nome):
        self.notebook.tab(self.idx, text=novo_nome)
    
    ########## Alterar tamanho da aba (do canvas) ##########
    def novoTamanho(self, novo_tamanho):
        x, y = novo_tamanho
        self.canvas.config(width=x, height=y)
        self.tamanho = (x, y)

    ########## Inserir imagem na aba (no canvas) ##########
    def novaImagem(self, caminho_imagem=None):
        if not caminho_imagem:
            return
        self.canvas.image_ref = ImageTk.PhotoImage(Image.open(caminho_imagem))
        self.canvas.create_image(
            self.canvas.winfo_width()/2,
            self.canvas.winfo_height()/2,
            image=self.canvas.image_ref,
            anchor='center')
        self.imagem = caminho_imagem

    ########## Excluir um projeto/aba ##########
    def delete(self):
        self.notebook.forget(self.idx)

class Projeto:
    def __init__(self, root):
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(side='bottom',fill='both', expand=True)
        self.abas = {}
        self.servidores = {}

    #################### Funções auxiliares ####################
    ########## exibe o projeto no terminal ##########
    def exibir(self):
        print("\n" + "#"*20 + " ESTADO ATUAL DO PROJETO " + "#"*20)

        # Exibe os servidores
        if self.servidores:
            print("\n>>> SERVIDORES:")
            for nome, servidor in self.servidores.items():
                print(f"  - Nome: {nome}")
                if hasattr(servidor, 'conexao'):
                    print(f"    - Conexão: {servidor.conexao}")
                if hasattr(servidor, 'modbus'):
                    if servidor.modbus:
                        print("    - Configurações:")
                        for config, valor in servidor.modbus.items():
                            print(f"      • {config}: {valor}")
                    else:
                        print("    - Configurações: Nenhuma")
        else:
            print("\n>>> Nenhum servidor adicionado.")

        # Exibe as abas
        if self.abas:
            print("\n>>> ABAS:")
            for nome, aba in self.abas.items():
                print(f"  - Nome: {nome}")
                print(f"    - Tamanho: {aba.tamanho[0]}x{aba.tamanho[1]} pixels")
                print(f"    - Imagem de fundo: {aba.imagem if aba.imagem else 'Não'}")

                # Exibe os widgets da aba
                if aba.widgets:
                    print("    - Widgets:")
                    # Varrer todos os parâmetros de cada widget
                    for wid, widget_obj in aba.widgets.items():
                        print(f"      • ID={wid} | Classe={widget_obj.classe.__name__}")
                        print(f"        - Posição: ({widget_obj.x}, {widget_obj.y})")
                        if widget_obj.propriedades:
                            print("        - Propriedades:")
                            for prop, valor in widget_obj.propriedades.items():
                                print(f"          - {prop}: {valor}")
                else:
                    print("    - Widgets: Nenhum")
        else:
            print("\n>>> Nenhuma aba adicionada.")
        
        print("#"*65 + "\n")
    
    ########## encontra alguma coisa ##########
    def find(self, coisa, id_widget=None):
        index = self.notebook.select()
        nome_aba = self.notebook.tab(index, 'text')
        aba = self.abas[nome_aba]
        canvas = aba.canvas
        if coisa == 'id_aba':
            return index
        elif coisa == 'nome_aba':
            return nome_aba
        elif coisa == 'aba':
            return aba
        elif coisa == 'canvas':
            return canvas
        elif coisa == 'widget' and id_widget:
            return aba.widgets[id_widget]

    #################### Trabalhando com as abas do Notebook ####################
    ########## Adiciona uma aba no notebook ##########
    def add_aba(self, nome, x=None, y=None):
        if nome in self.abas.keys():
            messagebox.showerror('Erro', 'Já existe uma aba com esse nome.')
            return
        # Cria objeto Aba
        aba = Aba(self.notebook)
        frame_aba = aba.add(x, y)
        # Adiciona no notebook
        self.notebook.add(frame_aba, text=nome)
        self.notebook.select(frame_aba)
        aba.idx = self.notebook.select()
        # Guarda no projeto
        self.abas[nome] = aba
        self.exibir()
    
    def config_aba(self, aba, chave, valor):
        if chave == 'nome':
            # Verifica se já existe uma aba com esse nome  e se o nome é diferente do atual
            nome_antigo = self.find('nome_aba')
            if valor != nome_antigo and valor in self.abas.keys():
                messagebox.showerror('Erro', 'Já existe uma aba com esse nome.')
                return
            else:
                aba.novoNome(valor)
                self.abas[valor] = self.abas.pop(nome_antigo)
        elif chave == 'tamanho':
            aba.novoTamanho(valor)
        elif chave == 'imagem':
            aba.novaImagem(valor)
        self.exibir()
    
    def del_aba(self, aba):
        nome_aba = self.notebook.tab(aba.idx, 'text')
        if messagebox.askyesno("Confirmar", f"Deseja excluir a aba: '{nome_aba}'?"):
            aba.delete()
            del self.abas[nome_aba]
        self.exibir()

    #################### Trabalhando com os Servidores ####################
    ########## Adicionar um servidor ##########
    def add_servidor(self, nome_servidor, conexao, configs):
        if nome_servidor not in self.servidores.keys():
            servidor = Servidor(nome_servidor, conexao)
            for key, value in configs.items():
                servidor.config(key, value)
            self.servidores[nome_servidor] = servidor
        self.exibir()
    
    ########## Conecta ao servidor ##########
    def concetar_servidor(self, nome_servidor):
        if nome_servidor in self.servidores.keys():
            self.servidores[nome_servidor].conectar()
        self.exibir()

    ########## Mudar o nome do servidor ##########
    def novoNome_servidor(self, nome_servidor, novo_nome_servidor):
        if novo_nome_servidor not in self.servidores.keys():
            self.servidores[novo_nome_servidor] = self.servidores[nome_servidor]
            del self.servidores[nome_servidor]
        self.exibir()

    ########## Configurar o servidor ##########
    def config_servidor(self, nome_servidor, config, valor):
        if config in self.servidores[nome_servidor].modbus.keys():
            servidor = self.servidores[nome_servidor]
            servidor.config(config, valor)
        self.exibir()

    ########## Deletar um servidor ##########
    def del_servidor(self, nome_servidor):
        if nome_servidor in self.servidores:
            del self.servidores[nome_servidor]
        self.exibir()

    ####################  Trabalhando com os Widgets das abas ####################
    ########## Adicionar um widget ##########
    def add_widget(self, classe, dados_widget, x, y):
        # Encontra aba atual
        nome_aba = self.find('nome_aba')
        canvas_atual = self.find('canvas')
        # Adiciona o widget na visualização
        widget = Widget(canvas_atual, classe, dados_widget, x, y)
        # Salva no projeto
        self.abas[nome_aba].widgets[widget.id] = widget
        self.exibir()
        return widget

    ########## Configurar o widget ##########
    def config_widget(self, wid, prop, novo_valor):
        # Encontra aba atual
        nome_aba = self.find('nome_aba')
        canvas_atual = self.find('canvas')
        # Altera o widget na visualização
        widget = canvas_atual.nametowidget(canvas_atual.itemcget(wid, 'window'))
        widget.config(**{prop: novo_valor})
        # Altera o widget no projeto
        widget = self.abas[nome_aba].widgets[wid]
        widget.propriedades[prop] = novo_valor
        self.exibir()

    ########## Deletar um widget ##########
    def del_widget(self, wid):
        canvas_atual = self.find('canvas')
        widget = canvas_atual.nametowidget(canvas_atual.itemcget(wid, 'window'))
        widget.destroy()
        canvas_atual.delete(wid)
        self.exibir()