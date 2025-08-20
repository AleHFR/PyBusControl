from datetime import datetime as dt

# Fonte
fonte_titulo = ('Calibri', 12)
fonte_texto = ('Calibri', 10)

# Tamanho do canva padrão
tamanho_x = 1280
tamanho_y = 720



# Propriedades que não quero usar
props_ignoradas = [
    'style',
    'class',
    'command',
    'cursor',
    'justify',
    'default',
    'textvariable',
    'padding',
]

# Dicionário de tradução de propriedades
props_equivalentes = {
    'Button': {
        'text': 'Texto do Botão',
        'state': 'Estado (normal/disabled)',
        'image': 'Imagem',
        'compound': 'Posição Imagem/Texto',
        'takefocus': 'Pode Receber Foco',
        'underline': 'Sublinhar Caractere',
        'width': 'Largura (em caracteres)',
        'background': 'Cor de Fundo',
        'foreground': 'Cor do Texto',
        'font': 'Fonte do Texto',
        'borderwidth': 'Largura da Borda',
        'relief': 'Estilo da Borda',
    },
    'Label': {
        'text': 'Texto do Rótulo',
        'image': 'Imagem',
        'compound': 'Posição Imagem/Texto',
        'justify': 'Alinhamento do Texto',
        'wraplength': 'Largura de Quebra de Linha',
        'anchor': 'Ancoragem do Conteúdo',
        'width': 'Largura (em caracteres)',
        'background': 'Cor de Fundo',
        'foreground': 'Cor do Texto',
        'font': 'Fonte do Texto',
        'borderwidth': 'Largura da Borda',
        'relief': 'Estilo da Borda',
    },
    'Entry': {
        'textvariable': 'Variável de Texto',
        'width': 'Largura (em caracteres)',
        'show': 'Caractere de Ocultação (Senha)',
        'state': 'Estado (normal/disabled/readonly)',
        'justify': 'Alinhamento do Texto',
        'fieldbackground': 'Cor do Fundo do Campo',
        'foreground': 'Cor do Texto',
        'font': 'Fonte do Texto',
        'insertcolor': 'Cor do Cursor de Texto',
        'selectbackground': 'Cor de Fundo da Seleção',
        'selectforeground': 'Cor do Texto Selecionado',
        'borderwidth': 'Largura da Borda',
        'relief': 'Estilo da Borda',
    },
    'Scale': {
        'from_': 'Valor Mínimo',
        'to': 'Valor Máximo',
        'orient': 'Orientação (horizontal/vertical)',
        'length': 'Comprimento (em pixels)',
        'variable': 'Variável Associada',
        'value': 'Valor Inicial',
        'state': 'Estado (normal/disabled)',
        'troughcolor': 'Cor da Trilha',
        'background': 'Cor do Controle Deslizante',
        'borderwidth': 'Largura da Borda do Controle',
        'relief': 'Estilo da Borda do Controle',
    },
    'Combobox': {
        'values': 'Valores da Lista',
        'textvariable': 'Variável de Texto',
        'state': 'Estado (normal/readonly)',
        'width': 'Largura (em caracteres)',
        'justify': 'Alinhamento do Texto',
        'fieldbackground': 'Cor do Fundo do Campo',
        'foreground': 'Cor do Texto',
        'font': 'Fonte do Texto',
        'arrowcolor': 'Cor da Seta',
        'arrowsize': 'Tamanho da Seta',
        'selectbackground': 'Cor de Fundo da Seleção',
        'selectforeground': 'Cor do Texto Selecionado',
    },
    'Checkbutton': {
        'text': 'Texto do Rótulo',
        'variable': 'Variável Associada',
        'onvalue': 'Valor (Ligado)',
        'offvalue': 'Valor (Desligado)',
        'state': 'Estado (normal/disabled/alternate)',
        'background': 'Cor de Fundo',
        'foreground': 'Cor do Texto',
        'font': 'Fonte do Texto',
        'padding': 'Espaçamento Interno',
    },
    'Radiobutton': {
        'text': 'Texto do Rótulo',
        'variable': 'Variável Associada (do grupo)',
        'value': 'Valor deste Botão',
        'state': 'Estado (normal/disabled)',
        'background': 'Cor de Fundo',
        'foreground': 'Cor do Texto',
        'font': 'Fonte do Texto',
        'padding': 'Espaçamento Interno',
    },
    'Frame': {
        'width': 'Largura (pixels)',
        'height': 'Altura (pixels)',
        'borderwidth': 'Largura da Borda',
        'relief': 'Estilo da Borda',
        'background': 'Cor de Fundo',
    },
}

# Dcionário das propriedades que têm valores para seleção.
props_selecionaveis = {
    # Controla o estado de interatividade do widget.
    'state': {
        'normal',      # Habilitado e interativo (padrão).
        'disabled',    # Cinza e não interativo.
        'readonly',    # O usuário não pode digitar, apenas selecionar (para Entry/Combobox).
    },
    # Define a orientação de widgets como Scale (slider) e Separator.
    'orient': {
        'horizontal',  # Orientação horizontal (da esquerda para a direita).
        'vertical',    # Orientação vertical (de cima para baixo).
    },
    # Define o alinhamento horizontal do texto dentro de um widget.
    'justify': {
        'left',        # Alinha o texto à esquerda.
        'center',      # Centraliza o texto.
        'right',       # Alinha o texto à direita.
    },
    # Define o estilo visual da borda de um widget (controlado via ttk.Style).
    'relief': {
        'flat',        # Sem borda visível.
        'groove',      # Borda "entalhada".
        'raised',      # Borda que parece elevada.
        'ridge',       # Borda que parece uma crista.
        'solid',       # Borda sólida de uma única cor.
        'sunken',      # Borda que parece afundada.
    },
    # Define a posição do conteúdo (texto ou imagem) dentro do espaço alocado para o widget.
    'anchor': {
        'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw',  # Pontos cardeais (Norte, Nordeste, etc.)
        'center'       # Centralizado (padrão).
    },
    # Define a posição da imagem em relação ao texto em widgets como Button e Label.
    'compound': {
        'top',         # Imagem acima do texto.
        'bottom',      # Imagem abaixo do texto.
        'left',        # Imagem à esquerda do texto.
        'right',       # Imagem à direita do texto.
        'center',      # Texto sobre a imagem.
        'none',        # Mostra apenas a imagem se houver, senão mostra o texto (padrão).
    },
    # Controla se o widget pode receber foco de navegação (usando a tecla Tab).
    'takefocus': {
        True,          # O widget pode ser focado.
        False,         # O widget não pode ser focado.
    },
}

# Propriedades com cores
props_cor = [
    # --- Cores Principais ---
    'background',         # Cor de fundo geral de um widget (ex: Botão, Frame)
    'foreground',         # Cor do texto principal

    # --- Cores de Campo de Entrada (Entry, Combobox) ---
    'fieldbackground',    # Cor de fundo da área onde se digita o texto
    'insertcolor',        # Cor do cursor de texto (o pipe que pisca)
    
    # --- Cores de Seleção (Entry, Combobox, Treeview) ---
    'selectbackground',   # Cor de fundo do texto quando selecionado
    'selectforeground',   # Cor do texto quando selecionado

    # --- Cores Específicas de Componentes ---
    'troughcolor',        # Cor da "trilha" por onde o slider desliza (Scale, Scrollbar)
    'arrowcolor',         # Cor das setas em um Spinbox ou Scrollbar
    
    # --- Cores de Borda (Menos comum, depende do tema) ---
    'bordercolor',        # Cor da borda principal
    'lightcolor',         # Cor da parte clara da borda (para efeito 3D)
    'darkcolor',          # Cor da parte escura da borda (para efeito 3D)
]