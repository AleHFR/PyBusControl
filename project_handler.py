########### Preâmbulo ###########
# Imports do python
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox, filedialog

# Imports do projeto
import server_handler as sh
import widget_handler as wh
import custom_widgets as cw

class Projeto:
    def __init__(self, root):
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(side='bottom',fill='both', expand=True)

        self.servidores = {}

    # Função auxiliar
    def exibir(self):
        print("\n########### Informações do Projeto ###########")

        print("\n--- Notebook ---")
        for i, frame in enumerate(self.notebook.winfo_children(), start=1):
            print(f"\n  Frame {i}: {frame.winfo_class()} ({frame})")

            for j, child in enumerate(frame.winfo_children(), start=1):
                widget_info = {
                    "classe": child.winfo_class(),
                    "nome": str(child),
                    "x": child.winfo_x(),
                    "y": child.winfo_y(),
                    "largura": child.winfo_width(),
                    "altura": child.winfo_height(),
                }

                if "text" in child.keys():
                    widget_info["text"] = child.cget("text")
                if "state" in child.keys():
                    widget_info["state"] = child.cget("state")
                if "bg" in child.keys():
                    widget_info["bg"] = child.cget("bg")
                if "fg" in child.keys():
                    widget_info["fg"] = child.cget("fg")

                print(f"    Widget {j}:")
                for k, v in widget_info.items():
                    print(f"      {k}: {v}")

                # Se for um Canvas, lista os itens desenhados
                if widget_info["classe"] == "Canvas":
                    itens = child.find_all()
                    if itens:
                        print("      Itens no Canvas:")
                        for item in itens:
                            tipo = child.type(item)
                            coords = child.coords(item)
                            detalhes = {}
                            for prop in ("fill", "outline", "width", "text", "image", "tags"):
                                try:
                                    val = child.itemcget(item, prop)
                                    if val:
                                        detalhes[prop] = val
                                except:
                                    pass
                            print(f"        - id {item} | tipo={tipo} | coords={coords} | {detalhes}")
                    else:
                        print("      (Canvas vazio)")

        print("\n--- Servidores ---")
        if self.servidores:
            for nome, servidor in self.servidores.items():
                print(f"\n  Servidor: {nome}")
                print(f"    Conexão: {servidor.conexao}")
                print("    Configurações Modbus:")
                for key, value in servidor.modbus.items():
                    print(f"      {key}: {value}")
                print("    Cliente conectado:", getattr(servidor.client, "connected", False))
        else:
            print("  Nenhum servidor cadastrado.")

    #################### Trabalhando com as abas do Notebook ####################
    ########## Adiciona uma aba no notebook ##########
    def add_aba(self, x=None, y=None):
        # Menu de contexto
        def menu_contexto(event):
            context_menu = tk.Menu(self.notebook, tearoff=0)
            context_menu.add_command(label='Mudar nome', command=lambda:self.novoNome_aba())
            context_menu.add_command(label='Alterar tamanho', command=lambda:self.alterar_tamanho_canvas(canvas))
            context_menu.add_command(label='Inserir imagem', command=lambda:self.inserir_imagem(canvas))
            context_menu.add_separator()
            context_menu.add_command(label='Excluir aba', command=lambda: self.del_aba())
            context_menu.post(event.x_root, event.y_root)

        # Trata o tamanho da aba
        if x and y:
            pass
        else:
            x = 1280
            y = 780
        # Pergunta o nome da aba
        nome_aba = cw.perguntarTexto('Nome da aba', 'Insira o nome da aba:', default_text='Nova Aba')

        # Cria a aba
        aba_canvas = ttk.Frame(self.notebook)
        canvas = tk.Canvas(aba_canvas, width=x, height=y, bg='white', borderwidth=0, highlightthickness=0)
        canvas.pack()
        canvas.bind('<Button-3>', lambda event: menu_contexto(event))
        # Adiciona a aba ao notebook
        self.notebook.add(aba_canvas, text=nome_aba)
        self.notebook.select(aba_canvas)
        self.exibir()
    
    ########## Mudar o nome da aba ##########
    def novoNome_aba(self):
        index = self.notebook.select()
        novo_nome = cw.perguntarTexto('Novo nome', 'Insira o novo nome da aba')
        self.notebook.tab(index, text=novo_nome)
        self.exibir()
    
    ########## Excluir um projeto/aba ##########
    def del_aba(self):
        index = self.notebook.select()
        nome_aba = self.notebook.tab(index, 'text')
        if messagebox.askyesno("Confirmar", f"Deseja excluir a aba: '{nome_aba}'?"):
            self.notebook.forget(index)
        self.exibir()
    
    ########## Alterar tamanho do canvas ##########
    def alterar_tamanho_canvas(self, canvas):
        x_atual = canvas.winfo_width()
        y_atual = canvas.winfo_height()

        janela = cw.janelaScroll('Alterar tamanho', geometry=(150,150), resizable=(False, False), scrollbar=False, command=lambda:aplicar(x,y))

        ttk.Label(janela, text='Altura em Pixel:').pack(padx=5, pady=5)
        x = ttk.Entry(janela, width=10)
        x.pack(padx=5, pady=5)
        x.insert(0, x_atual)
        ttk.Label(janela, text='Largura em Pixel:').pack(padx=5, pady=5)
        y = ttk.Entry(janela, width=10)
        y.pack(padx=5, pady=5)
        y.insert(0, y_atual)

        def aplicar(x,y):
            x = x.get()
            y = y.get()
            canvas.config(width=x, height=y)
        self.exibir()

    ########## Inserir imagem no canvas ##########
    def inserir_imagem(self, canvas):
        caminho_imagem = filedialog.askopenfilename(
            filetypes=[('Imagens', '*.jpg;*.png;*.jpeg;*.gif'), ('Todos os arquivos', '*.*')],
            title='Abrir arquivo'
        )
        if not caminho_imagem:
            return
        
        canvas.image_ref = ImageTk.PhotoImage(Image.open(caminho_imagem))
        canvas.create_image(canvas.winfo_width()/2, canvas.winfo_height()/2, anchor='center', image=canvas.image_ref)
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
    def add_widget(self, nome_aba, nome_widget, dados_widget):
        if nome_aba in self.notebook:
            self.notebook[nome_aba]['widgets'][nome_widget] = dados_widget
        self.exibir()

    def config_widget(self, nome_aba, nome_widget, config, novo_valor):
        if config in self.notebook[nome_aba]['widgets'][nome_widget].keys():
            self.notebook[nome_aba]['widgets'][nome_widget][config] = novo_valor
        self.exibir()

    def del_widget(self, nome_aba, nome_widget):
        if nome_aba in self.notebook and 'widgets' in self.notebook[nome_aba]:
            if nome_widget in self.notebook[nome_aba]['widgets']:
                del self.notebook[nome_aba]['widgets'][nome_widget]
        self.exibir()