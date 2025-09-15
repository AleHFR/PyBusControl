########### Preâmbulo ###########
# Imports do python
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from pymodbus.client import AsyncModbusTcpClient, AsyncModbusSerialClient

# Imports do projeto
import drivers.plc_driver as plc
import managers.widget_manager as wm
import interface.personalized as ps

# Classes axiliares pra trabalhar com o projeto
class Atibuitos:
    def __init__(self):
        self.classe = None
        self.item = None
        self.canvas = None
        self.imagem = None

class Widget:
    def __init__(self, classe:str, posicao:tuple, propriedades:dict):
        self.atributos = Atibuitos()
        self.classe = classe
        self.posicao = posicao
        self.propriedades = propriedades
        self.comando = None

class Aba:
    def __init__(self, tamanho:tuple):
        self.atributos = Atibuitos()
        self.tamanho = tamanho
        self.caminho_imagem = None
        self.widgets = {}

# Classe principal do projeto
class Projeto:
    def __init__(self, root):
        self.notebook = ps.customNotebook(root)
        self.notebook.pack(side='bottom', fill='both', expand=True)
        self.abas = {}
        self.servidores = {}

    def exibir(self):
        def print_propriedades_em_colunas(propriedades, colunas=5):
            # Converte o dicionário em uma lista de tuplas (chave, valor)
            itens = list(propriedades.items())
            num_itens = len(itens)
            
            # Calcula o número de linhas necessário
            num_linhas = (num_itens + colunas - 1) // colunas
            
            # Cria uma lista de colunas, onde cada coluna é uma sublista de itens
            colunas_de_itens = [itens[i * num_linhas : (i + 1) * num_linhas] for i in range(colunas)]
            
            # Armazena as larguras máximas de cada coluna para alinhamento
            larguras_colunas = []
            for coluna in colunas_de_itens:
                max_chave = 0
                max_valor = 0
                for chave, valor in coluna:
                    if len(str(chave)) > max_chave:
                        max_chave = len(str(chave))
                    if len(str(valor)) > max_valor:
                        max_valor = len(str(valor))
                larguras_colunas.append((max_chave, max_valor))

            # Itera sobre as linhas e imprime as propriedades em colunas
            for linha in range(num_linhas):
                linha_impressao = ''
                for i in range(colunas):
                    if linha < len(colunas_de_itens[i]):
                        chave, valor = colunas_de_itens[i][linha]
                        
                        # Formata a string de impressão com alinhamento dinâmico
                        prop_formatada = f"{str(chave).ljust(larguras_colunas[i][0])} : {str(valor).ljust(larguras_colunas[i][1])}"
                        linha_impressao += f" {prop_formatada.ljust(larguras_colunas[i][0] + larguras_colunas[i][1] + 3)}"
                    else:
                        # Se a coluna não tiver mais itens, preenche o espaço
                        espaco_vazio = larguras_colunas[i][0] + larguras_colunas[i][1] + 3
                        linha_impressao += ' ' * espaco_vazio
                print(linha_impressao)
            
        print('--- Visão Geral do Projeto ---\n')

        # Exibe as abas e seus widgets
        print('### Abas ###')
        if not self.abas:
            print('Nenhuma aba criada.')
        else:
            for nome_aba, aba_obj in self.abas.items():
                print(f'-> Nome da Aba: {nome_aba}')
                print(f'   - Tamanho: {aba_obj.tamanho}')
                print(f'   - Caminho da Imagem: {aba_obj.caminho_imagem}')
                print(f'   - Widgets:')
                if not aba_obj.widgets:
                    print('     Nenhum widget nesta aba.')
                else:
                    for widget_id, widget_obj in aba_obj.widgets.items():
                        print(f'     -> ID do Widget: {widget_id}')
                        print(f'        - Classe: {widget_obj.classe}')
                        print(f'        - Posição: {widget_obj.posicao}')
                        if widget_obj.comando:
                            print(f'        - Comando Associado: {widget_obj.comando}')
                        print(f'        - Propriedades:')
                        print_propriedades_em_colunas(widget_obj.propriedades, colunas=3)

        print('\n' + '-'*30 + '\n')

        # Exibe os servidores e seus detalhes
        print('### Servidores ###')
        if not self.servidores:
            print('Nenhum servidor configurado.')
        else:
            for nome_servidor, server_obj in self.servidores.items():
                print(f'-> Nome do Servidor: {nome_servidor}')
                print(f'   - Conexão: {server_obj.conexao}')
                print(f'   - Status: {server_obj.status}')
                # Exibe os parâmetros específicos para cada tipo de conexão
                if server_obj.conexao == 'TCP':
                    print(f'   - IP: {server_obj.ip}')
                    print(f'   - Porta: {server_obj.porta}')
                    print(f'   - Timeout: {server_obj.timeout}s')
                elif server_obj.conexao == 'RTU':
                    print(f'   - ID: {server_obj.id}')
                    print(f'   - Porta Serial: {server_obj.porta_serial}')
                    print(f'   - Baudrate: {server_obj.baudrate}')
                    print(f'   - Paridade: {server_obj.parity}')
                    print(f'   - Timeout: {server_obj.timeout}s')

    #################### Trabalhando com as abas do Notebook ####################
    ########## Adiciona uma aba no notebook ##########
    def add_aba(self, nome):
        if nome in self.abas.keys():
            messagebox.showerror('Erro', 'Já existe uma aba com esse nome.')
            return
        # Tamanho padrão
        x, y = 1280, 780
        # Adiciona uma aba
        frame = ctk.CTkFrame(self.notebook)
        canvas = tk.Canvas(frame, width=x, height=y, bg='white', borderwidth=2)
        canvas.pack()
        self.notebook.add(frame, text=nome)
        self.notebook.select(frame)
        # Guarda no projeto
        aba = Aba(tamanho=(x, y))
        aba.atributos.canvas = canvas
        aba.atributos.item = frame
        self.abas[nome] = aba

    ########## Configura uma aba no notebook ##########
    def config_aba(self, chave, valor):
        frame = self.notebook.select()
        nome_aba = self.notebook.tab(frame, 'text')
        aba = self.abas[nome_aba]
        
        if chave == 'nome':
            # Verifica se já existe uma aba com esse nome e se o nome é diferente do atual
            if valor != nome_aba and valor in self.abas.keys():
                messagebox.showerror('Erro', 'Já existe uma aba com esse nome.')
                return
            else:
                self.notebook.tab(frame, text=valor)
                self.abas[valor] = self.abas.pop(nome_aba)

        elif chave == 'tamanho':
            x, y = valor
            aba.atributos.canvas.config(width=x, height=y)

        elif chave == 'imagem':
            if valor not in [None, '', ' ']:
                return
            aba.caminho_imagem = valor
            aba.atributos.imagem = ps.imagem(valor)
            canvas = aba.atributos.canvas
            canvas.image_ref = aba.atributos.imagem
            canvas.create_image(
                canvas.winfo_width()/2,
                canvas.winfo_height()/2,
                image=canvas.image_ref,
                anchor='center'
            )

    ########## Deleta uma aba no notebook ##########
    def del_aba(self):
        frame = self.notebook.select()
        nome_aba = self.notebook.tab(frame, 'text')
        self.notebook.forget(frame)
        del self.abas[nome_aba]

    #################### Trabalhando com os Servidores ####################
    ########## Adicionar um servidor ##########
    def add_servidor(self, nome_servidor, conexao, configs):
        if nome_servidor not in self.servidores.keys():
            servidor = plc.Plc(conexao, configs)
            self.servidores[nome_servidor] = servidor

    ########## Mudar o nome do servidor ##########
    def novoNome_servidor(self, nome_servidor, novo_nome_servidor):
        if novo_nome_servidor not in self.servidores.keys():
            self.servidores[novo_nome_servidor] = self.servidores[nome_servidor]
            del self.servidores[nome_servidor]

    ########## Configurar o servidor ##########
    def config_servidor(self, nome_servidor, config, valor):
        servidor = self.servidores[nome_servidor]
        setattr(servidor, config, valor)

    ########## Deletar um servidor ##########
    def del_servidor(self, nome_servidor):
        if nome_servidor in self.servidores:
            del self.servidores[nome_servidor]

    ####################  Trabalhando com os Widgets das abas ####################
    ########## Adicionar um widget ##########
    def add_widget(self, classe, propriedades, x, y):
        # Encontra os atributos necessários
        frame = self.notebook.select()
        nome_aba = self.notebook.tab(frame, 'text')
        aba = self.abas[nome_aba]
        canvas = aba.atributos.canvas
        # Menu de contexto do Widget
        def menuContexto_widget(event):
            context_menu = ps.customMenu(canvas)
            context_menu.add_command(label='Mover', command=lambda:self.move_widget(wid))
            context_menu.add_command(label='Propriedades', command=lambda:wm.propriedades(self, wid))
            context_menu.add_command(label='Excluir', command=lambda:self.del_widget(wid))
            context_menu.post(event.x_root, event.y_root)
        # Adiciona o widget na visualização
        widgetTk = classe(canvas, **propriedades).get()
        widgetTk.bind('<Button-3>', lambda event: menuContexto_widget(event)) # Cria o bind do menu de contexto
        wid = canvas.create_window(x, y, window=widgetTk)
        # Salva no projeto
        classetk = widgetTk.__class__.__name__
        widget = Widget(classe=classetk, posicao=(x, y), propriedades=propriedades)
        widget.atributos.item = widgetTk
        widget.atributos.classe = classe
        aba.widgets[wid] = widget
        # Retorna o id do widget
        return wid

    ########## Configurar o widget ##########
    def config_widget(self, wid, prop, novo_valor):
        # Encontra os atributos necessários
        frame = self.notebook.select()
        nome_aba = self.notebook.tab(frame, 'text')
        aba = self.abas[nome_aba]
        widget = aba.widgets[wid]
        item = widget.atributos.item
        # Altera o widget na visualização
        if prop == 'image' and novo_valor not in [None, '', ' ']: # Trata o valor se for imagem
            imagem = ps.imagem(novo_valor)
            item.configure(image=imagem)
            widget.atributos.image = imagem # Salva a imagem
        elif prop == 'font': # Trata o valor se for fonte
            fonte = ctk.CTkFont(family=novo_valor[0], size=int(novo_valor[1]))
            item.configure(font=fonte)
        else:
            item.configure(**{prop:novo_valor})
        # Altera o widget no projeto
        widget.propriedades[prop] = novo_valor

    ########## Move o widget ##########
    def move_widget(self, wid):
        # Encontra os atributos necessários
        frame = self.notebook.select()
        nome_aba = self.notebook.tab(frame, 'text')
        aba = self.abas[nome_aba]
        canvas = aba.atributos.canvas
        # posição inicial do item no canvas
        x0, y0 = canvas.coords(wid)
        # Dica
        dica = ps.ClickTooltip(canvas, text='Clique e arraste para mover o widget')
        dica.show_tooltip()

        # calcula offset entre clique e posição do widget
        def iniciar(event):
            dica.hide_tooltip()
            canvas._drag_data = {
                "item": wid,
                "dx": x0 - event.x,
                "dy": y0 - event.y
            }
            # Impede de ser arrastado novamente
            canvas.unbind('<Button-1>')
            # ativa arrastar
            canvas.bind('<Motion>', mover)
            canvas.bind('<ButtonRelease-1>', parar)

        def mover(event):
            # muda a posição do widget
            dx = canvas._drag_data["dx"]
            dy = canvas._drag_data["dy"]
            pos_x = event.x + dx
            pos_y = event.y + dy
            canvas.coords(wid, pos_x, pos_y)
            # Salva a posição no widget
            self.x = pos_x
            self.y = pos_y

        def parar(event):
            # Impede de ser arrastado novamente
            canvas.unbind('<Motion>')
            canvas.unbind('<ButtonRelease-1>')
            canvas._drag_data = {}

        # espera o clique esquerdo pra começar arrastar
        canvas.bind('<Button-1>', iniciar)
        
    ########## Deletar um widget ##########
    def del_widget(self, wid):
        # Encontra os atributos necessários
        frame = self.notebook.select()
        nome_aba = self.notebook.tab(frame, 'text')
        aba = self.abas[nome_aba]
        widget = aba.widgets[wid].atributos.item
        canvas = aba.atributos.canvas
        widget.destroy()
        canvas.delete(wid)
        