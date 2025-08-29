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
    'text': 'Texto',
    'state': 'Estado',
    'image': 'Imagem',
    'compound': 'Posição Imagem/Texto',
    'takefocus': 'Pode Receber Foco',
    'underline': 'Sublinhar Caractere',
    'width': 'Largura',
    'height': 'Altura',
    'background': 'Cor de Fundo',
    'foreground': 'Cor do Texto',
    'font': 'Fonte do Texto',
    'borderwidth': 'Largura da Borda',
    'relief': 'Estilo da Borda',
    'justify': 'Alinhamento do Texto',
    'wraplength': 'Largura de Quebra de Linha',
    'anchor': 'Ancoragem do Conteúdo',
    'textvariable': 'Variável de Texto',
    'show': 'Caractere de Ocultação',
    'fieldbackground': 'Cor do Fundo do Campo',
    'insertcolor': 'Cor do Cursor de Texto',
    'selectbackground': 'Cor de Fundo da Seleção',
    'selectforeground': 'Cor do Texto Selecionado',
    'from_': 'Valor Mínimo',
    'to': 'Valor Máximo',
    'orient': 'Orientação',
    'length': 'Comprimento',
    'variable': 'Variável Associada',
    'value': 'Valor',
    'troughcolor': 'Cor da Trilha',
    'values': 'Valores da Lista',
    'arrowcolor': 'Cor da Seta',
    'arrowsize': 'Tamanho da Seta',
    'onvalue': 'Valor Ligado',
    'offvalue': 'Valor Desligado',
    'padding': 'Espaçamento Interno',
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