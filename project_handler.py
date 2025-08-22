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
        if nome_aba in self.dados['notebook']:
            messagebox.showerror("Erro", f"A aba '{nome_aba}' ja existe.")
            return False
        else:
            self.dados['notebook'][nome_aba] = {
                'x': x,
                'y': y,
                'imagem': '',
                'widgets': {},
            }
            return True
        
    def mudar_nome_aba(self, nome_aba, novo_nome_aba):
        if novo_nome_aba in self.dados['notebook']:
            messagebox.showerror("Erro", f"Já existe uma aba com o nome'{nome_aba}'.")
            return False
        else:
            self.dados['notebook'][novo_nome_aba] = self.dados['notebook'][nome_aba]
            del self.dados['notebook'][nome_aba]
            return True

    def editar_aba(self, nome_aba, chave, novo_valor):
        if chave in self.dados['notebook'][nome_aba].keys():
            self.dados['notebook'][nome_aba][chave] = novo_valor

    def del_aba(self, nome_aba):
        del self.dados['notebook'][nome_aba]

    ########## Trabalhando com os Widgets das abas ##########
    def add_widget(self, nome_aba, nome_widget, dados_widget):
        if nome_aba in self.dados['notebook']:
            # Adiciona o widget
            self.dados['notebook'][nome_aba]['widgets'][nome_widget] = dados_widget
            print(f"Widget '{nome_widget}' adicionado/atualizado na aba '{nome_aba}'.")
        else:
            print(f"Erro: A aba '{nome_aba}' não existe.")

    def del_widget(self, nome_aba, nome_widget):
        if nome_aba in self.dados['notebook'] and 'widgets' in self.dados['notebook'][nome_aba]:
            if nome_widget in self.dados['notebook'][nome_aba]['widgets']:
                del self.dados['notebook'][nome_aba]['widgets'][nome_widget]
                print(f"Widget '{nome_widget}' removido da aba '{nome_aba}'.")
            else:
                print(f"Erro: O widget '{nome_widget}' não foi encontrado na aba '{nome_aba}'.")
        else:
            print(f"Erro: A aba '{nome_aba}' ou o seu dicionário de widgets não existe.")

    ########## Trabalhando com os Servidores ##########
    def add_servidor(self, nome_servidor, valor):
        if nome_servidor in self.dados['servidores']:
            print(f"Erro: O servidor '{nome_servidor}' ja existe.")
            return
        else:
            self.dados['servidores'][nome_servidor] = valor
        
    def del_servidor(self, nome_servidor):
        if nome_servidor not in self.dados['servidores']:
            print(f"Erro: O servidor '{nome_servidor}' nao existe.")
            return
        else:
            del self.dados['servidores'][nome_servidor]