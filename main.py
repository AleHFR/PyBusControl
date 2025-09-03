########### Preâmbulo ###########
# Imports do python
import customtkinter as ctk
import platform

# Imports do projeto
import gui_manager as gm
import custom_widgets as cw

########## Janela principal ##########
root = ctk.CTk()
root.title('PyBusControl')
ctk.set_appearance_mode('light')
# Icone
root.iconphoto(True, cw.imagem('pbc.png'))
# Estilo
# style = ttk.Style(root)

########## Configura conforme o sistema operacional ##########
def maximizar_janela():
    system = platform.system()
    if system == "Windows":
        root.state('zoomed')
    else: # Funciona para Linux e macOS
        root.attributes('-zoomed', True)

########## Menu ##########
menu_bar = cw.customMenu(root)
root.config(menu=menu_bar)

# Criar um menu de arquivo
menu_arquivo = cw.customMenu(menu_bar)
menu_bar.add_cascade(label="Arquivo", menu=menu_arquivo)
menu_arquivo.add_command(label="Novo Projeto", command=lambda:gm.novo_projeto(root))
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Preferências", command=lambda:cw.preferencias())
menu_arquivo.add_command(label="Sair", command=root.quit)

##########  ##########
# Espaçamento em cima
ctk.CTkLabel(root, text='').pack(side='top', fill='both', expand=True)

frame_central = ctk.CTkFrame(root, corner_radius=5)
frame_central.pack(expand=True, padx=20, pady=20)

# Configuração do grid
frame_central.columnconfigure(0, weight=1)
frame_central.columnconfigure(1, weight=2)
frame_central.rowconfigure(0, weight=1)

# Coluna da esquerda (botões)
frame_btn = ctk.CTkFrame(frame_central, fg_color='transparent', corner_radius=0)
frame_btn.grid(row=0, column=0, padx=20, pady=20, sticky='ns')

ctk.CTkButton(frame_btn, text='Novo Projeto', command=lambda:gm.novo_projeto(root)).pack(pady=5, fill='x')

# Coluna da direita (arquivos recentes)
frame_arquivos = ctk.CTkFrame(frame_central, fg_color='transparent', corner_radius=0)
ctk.CTkLabel(frame_arquivos, text='Arquivos Recentes').pack(pady=5, fill='x', anchor='nw')
frame_arquivos.grid(row=0, column=1, padx=20, pady=20)

lista = ctk.CTkTextbox(frame_arquivos, width=200, height=200, exportselection=False)
# lista.configure(state='disabled')
lista.pack(fill='both', expand=True, padx=5, pady=5)

# Espaçamento embaixo
ctk.CTkLabel(root, text='').pack(side='bottom', fill='both', expand=True)

# Deixa a tela maximizada
root.after(5, maximizar_janela)
root.mainloop()