########### Preâmbulo ###########
# Imports do python
import tkinter as tk
import customtkinter as ctk

# Imports do projeto
import widget_manager as wm
import custom_widgets as cw

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
            context_menu = tk.Menu(self.canvas,
                               bg=ctk.ThemeManager.theme["CTkButton"]["fg_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme["CTkButton"]["fg_color"][1],
                               fg=ctk.ThemeManager.theme["CTkButton"]["text_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme["CTkButton"]["text_color"][1],
                               activebackground=ctk.ThemeManager.theme["CTkButton"]["hover_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme["CTkButton"]["hover_color"][1],
                               activeforeground=ctk.ThemeManager.theme["CTkButton"]["text_color"][0] if ctk.get_appearance_mode() == "Light" else ctk.ThemeManager.theme["CTkButton"]["text_color"][1],
                               tearoff=0)
            context_menu.add_command(label='Mover', command=lambda:self.move(self.id))
            context_menu.add_command(label='Função', command=lambda:wm.funcao(self))
            context_menu.add_command(label='Visual', command=lambda:wm.visual_widget(self))
            context_menu.add_command(label='Excluir', command=lambda:self.delete(self.id))
            context_menu.post(event.x_root, event.y_root)
        # Cria o bind do menu de contexto
        self.widget.bind('<Button-3>', lambda event: menuContexto_widget(event))
        self.return_id()
    
    def return_id(self):
        return self.id

    def config(self, prop, novo_valor):
        if prop == 'image':
            novo_valor = cw.imagem(novo_valor)
        self.widget.configure(**{prop: novo_valor})

    def move(self, wid):
        # Dica
        cw.dica('Clique e arraste para mover o widget')
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
            cw.dica()

        # espera o clique esquerdo pra começar arrastar
        self.canvas.bind('<Button-1>', iniciar)

    def delete(self, wid):
        self.widget.destroy()
        self.canvas.delete(wid)