import os
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog
from CTkColorPicker import AskColor
from TkToolTip import ToolTip

def imagem(caminho: str, tamanho: tuple = None, para_tk: bool = False):    
    if os.path.exists(caminho) and os.path.isfile(caminho):
        imagem_pil = Image.open(caminho)
    else:
        return None

    # Se a imagem for para um widget do Tkinter padrão (como o Canvas)
    if para_tk:
        if tamanho:
            imagem_pil = imagem_pil.resize(tamanho)
        return ImageTk.PhotoImage(imagem_pil)

    # Se for para um widget do CustomTkinter (padrão)
    else:
        return ctk.CTkImage(light_image=imagem_pil, 
                            dark_image=imagem_pil, 
                            size=tamanho if tamanho else (imagem_pil.width, imagem_pil.height))

class customClickTooltip(ctk.CTkToplevel):
    def __init__(self, master, text="Tooltip", **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.text = text
        self.visible = False
        
        self.withdraw()
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        # self.configure(fg_color="#363636", bg_color="#363636")

        self.label = ctk.CTkLabel(self, text=self.text, fg_color="transparent")
        self.label.pack(padx=8, pady=4)

    def show_tooltip(self, event=None):
        if not self.visible:
            self.visible = True
            # Mostra a tooltip e a posiciona
            self.deiconify()
            self.update_position(event)
            
            # Liga o evento de movimento e clique para seguir e esconder a tooltip
            self.master.bind("<Motion>", self.update_position)
            self.master.bind("<Button-1>", self.hide_tooltip)
            self.master.bind("<Button-3>", self.hide_tooltip)
            
            # Se for um evento de botão, desabilita a propagação para evitar o ocultamento imediato
            if event and isinstance(event.widget, ctk.CTkButton):
                self.after(1, lambda: event.widget.unbind("<Button-1>"))

    def hide_tooltip(self, event=None):
        if self.visible:
            # Desliga os eventos de rastreamento do mouse e de clique
            self.master.unbind("<Motion>")
            self.master.unbind("<Button-1>")
            self.master.unbind("<Button-3>")
            
            # Esconde a tooltip
            self.withdraw()
            self.visible = False
            self.destroy()

    def update_position(self, event):
        x = self.master.winfo_pointerx() + 15
        y = self.master.winfo_pointery() + 15
        self.geometry(f"+{x}+{y}")
        self.update_idletasks()

class customIconButton(ctk.CTkButton):
    def __init__(self, root, icone:str, tooltip:str=None, tamanho:tuple=(15, 15), **kwargs):
        caminho_completo = os.path.join(os.path.dirname(__file__), "assets", icone)
        self.icone = imagem(caminho_completo, tamanho)
        super().__init__(root, text="", width=0, fg_color="#FFFFFF", hover_color="gray", image=self.icone, **kwargs)
        ToolTip(self, text=tooltip, font=("Arial", 10), delay=0.5)

class customMenu(tk.Menu): # arrumar
    def __init__(self, root, **kwargs):
        # bg = ctk.ThemeManager.theme["CTkLabel"]["fg_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme[ref]["fg_color"][1]
        # fg = ctk.ThemeManager.theme["CTkLabel"]["text_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme[ref]["text_color"][1]
        # activebg = ctk.ThemeManager.theme["CTkButton"]["hover_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme[ref]["hover_color"][1]
        # activefg = ctk.ThemeManager.theme["CTkButton"]["text_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme[ref]["text_color"][1]

        super().__init__(root, tearoff=0, **kwargs)

class customLabelFrame(ttk.LabelFrame): # arrumar
    def __init__(self, root, **kwargs):
        # Adapta ao tema do customtkinter
        # bg = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1]
        # fg = ctk.ThemeManager.theme["CTkLabel"]["text_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme["CTkLabel"]["text_color"][1]

        # # Cria estilo personalizado
        # style = ttk.Style()
        # style.configure("Custom.TLabelframe", background=bg, foreground=fg)
        # style.configure("Custom.TLabelframe.Label", background=bg, foreground=fg)

        # Inicializa o LabelFrame com o estilo
        super().__init__(root, **kwargs)

class customNotebook(ttk.Notebook): # arrumar
    def __init__(self, root, **kwargs):
        # Adapta ao tema do customtkinter
        bg = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1]
        fg = ctk.ThemeManager.theme["CTkLabel"]["text_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme["CTkLabel"]["text_color"][1]

        # Cria estilo personalizado
        style = ttk.Style()
        style.configure("Custom.TNotebook", background=bg, foreground=fg)
        style.configure("Custom.TNotebook.Tab", background=bg, foreground=fg)

        # Inicializa o Notebook com o estilo
        super().__init__(root, **kwargs)

class customSelecionaCor(ctk.CTkButton):
    def __init__(self, root, cor_inicial:str=None, button_name:str=None, **kwargs):
        self.cor_atual = cor_inicial if cor_inicial else "#ffffff"
        self.button_name = button_name if button_name else self.cor_atual
        super().__init__(root, text=self.button_name, command=self.buscar, **kwargs)
        self.configure(fg_color=self.cor_atual)

    def buscar(self):
        self.cor_atual = AskColor(initial_color=self.cor_atual, title="Selecione a cor").get()
        self.configure(fg_color=self.cor_atual, text=self.button_name if self.button_name else self.cor_atual)

    def get(self):
        return self.cor_atual

class customBuscaArquivo(ctk.CTkFrame):
    def __init__(self, root, valor_inicial:str=None, button_name:str=None, **kwargs):
        super().__init__(root, fg_color="transparent")
        self.valor_inicial = valor_inicial if valor_inicial else None
        self.button_name = button_name if button_name else "..."

        self.botao = ctk.CTkButton(self, text=self.button_name, width=25, command=self.buscar)
        self.botao.pack(padx=(5,0), side="right")
        self.botao.cget("width")

        self.entry = ctk.CTkEntry(self, placeholder_text="Selecione um arquivo...", **kwargs)
        self.entry.pack(fill="x", side="left")
        if self.valor_inicial:
            self.entry.insert(0, self.valor_inicial)

    def buscar(self):
        arquivo = filedialog.askopenfilename()
        self.entry.delete(0, ctk.END)
        self.entry.insert(0, arquivo)

    def get(self):
        return self.entry.get()

class customSpinbox(ctk.CTkFrame):
    def __init__(self, master, min_value=None, max_value=None, step=1, initial_value=0, width=100, **kwargs):
        super().__init__(master, fg_color="transparent", width=width, **kwargs)
        
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = initial_value
        
        # Botão de decremento
        self.decrement_button = ctk.CTkButton(self, text="-", width=25, command=self.decrement)
        self.decrement_button.pack(side="left")
        
        # Entrada de texto para o valor
        self.entry = ctk.CTkEntry(self, width=width-60)
        self.entry.pack(side="left", anchor="center", padx=5)
        self.entry.insert(0, str(self.value))
        
        # Botão de incremento
        self.increment_button = ctk.CTkButton(self, text="+", width=25, command=self.increment)
        self.increment_button.pack(side="left")
        
    def increment(self):
        try:
            current_value = int(self.entry.get())
            new_value = current_value + self.step
            if self.max_value and new_value >= self.max_value:self.value = self.max_value
            else:self.value = new_value
            self.entry.delete(0, ctk.END)
            self.entry.insert(0, str(self.value))
        except ValueError:
            # Lida com o caso de entrada não-numérica
            pass

    def decrement(self):
        try:
            current_value = int(self.entry.get())
            new_value = current_value - self.step
            if self.min_value and new_value <= self.min_value:self.value = self.min_value
            else:self.value = new_value
            self.entry.delete(0, ctk.END)
            self.entry.insert(0, str(self.value))
        except ValueError:
            pass

    def get(self):
        try:
            return int(self.entry.get())
        except ValueError:
            return None

class customDialog(ctk.CTkToplevel):
    def __init__(self, title:str, message:str, tipo:str=None, **kwargs):
        super().__init__(tk._default_root, **kwargs)
        self.geometry("300x150")
        self.resizable(False, False)
        self.title(title)

        # Modal
        self.transient(tk._default_root)
        self.grab_set()

        # Variáveis
        self.message = message
        self.result = False

        for t in ["yes_no", "entry"]:
            metodo = getattr(self, t, None)
            if metodo and t == tipo:
                metodo()
                break
        self.wait_window()

    def yes_no(self):
        def on_yes():
            self.result = True
            self.destroy()

        def on_no():
            self.result = False
            self.destroy()

        label = ctk.CTkLabel(self, text=self.message, font=("", 14), wraplength=250)
        label.pack(expand=True, fill="both", padx=20, pady=20)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=(0, 5))

        yes_button = ctk.CTkButton(button_frame, text="Sim", command=on_yes, width=100)
        yes_button.pack(side="left", padx=10)

        no_button = ctk.CTkButton(button_frame, text="Não", command=on_no, width=100)
        no_button.pack(side="left", padx=10)

        self.bind("<Return>", lambda event: on_yes())
        self.bind("<Escape>", lambda event: on_no())
    
    def entry(self):
        def on_ok():
            self.result = self.entry.get()
            self.destroy()

        label = ctk.CTkLabel(self, text=self.message, font=("", 14), wraplength=250)
        label.pack(expand=True, fill="both", padx=20, pady=20)

        self.entry = ctk.CTkEntry(self)
        self.entry.pack(pady=5)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=5)

        ok_button = ctk.CTkButton(button_frame, text="OK", command=on_ok, width=100)
        ok_button.pack(side="left", padx=10)

        self.bind("<Return>", lambda event: on_ok())
        self.bind("<Escape>", lambda event: self.destroy())

class customTopLevel(ctk.CTkToplevel):
    def __init__(self, title, geometry=None, resizable=None, scrollbar=True, Notebook=False, buttonSet=True, command=None, buttonName=None, **kwargs):
        super().__init__(tk._default_root, **kwargs)
        self.title(title)
        self.transient(tk._default_root)
        self.grab_set()
        # Frame interno
        self.frame_interno = ctk.CTkScrollableFrame(self, fg_color="transparent") if scrollbar else ctk.CTkFrame(self, fg_color="transparent")
        self.frame_interno.pack(side="top", fill="both", expand=True, padx=10, pady=5)
        # Notebook
        if Notebook:
            self.notebook = customNotebook(self.frame_interno)
            self.notebook.pack(fill="both", expand=True)

        # Variáveis 
        self.itens = {}

        # Tamanho e redimensionamento
        self.geometry(f"{geometry[0]}x{geometry[1]}" if geometry else "300x150")
        if resizable:
            self.resizable(resizable[0], resizable[1])
        else:
            self.resizable(True, True)
        # Botão
        if buttonSet:
            self.frame_botao = ctk.CTkFrame(self, fg_color="transparent")
            self.frame_botao.pack(side="bottom", fill="x", padx=10, pady=5)
            def aplicar():
                if command:
                    command()
            ctk.CTkButton(self.frame_botao, text=buttonName if buttonName else "Aplicar", command=aplicar).pack(side="left", padx=5, expand=True)
    
    def addTopLabel(self, text:str, root=None):
        # Verifica se tem um frame externo, se não usa o interno
        root = root if root else self.frame_interno
        # Simplesmente uma label no topo
        ctk.CTkLabel(root, text=text).pack(fill="x", side="top", pady=5)

    def addItem(self, nome:str, item, tamanho:int=200, valor_inicial=None, valores:list=None, root=None):
        # Verifica se tem um frame externo, se não usa o interno
        root = root if root else self.frame_interno
        # Cria um frame temporário
        frame_temp = ctk.CTkFrame(root, fg_color="transparent")
        frame_temp.pack(fill="x", pady=5)
        # Inclui o nome do item
        ctk.CTkLabel(frame_temp, text=nome).pack(side="left")
        # Se item for uma classe, cria
        if isinstance(item, type):
            item = item(frame_temp, width=tamanho)
        item.pack(side="right")

        # Se houver valores de lista, insere no item
        if valores:item.configure(values=valores, state="readonly")

        # Trata a atribuição de acordo com o tipo SE houver um valor inicial
        if valor_inicial:
            if isinstance(item, ctk.CTkFrame):
                item.entry.delete(0, ctk.END)
                item.entry.insert(0, valor_inicial)
            else:
                if isinstance(item, (ctk.CTkEntry, ctk.CTkTextbox)):
                    item.delete(0, ctk.END)
                    item.insert(0, valor_inicial)
                elif isinstance(item, (ctk.CTkComboBox, ctk.CTkOptionMenu, ctk.CTkCheckBox, ctk.CTkSwitch)):
                    item.set(valor_inicial)
                elif isinstance(item, ctk.CTkButton):
                    item.configure(text=valor_inicial, fg_color=valor_inicial)
            
        # Salva no dicionário
        self.itens[nome] = item
        # retorna o item
        return item

    def addTupleItem(self, nome:str, item_1, item_2, tamanho:int=200, valor_inicial_1=None, valores_1:list=None, valor_inicial_2=None, valores_2:list=None, root=None):
        # Verifica se tem um frame externo, se não usa o interno
        root = root if root else self.frame_interno
        # Cria um frame temporário
        frame_temp = ctk.CTkFrame(root, fg_color="transparent")
        frame_temp.pack(fill="x", pady=5)
        # Inclui o nomde do item
        ctk.CTkLabel(frame_temp, text=nome).pack(side="left")
        # Cria o item de acordo com o tipo dinamicamente
        item_2 = item_2(frame_temp, width=tamanho/2-3) # item 2 primeiro pq a ordem de pack é a ordem de apresentação
        item_2.pack(side="right", padx=(3,0))
        item_1 = item_1(frame_temp, width=tamanho/2-3)
        item_1.pack(side="right", padx=(0,3))

        # Se houver valores de lista, insere no item
        valores = {item_1:valores_1, item_2:valores_2}
        for item, valor in valores.items():
            if valor:
                item.configure(values=valor)
        
        # Trata a atribuição de acordo com o tipo SE houver um valor inicial
        itens = {item_1:valor_inicial_1, item_2:valor_inicial_2} # Dicionário pra simplificar a escrita
        for item, valor in itens.items():
            if not valor: # Se n tem valor inicial pula
                continue
            if isinstance(item, ctk.CTkFrame):
                item.entry.delete(0, ctk.END)
                item.entry.insert(0, valor)
            else:
                if isinstance(item, (ctk.CTkEntry, ctk.CTkTextbox)):
                    item.delete(0, ctk.END)
                    item.insert(0, valor)
                elif isinstance(item, (ctk.CTkComboBox, ctk.CTkOptionMenu, ctk.CTkCheckBox, ctk.CTkSwitch)):
                    item.set(valor)

        # Salva no dicionário
        self.itens[nome] = [item_1, item_2]
        # retorna o item
        return 

    def addTab(self, title, **kwargs):
        frame = ctk.CTkFrame(self.notebook, fg_color="transparent")
        self.notebook.add(frame, text=title, **kwargs)
        self.notebook.select(frame)
        return frame