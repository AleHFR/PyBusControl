import tkinter as tk
from tkinter import ttk

def menuPropriedades(title, geometry=None, resizable=None, command=None):
    # Cria a janela de propriedades
    janela = tk.Toplevel()
    janela.title(title)
    if geometry:
        janela.geometry(f'{geometry[0]}x{geometry[1]}')
    if resizable:
        janela.resizable(resizable[0], resizable[1])

    # Botão de aplicar
    frame_botao = ttk.Frame(janela)
    frame_botao.pack(side='bottom', fill='x')
    ttk.Button(frame_botao, text='Aplicar', command=command if command else None).pack(pady=2)

    # Frame principal para organizar canvas e botão
    frame_principal = ttk.Frame(janela)
    frame_principal.pack(fill="both")

    # Canvas e frame interno para scrollbar
    canvas_interno = tk.Canvas(frame_principal)
    scrollbar = ttk.Scrollbar(frame_principal, orient="vertical", command=canvas_interno.yview)
    canvas_interno.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas_interno.pack(side="left", fill="both")

    frame_interno = ttk.Frame(canvas_interno)
    frame_interno.pack(side="top", fill="both")
    canvas_interno.create_window((0, 0), window=frame_interno, anchor='nw')

    def atualizar_scroll(event):
        canvas_interno.configure(scrollregion=canvas_interno.bbox("all"))
    frame_interno.bind("<Configure>", atualizar_scroll)
    frame_interno.bind("<Button2-Motion>", atualizar_scroll)

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