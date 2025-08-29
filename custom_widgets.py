import tkinter as tk
from tkinter import ttk

#arrumar
def perguntarTexto(title, text, default_text=None):
    # Cria a janela
    janela = tk.Toplevel()
    janela.title(title)
    janela.resizable(False, False)

    # Variável de controle para guardar o texto
    texto_entrada = tk.StringVar(value=default_text if default_text else '')
    
    # Frame pra colocar os componentes
    frame = ttk.Frame(janela)
    frame.pack(padx=5, pady=5)
    ttk.Label(frame, text=text).pack(padx=5, pady=5)
    
    # Associar a entrada à variável de controle
    entrada = ttk.Entry(frame, textvariable=texto_entrada, width=20)
    entrada.pack(padx=5, pady=5)

    # Botão de aplicar
    frame_botao = ttk.Frame(janela)
    frame_botao.pack(side='bottom')
    ttk.Button(frame_botao, text='Ok', command=lambda:janela.destroy()).pack(pady=2)
    entrada.focus_set()

    # Espera a janela ser fechada pra retornar
    janela.wait_window()
    return texto_entrada.get()

def janelaScroll(title, geometry=None, resizable=None, scrollbar=True, command=None, buttonName = None, closeWindow = True):
    # Cria a janela
    janela = tk.Toplevel()
    janela.title(title)
    if geometry:
        janela.geometry(f'{geometry[0]}x{geometry[1]}')
    if resizable:
        janela.resizable(resizable[0], resizable[1])

    # Botão de aplicar
    frame_botao = ttk.Frame(janela)
    frame_botao.pack(side='bottom')
    ttk.Button(frame_botao, text=buttonName if buttonName else 'Ok', command=lambda:ok()).pack(pady=2)

    # Canvas e frame interno
    canvas_interno = tk.Canvas(janela)
    if scrollbar:
        scrollbar = ttk.Scrollbar(janela, orient="vertical", command=canvas_interno.yview)
        canvas_interno.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
    canvas_interno.pack(side="left", fill="both", expand=True)

    frame_interno = ttk.Frame(canvas_interno)
    frame_interno_id = canvas_interno.create_window((0, 0), window=frame_interno, anchor='nw')

    def atualizar_scroll(event):
        canvas_interno.configure(scrollregion=canvas_interno.bbox("all"))
    frame_interno.bind("<Configure>", atualizar_scroll)

    def ajustar_largura_frame(event):
        canvas_interno.itemconfig(frame_interno_id, width=event.width)
    canvas_interno.bind('<Configure>', ajustar_largura_frame)

    def ok():
        if command:command()
        if closeWindow:janela.destroy()

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