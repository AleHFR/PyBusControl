import os
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog

# arrumar
class customMenu(tk.Menu):
    def __init__(self, root, **kwargs):
        # bg = ctk.ThemeManager.theme["CTkLabel"]["fg_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme[ref]["fg_color"][1]
        # fg = ctk.ThemeManager.theme["CTkLabel"]["text_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme[ref]["text_color"][1]
        # activebg = ctk.ThemeManager.theme["CTkButton"]["hover_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme[ref]["hover_color"][1]
        # activefg = ctk.ThemeManager.theme["CTkButton"]["text_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme[ref]["text_color"][1]

        super().__init__(root, tearoff=0, **kwargs)
# arrumar
class customLabelFrame(ttk.LabelFrame):
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
# arrumar
class customNotebook(ttk.Notebook):
    def __init__(self, root, **kwargs):
        # # Adapta ao tema do customtkinter
        # bg = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1]
        # fg = ctk.ThemeManager.theme["CTkLabel"]["text_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme["CTkLabel"]["text_color"][1]

        # # Cria estilo personalizado
        # style = ttk.Style()
        # style.configure("Custom.TNotebook", background=bg, foreground=fg)
        # style.configure("Custom.TNotebook.Tab", background=bg, foreground=fg)

        # Inicializa o Notebook com o estilo
        super().__init__(root, **kwargs)

class customBuscaArquivo(ctk.CTkFrame):
    def __init__(self, root, tamanho:int=200, valor_inicial:str=None, button_name:str=None, **kwargs):
        super().__init__(root, fg_color="transparent")
        self.valor_inicial = valor_inicial if valor_inicial else 'Selecione o arquivo...'
        self.button_name = button_name if button_name else '...'

        self.botao = ctk.CTkButton(self, text=self.button_name, width=25, command=self.buscar)
        self.botao.pack(padx=(5,0), side='right')

        self.entry = ctk.CTkEntry(self, width=tamanho - 30, **kwargs)
        self.entry.insert(0, self.valor_inicial)
        self.entry.pack(fill='x', side='left')

    def buscar(self):
        arquivo = filedialog.askopenfilename()
        self.entry.delete(0, ctk.END)
        self.entry.insert(0, arquivo)

    def get(self):
        return self.entry.get()

class customSpinbox(ctk.CTkFrame):
    def __init__(self, master, min_value=0, max_value=100, step=1, initial_value=0, width=100, **kwargs):
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
        self.entry.pack(side="left", anchor='center', padx=5)
        self.entry.insert(0, str(self.value))
        
        # Botão de incremento
        self.increment_button = ctk.CTkButton(self, text="+", width=25, command=self.increment)
        self.increment_button.pack(side="left")
        
    def increment(self):
        try:
            current_value = int(self.entry.get())
            new_value = current_value + self.step
            if new_value <= self.max_value:
                self.value = new_value
                self.entry.delete(0, ctk.END)
                self.entry.insert(0, str(self.value))
        except ValueError:
            # Lida com o caso de entrada não-numérica
            pass

    def decrement(self):
        try:
            current_value = int(self.entry.get())
            new_value = current_value - self.step
            if new_value >= self.min_value:
                self.value = new_value
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

        self._build_()

    def _build_(self):
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
        
        self.wait_window()
        return self.result

class customTopLevel(ctk.CTkToplevel):
    def __init__(self, title, geometry=None, resizable=None, scrollbar=True, Notebook=False, buttonSet=True, command=None, buttonName=None, **kwargs):
        super().__init__(tk._default_root, **kwargs)
        self.title(title)
        self.transient(tk._default_root)
        self.grab_set()
        # Frame interno
        self.frame_interno = ctk.CTkScrollableFrame(self, fg_color="transparent") if scrollbar else ctk.CTkFrame(self, fg_color="transparent")
        self.frame_interno.pack(side='top', fill='both', expand=True, padx=10, pady=10)
        # Notebook
        if Notebook:
            self.notebook = customNotebook(self.frame_interno)
            self.notebook.pack(fill='both', expand=True)

        # Variáveis 
        self.itens = {}

        # Tamanho e redimensionamento
        self.geometry(f'{geometry[0]}x{geometry[1]}' if geometry else '300x150')
        if resizable:
            self.resizable(resizable[0], resizable[1])
        else:
            self.resizable(True, True)
        # Botão
        if buttonSet:
            frame_botao = ctk.CTkFrame(self, fg_color="transparent")
            frame_botao.pack(side='bottom', fill='x', padx=10, pady=10)
            def aplicar():
                if command:
                    command()
            ctk.CTkButton(frame_botao, text=buttonName if buttonName else 'Aplicar', command=aplicar).pack()
    
    def addTopLabel(self, text:str, root=None):
        # Verifica se tem um frame externo, se não usa o interno
        root = root if root else self.frame_interno
        # Simplesmente uma label no topo
        ctk.CTkLabel(root, text=text).pack(fill='x', side='top', pady=5)

    def addItem(self, nome:str, item, tamanho:int=200, valor_inicial=None, root=None, **kwargs):
        # Verifica se tem um frame externo, se não usa o interno
        root = root if root else self.frame_interno
        # Cria um frame temporário
        frame_temp = ctk.CTkFrame(root, fg_color="transparent")
        frame_temp.pack(fill='x', pady=5)
        # Inclui o nomde do item
        ctk.CTkLabel(frame_temp, text=nome).pack(side='left')
        try: # Cria o item de acordo com o tipo
            item = item(frame_temp, width=tamanho, **kwargs)
            item.pack(side='right')
        except: # Se já existir, só coloca
            item.pack(side='right')
        # Trata a atribuição de acordo com o tipo
        if isinstance(item, (ctk.CTkEntry, ctk.CTkTextbox)):
            item.delete(0, ctk.END)
            if valor_inicial is not None:
                item.insert(0, valor_inicial)
        elif isinstance(item, (ctk.CTkComboBox, ctk.CTkOptionMenu, ctk.CTkCheckBox, ctk.CTkSwitch)):
            if valor_inicial is not None:
                item.set(valor_inicial)
        # Salva no dicionário
        self.itens[nome] = item
        # retorna o item
        return item

    def addTupleItem(self, nome:str, item_1, item_2, tamanho:int=200, valor_inicial_1=None, valor_inicial_2=None, root=None):
        # Verifica se tem um frame externo, se não usa o interno
        root = root if root else self.frame_interno
        # Cria um frame temporário
        frame_temp = ctk.CTkFrame(root, fg_color="transparent")
        frame_temp.pack(fill='x', pady=5)
        # Inclui o nomde do item
        ctk.CTkLabel(frame_temp, text=nome).pack(side='left')
        # Cria o item de acordo com o tipo dinamicamente
        items = {item_1:valor_inicial_1, item_2:valor_inicial_2}
        for item, valor_inicial in items.items():
            item = item(frame_temp, width=tamanho)
            item.pack(side='right', )
            # Trata a atribuição de acordo com o tipo
            if isinstance(item, (ctk.CTkEntry, ctk.CTkTextbox)):
                item.delete(0, ctk.END)
                if valor_inicial is not None:
                    item.insert(0, valor_inicial)
            elif isinstance(item, (ctk.CTkComboBox, ctk.CTkOptionMenu, ctk.CTkCheckBox, ctk.CTkSwitch)):
                if valor_inicial is not None:
                    item.set(valor_inicial)

            # Salva no dicionário
            self.itens[nome] = item
        # retorna o item
        return 

    def addTab(self, title, **kwargs):
        frame = ctk.CTkFrame(self.notebook, fg_color="transparent")
        self.notebook.add(frame, text=title, **kwargs)
        self.notebook.select(frame)
        return frame
    
class ClickTooltip(ctk.CTkToplevel):
    def __init__(self, master, text="Tooltip", **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.text = text
        self.visible = False
        
        self.withdraw()
        self.overrideredirect(True)
        self.attributes('-topmost', True)
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

def imagem(caminho:str, tamanho_icone:tuple[int, int] = None):
    caminho_completo = None
    if os.path.isabs(caminho):
        caminho_completo = caminho
    else:
        caminho_completo = os.path.join(os.path.dirname(__file__), 'assets', caminho)
    imagem = Image.open(caminho_completo)
    if tamanho_icone:imagem = ctk.CTkImage(light_image=imagem, dark_image=imagem, size=tamanho_icone)
    else: imagem = ctk.CTkImage(light_image=imagem, dark_image=imagem)
    return imagem