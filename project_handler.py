########### Preâmbulo ###########
# Imports do python
from tkinter import ttk
from tkinter import messagebox

# Imports do projeto
import handlers.server as sh
import handlers.widget as wh
import handlers.notebook as nh

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
        aba = nh.Aba(self.notebook)
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
            servidor = sh.Servidor(nome_servidor, conexao)
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
        widget = wh.Widget(canvas_atual, classe, dados_widget, x, y)
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