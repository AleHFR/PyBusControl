import tkinter as tk
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
            'font': None,
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
            'font': None,
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
            'font': None,
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
            'font': None,
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
            'font': None,
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
            'font': None,
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

# Propriedades dos widgets
props_ignoradas = [
    'takefocus',
    'textvariable',
    'bitmap',
    'cursor',
    'underline',
    'insertbackground',
    'insertborderwidth',
    'insertwidth',
    'default',
    'padx',
    'pady',
    'repeatdelay',
    'repeatinterval',
    'compound',
    'borderwidth',  # duplicata de 'bd'
    'foreground',   # duplicata de 'fg'
    'background',   # duplicata de 'bg'
    'activebackground',
    'activeforeground',
    'state',  # já está na props_por_tipo
    'command',  # está na props_por_tipo mas precisa ser tratada na exportação
    'bigincrement',
    'digits',
    'label',
    'variable',
    'sliderrelief',
    'sliderlength',
]

# Auxiliares
props_equivalentes = {
    'text': 'Texto',
    'bg': 'Cor de Fundo',
    'fg': 'Cor do Texto',
    'font': 'Fonte',
    'size': 'Tamanho da Fonte',
    'width': 'Largura',
    'height': 'Altura',
    'command': 'Comando',
    'justify': 'Justificação',
    'orient': 'Orientação',
    'from_': 'Range Mínimo',
    'to': 'Range Máximo',
    'resolution': 'Passo',
    'image': 'Caminho da Imagem',
    'formato': 'Formato',
    'relief': 'Borda',
    'showvalue': 'Exibir Valor',
    'length': 'Comprimento',
    'highlightcolor': 'Cor Borda Interna',
    'highlightbackground': 'Cor Borda Externa',
}

listas_configs_comuns = {
    'font':{
        'Arial',
        'Courier',
        'Times New Roman',
        'Helvetica',
        'Verdana',
        'Tahoma',
        'Comic Sans MS',
        'Lucida Console',
        'Fixedsys'
        'System',
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
}
