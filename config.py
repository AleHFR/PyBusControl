import tkinter as tk
from datetime import datetime as dt

# Cores
bg = "#f0f0f0"

# Fonte
fonte_titulo = ('Calibri', 12)
fonte_texto = ('Calibri', 10)

# Tamanho do canva padrão
tamanho_x = 1000
tamanho_y = 600
tamanho_x_max = 1920
tamanho_y_max = 1080

# Itens do menu de contexto do canvas
tipos_widgets = {
    'Botão': {
        'classe': tk.Button,
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
        'classe': tk.Label,
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
        'classe': tk.Label,
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
        'classe': tk.Label,
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
        'classe': tk.Scale,
        'propriedades': {
            'from_': 0,
            'to': 100,
            'orient': 'horizontal',
            'bg': 'SystemButtonFace',
            'fg': 'black',
            'font': None,
            'width': None,
            'height': None,
            'state': 'normal',
        }
    },
    'Imagem': {
        'classe': tk.Label,
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
        'classe': tk.Label,
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

props_gerais = {
    'Texto': {
        'text': ''
    },
    'Fonte': {
        'font': [
            'Padrão',
            'Arial',
            'Helvetica',
            'Courier'
        ],
        'size': ''
    },
    'Cor do Texto': {
        'fg': ''
    },
    'Cor de Fundo': {
        'bg': ''
    },
    'Largura': {
        'width': ''
    },
    'Altura': {
        'height': ''
    },
    'Borda': {
        'relief': {
            'Liso': 'flat',
            'Elevado': 'raised',
            'Afundado': 'sunken',
            'Entalhado': 'groove',
            'Saliênte': 'ridge'
        }
    },
}

props_especificas = {
    'Botão': ['Registrador'],
    'Texto': ['Justificação'],
    'Indicador': ['Unidade', 'Casas Decimais'],
    'LED': ['Cor Ligado', 'Cor Desligado'],
    'Slider': ['Range Mínimo', 'Range Máximo', 'Passo'],
    'Imagem': ['Caminho do Arquivo'],
    'Relógio': ['Formato'],
}