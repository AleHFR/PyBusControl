import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

#arrumar
def ask_yes_no(title: str, message: str) -> bool:
    dialog = ctk.CTkToplevel()
    dialog.title(title)
    dialog.geometry("350x180")
    dialog.resizable(False, False)
    
    # Faz o diálogo ser modal
    dialog.transient()
    dialog.grab_set()

    # Variável para armazenar o resultado
    result = False
    
    def on_yes():
        nonlocal result
        result = True
        dialog.destroy()

    def on_no():
        nonlocal result
        result = False
        dialog.destroy()

    label = ctk.CTkLabel(dialog, text=message, font=("", 14), wraplength=320)
    label.pack(expand=True, fill="both", padx=20, pady=20)

    button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
    button_frame.pack(pady=(0,5))

    yes_button = ctk.CTkButton(button_frame, text="Sim", command=on_yes, width=100)
    yes_button.pack(side="left", padx=10)

    no_button = ctk.CTkButton(button_frame, text="Não", command=on_no, width=100)
    no_button.pack(side="left", padx=10)
    
    # Espera até que a janela de diálogo seja fechada (por um dos botões)
    dialog.wait_window()
    
    return result

def janelaScroll(title, geometry=None, resizable=None, scrollbar=None, button_set=True, command=None, buttonName = None, closeWindow = True):
    # Cria a janela
    janela = ctk.CTkToplevel() # Usa a raiz padrão do CustomTkinter
    janela.title(title)
    janela.transient()
    janela.grab_set()

    if geometry:
        janela.geometry(f'{geometry[0]}x{geometry[1]}')
    if resizable:
        janela.resizable(resizable[0], resizable[1])
    else:
        janela.resizable(True, True) # Padrão mais flexível

    def ok():
        if command:
            command()
        if closeWindow:
            janela.destroy()

    if button_set:
        frame_botao = ctk.CTkFrame(janela, fg_color="transparent")
        frame_botao.pack(side='bottom', fill='x', padx=10, pady=(5, 10))

        ctk.CTkButton(
            frame_botao,
            text=buttonName if buttonName else 'Ok',
            command=ok
        ).pack()

    frame_interno = None
    if scrollbar:frame_interno = ctk.CTkScrollableFrame(janela, label_text="")
    else:frame_interno = ctk.CTkFrame(janela)
    frame_interno.pack(side='top', fill='both', expand=True, padx=10, pady=(10, 5))

    return frame_interno

def listaDinamica(root, values, start_value=None, height_entry=None, width_entry=None, height_listbox=None, width_listbox=None):
    values_orig = values[:]  # cópia para evitar alterar lista original

    entry = ttk.Entry(root, width=width_entry if width_entry else 20)
    if height_entry:
        entry.config(height=height_entry)
    if width_entry:
        entry.config(width=width_entry)
    if start_value:
        entry.insert(0, start_value)

    scrollbar = ttk.Scrollbar(root, orient="vertical")
    listbox = tk.Listbox(root, yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    def mostrar_lista():
        if listbox.size() > 0:
            x, y, w, h = entry.winfo_x(), entry.winfo_y(), entry.winfo_width(), entry.winfo_height()

            # Ajusta dimensões conforme parâmetros
            w_listbox = width_listbox if width_listbox else w - scrollbar.winfo_reqwidth()
            h_listbox = height_listbox if height_listbox else 100
            w_scroll = scrollbar.winfo_reqwidth()

            listbox.place(x=x, y=y+h, width=w_listbox, height=h_listbox)
            scrollbar.place(x=x + w_listbox, y=y+h, width=w_scroll, height=h_listbox)

            listbox.lift(), scrollbar.lift()
        else:
            esconder_lista()

    def esconder_lista(*_):
        listbox.place_forget()
        scrollbar.place_forget()

    def atualizar_lista(*_):
        typed = entry.get().lower()
        filtradas = [v for v in values_orig if typed in v.lower()] if typed else values_orig
        listbox.delete(0, tk.END)
        [listbox.insert(tk.END, o) for o in filtradas]
        mostrar_lista()

    def selecionar_item(*_):
        if listbox.curselection():
            entry.delete(0, tk.END)
            entry.insert(0, listbox.get(listbox.curselection()[0]))
        esconder_lista()

    entry.bind("<KeyRelease>", atualizar_lista)
    entry.bind("<Button-1>", atualizar_lista)
    listbox.bind("<ButtonRelease-1>", selecionar_item)

    # Fecha ao clicar fora
    root.bind("<Button-1>", lambda e: esconder_lista() if e.widget != entry else None)

    return entry