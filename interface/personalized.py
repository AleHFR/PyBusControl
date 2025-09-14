import os
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image

# arrumar
class customMenu(tk.Menu):
    def __init__(self, root, **kwargs):
        # bg = ctk.ThemeManager.theme["CTkLabel"]["fg_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme[ref]["fg_color"][1]
        # fg = ctk.ThemeManager.theme["CTkLabel"]["text_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme[ref]["text_color"][1]
        # activebg = ctk.ThemeManager.theme["CTkButton"]["hover_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme[ref]["hover_color"][1]
        # activefg = ctk.ThemeManager.theme["CTkButton"]["text_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme[ref]["text_color"][1]

        super().__init__(root, tearoff=0, **kwargs)

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
    def __init__(self, title: str, message: str, **kwargs):
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

        yes_button = ctk.CTkButton(button_frame, text="Sim", command=lambda:on_yes(), width=100)
        yes_button.pack(side="left", padx=10)

        no_button = ctk.CTkButton(button_frame, text="Não", command=lambda:on_no(), width=100)
        no_button.pack(side="left", padx=10)
        
        self.wait_window()
        return self.result

class customTopLevel(ctk.CTkToplevel):
    def __init__(self, title, geometry=None, resizable=None, scrollbar=True, buttonSet=True, command=None, buttonName=None, **kwargs):
        super().__init__(tk._default_root, **kwargs)
        self.title(title)
        self.transient(tk._default_root)
        self.grab_set()

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
            frame_botao.pack(side='bottom', fill='x', padx=10, pady=(5, 10))
            def aplicar():
                if command:
                    command()
            ctk.CTkButton(frame_botao, text=buttonName if buttonName else 'Aplicar', command=aplicar).pack()

        # Frame interno
        self.frame_interno = ctk.CTkScrollableFrame(self, fg_color="transparent") if scrollbar else ctk.CTkFrame(self, fg_color="transparent")
        self.frame_interno.pack(side='top', fill='both', expand=True, padx=10, pady=(10, 5))
    
    def addTopLabel(self, text:str, root=None, **kargs):
        # Verifica se tem um frame externo, se não usa o interno
        root = root if root else self.frame_interno
        # Simplesmente uma label no topo
        ctk.CTkLabel(root, text=text, **kargs).pack(padx=5, pady=5, fill='x', side='top')

    def addItem(self, nome:str, item, tamanho:int=None, valor_inicial=None, root=None, **kargs):
        # Verifica se tem um frame externo, se não usa o interno
        root = root if root else self.frame_interno
        # Cria um frame temporário
        frame_temp = ctk.CTkFrame(root, fg_color="transparent")
        frame_temp.pack(fill='x', pady=2, padx=2)
        # Inclui o nomde do item
        ctk.CTkLabel(frame_temp, text=nome).pack(side='left')
        # Cria o item de acordo com o tipo
        tamanho = tamanho if tamanho else 200
        item = item(frame_temp, width=tamanho, **kargs)
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
    
    def addButtonItem(self, nome:str, comando, tamanho:int=None, valor_inicial=None, root=None, **kargs):
        # Verifica se tem um frame externo, se não usa o interno
        root = root if root else self.frame_interno
        # Cria um frame temporário
        frame_temp = ctk.CTkFrame(root, fg_color="transparent")
        frame_temp.pack(fill='x', pady=2, padx=2)
        # Inclui o nomde do item
        ctk.CTkLabel(frame_temp, text=nome).pack(side='left')
        # Cria o botão
        ctk.CTkButton(frame_temp, text='...', width=30, command=lambda:comando()).pack(side='right', padx=(5,0))
        # Cria uma entry com botão do lado
        tamanho = tamanho if tamanho else 200
        item = ctk.CTkEntry(frame_temp, width=tamanho-35, **kargs)
        item.pack(side='right')
        # Insere o valor
        item.insert(0, valor_inicial)
        # Salva no dicionário
        self.itens[nome] = item
        # retorna o item
        return item

class customNotebookTopLevel(customTopLevel):
    def __init__(self, title, geometry=None, resizable=None, buttonSet=True, command=None, buttonName=None, **kwargs):
        super().__init__(title, geometry=geometry, resizable=resizable, scrollbar=True, buttonSet=buttonSet, command=command, buttonName=buttonName, **kwargs)
        self.notebook = ttk.Notebook(self.frame_interno)
        self.notebook.pack(fill='both', expand=True)

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

def imagem(nome, tamanho_icone=None):
    caminho_icone = os.path.join(os.path.dirname(__file__), 'assets', nome)
    image = Image.open(caminho_icone)
    if tamanho_icone:image = ctk.CTkImage(light_image=image, dark_image=image, size=tamanho_icone)
    else: image = ctk.CTkImage(light_image=image, dark_image=image)
    return image