from datetime import datetime as dt

# Cores
bg = "#f0f0f0"

# Fonte
fonte_titulo = ('Calibri', 12)
fonte_texto = ('Calibri', 10)

# Tamanho do canva padrão
tamanho_x = 1280
tamanho_y = 720

# Itens do menu de contexto do canvas
tipos_widgets = {
    'Botão': {
        'classe': 'Button',
        'propriedades': {
            'text': 'Botão',
        }
    },
    'Texto': {
        'classe': 'Label',
        'propriedades': {
            'text': 'Texto',
        }
    },
    'Indicador': {
        'classe': 'Label',
        'propriedades': {
            'text': '0.00',
        }
    },
    'Sinalizador': {
        'classe': 'Label',
        'propriedades': {
            'text': '●',
        }
    },
    'Slider': {
        'classe': 'Scale',
        'propriedades': {
            'from_': 0,
            'to': 100,
            'orient': 'horizontal',
            'length': 100,
        }
    },
    'Imagem': {
        'classe': 'Label',
        'propriedades': {
            'text': 'Imagem',
        }
    },
    'Relógio': {
        'classe': 'Label',
        'propriedades': {
            'text': dt.now().strftime('%d/%m/%Y %H:%M:%S'),
        }
    },
}

# Propriedades que não quero usar
props_ignoradas = [

]

# Dicionário de tradução de propriedades
props_equivalentes = {
    # --- Comportamento e Conteúdo ---
    'text': 'Texto',
    'textvariable': 'Variável de Texto',
    'command': 'Comando (Função)',
    'style': 'Estilo Aplicado',
    'state': 'Estado',
    'cursor': 'Cursor do Mouse',
    'takefocus': 'Pode Receber Foco',
    'underline': 'Sublinhar Caractere',
    'image': 'Imagem',
    'compound': 'Composição Imagem/Texto',
    'variable': 'Variável Associada',
    'values': 'Valores da Lista (Combobox)',
    'show': 'Caractere de Ocultação (Senha)',

    # --- Dimensão e Posição ---
    'width': 'Largura (em caracteres)',
    'length': 'Comprimento (em pixels)',
    'padding': 'Espaçamento Interno',
    'justify': 'Alinhamento do Texto',
    'orient': 'Orientação',
    'anchor': 'Ancoragem do Conteúdo',
    
    # --- Aparência (via Estilo) ---
    'font': 'Fonte do Texto',
    'background': 'Cor de Fundo',
    'foreground': 'Cor do Texto',
    'borderwidth': 'Largura da Borda',
    'relief': 'Estilo da Borda',
    
    # --- Específicos de Widgets (Comportamento e Estilo) ---
    'from_': 'Valor Mínimo (Scale)',
    'to': 'Valor Máximo (Scale)',
    'troughcolor': 'Cor da Trilha (Scale)',
    'arrowcolor': 'Cor da Seta (Spinbox)',
    'fieldbackground': 'Cor de Fundo do Campo de Texto',
    'insertcolor': 'Cor do Cursor de Texto',
    'selectbackground': 'Cor de Fundo da Seleção',
    'selectforeground': 'Cor do Texto Selecionado',
}

# Dicionário de propriedades comuns
# Propriedades com valores fixos para seleção
props_selecionaveis = {
    'state': {
        'normal',      # Habilitado e interativo
        'disabled',    # Desabilitado
        'readonly',    # Apenas leitura (para Entry/Combobox)
    },
    'orient': {
        'horizontal',
        'vertical',
    },
    'justify': {
        'left',
        'center',
        'right',
    },
    'relief': {
        'flat',
        'groove',
        'raised',
        'ridge',
        'solid',
        'sunken',
    },
    'anchor': {
        'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'center'
    },
    'compound': {
        'top',
        'bottom',
        'left',
        'right',
        'center',
        'none',
    },
    'takefocus': {
        True,
        False,
    },
}

# Propriedades com cores
props_cor = [
    'background',
    'foreground',
    'troughcolor',
    'arrowcolor',
    'fieldbackground',
    'insertcolor',
    'selectbackground',
    'selectforeground',
]