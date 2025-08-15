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
            'bg': 'white',
            'fg': 'black',
            'font': 'Arial',
            'width': None,
            'height': None,
            'state': 'normal',
            'command': lambda: print("Botão pressionado"),
        }
    },
    'Texto': {
        'classe': 'Label',
        'propriedades': {
            'text': 'Texto',
            'bg': 'white',
            'fg': 'black',
            'font': 'Arial',
            'width': None,
            'height': None,
            'state': 'normal',
        }
    },
    'Indicador': {
        'classe': 'Label',
        'propriedades': {
            'text': '0.00',
            'bg': 'white',
            'fg': 'black',
            'font': 'Arial',
            'width': None,
            'height': None,
            'state': 'normal',
        }
    },
    'LED': {
        'classe': 'Label',
        'propriedades': {
            'text': '●',
            'bg': 'white',
            'fg': 'red',
            'font': 'Arial',
            'width': 1,
            'height': 1,
            'state': 'normal',
        }
    },
    'Slider': {
        'classe': 'Scale',
        'propriedades': {
            'from_': 0,
            'to': 100,
            'orient': 'horizontal',
            'bg': 'SystemButtonFace',
            'fg': 'black',
            'font': 'Arial',
            'width': None,
            'height': None,
            'from_': 0,
            'to': 10,
            'state': 'normal',
        }
    },
    'Imagem': {
        'classe': 'Label',
        'propriedades': {
            'text': 'Imagem',
            'bg': 'gray',
            'fg': 'white',
            'relief': 'groove',
            'bd': 2,
            'font': 'Arial',
            'width': 30,
            'height': 10,
            'state': 'normal',
        }
    },
    'Relógio': {
        'classe': 'Label',
        'propriedades': {
            'text': dt.now().strftime('%d/%m/%Y %H:%M:%S'),
            'bg': 'white',
            'fg': 'black',
            'font': ('Consolas', 12),
            'width': None,
            'height': None,
            'state': 'normal',
        }
    },
}

# Propriedades que não quero usar
props_ignoradas = [
    'takefocus',           # Controle de foco do teclado
    'textvariable',        # Ligação de variável (manipulado no código)
    'bitmap',              # Pouco usado, só imagens internas do Tk
    'cursor',              # Cursor do mouse sobre o widget
    'underline',           # Índice do caractere sublinhado
    'default',             # Estado padrão de botão (OK, Cancel)
    'repeatdelay',         # Delay antes de repetição (para Spinbox/Button)
    'repeatinterval',      # Intervalo de repetição
    'compound',            # Posição imagem/texto (normalmente fixo)
    'bigincrement',        # Incremento grande no Scale
    'digits',              # Dígitos no Scale
    'label',               # Label no Scale (normalmente fixo)
    'variable',            # Variável associada (manipulada no código)
    'highlightcolor',      # Cor interna de foco
    'highlightbackground', # Cor externa de foco
    'highlightthickness',  # Espessura de foco
    'takefocus',           # Controle de foco do teclado
    'bitmap',              # Pouco usado, só imagens internas do Tk
    'justify',             # Alinhamento do texto
    'state',               # Estado do botão
    'padx',                # Espaço horizontal interno
    'pady',                # Espaço vertical interno
    'activebackground',    # Cor de fundo ativa
    'activeforeground',    # Cor de texto ativo
    'bd',                  # Espessura da borda - cópia de borderwidth
    'default',             # Estado padrão de botão (OK, Cancel)
    'overrelief',          # Relieve ao passar o mouse
    'repeatdelay',         # Delay antes de repetição
    'repeatinterval',      # Intervalo de repetição
    'disabledforeground',  # Cor de texto desabilitado
]

# Dicionário de tradução de propriedades
props_equivalentes = {
    # Comuns
    'text': 'Texto',
    'bg': 'Cor de Fundo',
    'fg': 'Cor do Texto',
    'font': 'Fonte',
    'width': 'Largura',
    'height': 'Altura',
    'cursor': 'Cursor',
    'relief': 'Borda',
    'borderwidth': 'Espessura da Borda',
    'bd': 'Espessura da Borda',
    'highlightbackground': 'Cor da Borda de Destaque (Fora)',
    'highlightcolor': 'Cor da Borda de Destaque (Dentro)',
    'highlightthickness': 'Espessura da Borda de Destaque',
    'anchor': 'Ancoragem',
    'image': 'Imagem',
    'bitmap': 'Bitmap',
    'compound': 'Composição Imagem/Text',
    'underline': 'Sublinhar Caractere',
    'justify': 'Alinhamento do Texto',
    'padx': 'Espaço Horizontal Interno',
    'pady': 'Espaço Vertical Interno',
    'state': 'Estado',
    'takefocus': 'Pode Receber Foco',
    'activebackground': 'Cor de Fundo Ativa',
    'activeforeground': 'Cor do Texto Ativo',
    'disabledforeground': 'Cor do Texto Desabilitado',
    'overrelief': 'Borda ao Passar o Mouse',

    # Label
    'wraplength': 'Largura de Quebra de Texto',

    # Button
    'command': 'Comando',
    'default': 'Botão Padrão',

    # Scale (Slider)
    'from_': 'Valor Mínimo',
    'to': 'Valor Máximo',
    'orient': 'Orientação',
    'resolution': 'Passo',
    'showvalue': 'Exibir Valor',
    'length': 'Comprimento',
    'sliderlength': 'Comprimento do Slider',
    'sliderrelief': 'Borda do Slider',
    'troughcolor': 'Cor da Trilha',
    'digits': 'Número de Dígitos',
    'label': 'Rótulo',
    'bigincrement': 'Incremento Grande',
    'variable': 'Variável Associada',

    # Entry
    'show': 'Caractere de Ocultação',
    'exportselection': 'Exportar Seleção',
    'insertbackground': 'Cor do Cursor',
    'insertborderwidth': 'Espessura do Cursor',
    'insertofftime': 'Cursor Piscando (Off)',
    'insertontime': 'Cursor Piscando (On)',
    'insertwidth': 'Largura do Cursor',
    'selectbackground': 'Cor de Seleção',
    'selectborderwidth': 'Espessura da Seleção',
    'selectforeground': 'Cor do Texto Selecionado',

    # Outros
    'repeatdelay': 'Delay de Repetição',
    'repeatinterval': 'Intervalo de Repetição',
}

# Dicionário de propriedades comuns
# Propriedades com valores fixos para seleção
props_selecionaveis = {
    'font': {
        'Arial',
        'Courier',
        'Times New Roman',
        'Helvetica',
        'Verdana',
        'Tahoma',
        'Comic Sans MS',
        'Lucida Console',
        'Fixedsys',
        'Terminal',
        'Consolas',
        'Calibri',
        'Cambria',
        'Segoe UI',
    },
    'justify': {
        'left',
        'center',
        'right',
    },
    'orient': {
        'horizontal',
        'vertical',
    },
    'relief': {
        'groove',
        'ridge',
        'sunken',
        'raised',
        'flat',
    },
    'anchor': {
        'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'center'
    },
    'state': {
        'normal',
        'active',
        'disabled',
    },
    'compound': {
        'top',
        'bottom',
        'left',
        'right',
        'center',
        'none',
    },
    'showvalue': {
        True,
        False,
    },
    'underline': {
        True,
        False,
    },
    'wrap': {  # Para Label, texto com quebra automática
        True,
        False,
    },
    'takefocus': {
        True,
        False,
    },
    'repeatdelay': {  # numérico, então deixo comentado
        # valores inteiros em ms
    },
    'repeatinterval': {  # numérico
        # valores inteiros em ms
    },
    'highlightthickness': {  # numérico
        # valores inteiros em px
    },
}

# Propriedades com cores
props_cor = [
    'bg',
    'background',
    'fg',
    'foreground',
    'activebackground',
    'activeforeground',
    'disabledforeground',
    'highlightbackground',
    'highlightcolor',
    'selectbackground',
    'selectforeground',
    'troughcolor',
    'insertbackground',
]