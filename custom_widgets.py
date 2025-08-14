import tkinter as tk
from tkinter import ttk

def listaDinamica(root, values, start_value, height_entry=None, width_entry=None, height_listbox=None, width_listbox=None):
    values_orig = values[:]  # cópia para evitar alterar lista original

    entry = ttk.Entry(root, width=width_entry if width_entry else 20)
    if height_entry:
        entry.config(height=height_entry)
    if width_entry:
        entry.config(width=width_entry)
    if start_value:
        entry.insert(0, start_value)

    scrollbar = tk.Scrollbar(root, orient="vertical")
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