########### Preâmbulo ###########
# Imports do python
from tkinter import messagebox

class Projeto:
    def __init__(self):
        self.dados = {
            'notebook': {},
            'servidores': {},
        }

    # Funções auxiliares
    def limpar(self):
        self.dados['notebook'] = {}
        self.dados['servidores'] = {}
    
    def exibir(self):
        print("\n--- Informações do Projeto ---")
        for chave, valor in self.dados.items():
            print(f"  {chave}: {valor}")
        print("------------------------------\n")

    ########## Trabalhando com as abas do Notebook ##########
    def add_aba(self, nome_aba, x, y):
        if nome_aba not in self.dados['notebook']:
            self.dados['notebook'][nome_aba] = {
                'x': x,
                'y': y,
                'imagem': '',
                'widgets': {},
            }
            return True
        else:
            return False
        
    def novoNome_aba(self, nome_aba, novo_nome_aba):
        if novo_nome_aba not in self.dados['notebook']:
            self.dados['notebook'][novo_nome_aba] = self.dados['notebook'][nome_aba]
            del self.dados['notebook'][nome_aba]
            return True
        else:
            return False

    def config_aba(self, nome_aba, chave, novo_valor):
        if chave in self.dados['notebook'][nome_aba].keys():
            self.dados['notebook'][nome_aba][chave] = novo_valor

    def del_aba(self, nome_aba):
        del self.dados['notebook'][nome_aba]

    ########## Trabalhando com os Widgets das abas ##########
    def add_widget(self, nome_aba, nome_widget, dados_widget):
        if nome_aba in self.dados['notebook']:
            self.dados['notebook'][nome_aba]['widgets'][nome_widget] = dados_widget

    def config_widget(self, nome_aba, nome_widget, config, novo_valor):
        if config in self.dados['notebook'][nome_aba]['widgets'][nome_widget].keys():
            self.dados['notebook'][nome_aba]['widgets'][nome_widget][config] = novo_valor

    def del_widget(self, nome_aba, nome_widget):
        if nome_aba in self.dados['notebook'] and 'widgets' in self.dados['notebook'][nome_aba]:
            if nome_widget in self.dados['notebook'][nome_aba]['widgets']:
                del self.dados['notebook'][nome_aba]['widgets'][nome_widget]

    #################### Trabalhando com os Servidores ####################
    def add_servidor(self, nome_servidor, configs):
        if nome_servidor not in self.dados['servidores']:
            self.dados['servidores'][nome_servidor] = configs

    def novoNome_servidor(self, nome_servidor, novo_nome_servidor):
        if novo_nome_servidor not in self.dados['servidores']:
            self.dados['servidores'][novo_nome_servidor] = self.dados['servidores'].pop(nome_servidor)

    def config_servidor(self, nome_servidor, config, valor):
        if config in self.dados['servidores'][nome_servidor].keys():
            self.dados['servidores'][nome_servidor][config] = valor
        
    def del_servidor(self, nome_servidor):
        if nome_servidor in self.dados['servidores']:
            del self.dados['servidores'][nome_servidor]