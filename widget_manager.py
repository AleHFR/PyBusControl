########### Preâmbulo ###########
# Imports do python
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Imports do projeto
import custom_widgets as cw

# Variáveis Locais
tipos_widgets = {
    'Texto': {
        'classe': 'Label',
        'propriedades': {
            'text': 'Texto',
            'image': '',
        }
    },
    'Botão': {
        'classe': 'Button',
        'função': '',
        'propriedades': {
            'text': 'Botão',
            'width': 5,
            'image': '',
        }
    },
    'Indicador': {
        'classe': 'Label',
        'função': '',
        'propriedades': {
            'text': '0.00',
        }
    },
    'Slider': {
        'classe': 'Scale',
        'função': '',
        'propriedades': {
            'from_': 0,
            'to': 100,
            'orient': 'horizontal',
            'length': 100,
        }
    },
}

#################### Adicionar um widget ####################
def adicionar_widget(projeto):
    if not projeto.notebook.tabs():
        messagebox.showerror('Erro', 'Nenhuma aba existente')
        return

    janela = cw.janelaScroll('Adicionar Widget', resizable=(False, False), command=lambda: click())

    frame_classe = ttk.Frame(janela)
    frame_classe.pack(padx=5, pady=5, fill='x')
    ttk.Label(frame_classe, text='Widget:').pack(side='left')

    combo_classe = ttk.Combobox(frame_classe, values=list(tipos_widgets.keys()), state='readonly')
    combo_classe.pack(side='right')

    frame_propriedades = ttk.LabelFrame(janela, text='Propriedades')
    frame_propriedades.pack(padx=5, pady=5, fill='both')

    propriedades = {}
    canvas_atual = None
    tipo_selecionado = tk.StringVar()

    # Atualiza propriedades quando mudar o tipo
    def atualizar_classe():
        # Limpa tudo
        for widget in frame_propriedades.winfo_children():
            widget.destroy()
        propriedades.clear()
        # Pega o novo tipo
        tipo = combo_classe.get()
        tipo_selecionado.set(tipo)
        # Escrever dinamicamente
        for key, value in tipos_widgets[tipo]['propriedades'].items():
            ttk.Label(frame_propriedades, text=key).pack(anchor='w', padx=5, pady=2)
            var = tk.StringVar(value=value)
            entry = ttk.Entry(frame_propriedades, textvariable=var)
            entry.pack(anchor='w', padx=5, pady=2)
            propriedades[key] = var

    # Cria um bind pra atualizar quando selecionar outro tipo de widget
    combo_classe.bind('<<ComboboxSelected>>', lambda e:atualizar_classe())

    # Encontra a aba e o canvas
    def click():
        nonlocal canvas_atual
        aba_atual = janela.nametowidget(projeto.notebook.select())
        for child in aba_atual.winfo_children():
            if isinstance(child, tk.Canvas):
                canvas_atual = child
                break
        # Cria o widget depois de clicar no canvas
        classe = tipos_widgets[combo_classe.get()]['classe']
        props = {p: v.get() for p, v in propriedades.items()}
        if canvas_atual:
            canvas_atual.bind("<Button-1>", lambda event: projeto.add_widget(classe, props, event.x, event.y))