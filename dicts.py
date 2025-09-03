widgets_padrao = {
    'Texto': {
        'classe': 'CTkLabel',
        'propriedades': {
            'text': 'Texto',
            'font': ('Roboto', 13),
            'text_color': "#000000",
            'fg_color': 'transparent',
            'corner_radius': 0,
            'width': 0,
            'height': 0,
            'image': None,
            'compound': 'left',
            'anchor': 'center'
        }
    },
    'Botão': {
        'classe': 'CTkButton',
        'propriedades': {
            'text': 'Botão',
            'font': ('Roboto', 13),
            'state': 'normal',
            'width': 140,
            'height': 28,
            'corner_radius': 6,
            'border_width': 0,
            'border_spacing': 2,
            'fg_color': "#FFFFFF",
            'hover_color': '#325882',
            'border_color': None,
            'text_color': "#000000",
            'text_color_disabled': '#909090',
            'image': None,
            'compound': 'left',
            'anchor': 'center'
        }
    },
    'Indicador': {
        'classe': 'CTkLabel',
        'propriedades': {
            'text': '0.00',
            'font': ('Arial', 14),
            'text_color': "#000000",
            'fg_color': 'transparent',
            'corner_radius': 0,
            'width': 0,
            'height': 0,
            'anchor': 'center'
        }
    },
    'Slider': {
        'classe': 'CTkSlider',
        'propriedades': {
            'from_': 0,
            'to': 100,
            'number_of_steps': None,
            'orientation': 'horizontal',
            'width': 200,
            'height': 16,
            'fg_color': '#565B5E',
            'progress_color': '#3B8BBE',
            'button_color': '#DCE4EE',
            'button_hover_color': '#BFC9C9'
        }
    },
    'Caixa de Seleção': {
        'classe': 'CTkCheckBox',
        'propriedades': {
            'text': 'Opção',
            'variable': None,
            'onvalue': 1,
            'offvalue': 0,
            'font': ('Roboto', 13),
            'width': 0,
            'height': 0,
            'corner_radius': 6,
            'border_width': 3,
            'fg_color': '#2A2D2E',
            'hover_color': '#3B3B3B',
            'border_color': '#3B8BBE',
            'text_color': "#000000"
        }
    },
    'Interruptor': {
        'classe': 'CTkSwitch',
        'propriedades': {
            'text': 'Opção',
            'variable': None,
            'onvalue': 1,
            'offvalue': 0,
            'font': ('Roboto', 13),
            'width': 50,
            'height': 24,
            'corner_radius': 1000,
            'border_width': 3,
            'border_color': '#3B8BBE',
            'fg_color': "#FFFFFF",
            'progress_color': '#3B8BBE',
            'button_color': '#DCE4EE',
            'button_hover_color': '#BFC9C9',
            'text_color': "#000000"
        }
    },
}

traducoes_parametros = {
    'text': 'Texto',
    'font': 'Fonte',
    'text_color': 'Cor do Texto',
    'fg_color': 'Cor de Fundo',
    'corner_radius': 'Raio da Borda',
    'width': 'Largura',
    'height': 'Altura',
    'image': 'Caminho da Imagem',
    'compound': 'Composição',
    'anchor': 'Âncora',
    'state': 'Estado',
    'border_width': 'Largura da Borda',
    'border_spacing': 'Espaçamento da Borda',
    'hover_color': 'Cor ao Passar Mouse',
    'border_color': 'Cor da Borda',
    'text_color_disabled': 'Cor do Texto Desabilitado',
    'from_': 'De',
    'to': 'Para',
    'number_of_steps': 'Número de Passos',
    'orientation': 'Orientação',
    'progress_color': 'Cor do Progresso',
    'button_color': 'Cor do Botão',
    'button_hover_color': 'Cor do Botão ao Passar Mouse',
    'variable': 'Variável',
    'onvalue': 'Valor Ligado',
    'offvalue': 'Valor Desligado'
}

parametros_especiais = {
    'cores': ['text_color', 'fg_color', 'hover_color', 'border_color', 'text_color_disabled', 'progress_color', 'button_color', 'button_hover_color'],
    'pre-definidos': {
        'compound': ['left', 'right', 'top', 'bottom', 'center'],
        'anchor': ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'center'],
        'state': ['normal', 'disabled'],
        'orientation': ['horizontal', 'vertical']
    }
}

funcoes = {
    'Write_Single_Coil': {
        'parametros': {
            'server': '',
            'slave_id': 0,
            'address': 0,
            'value': 0
        }
    },
    'Read_Single_Coil': {
        'parametros': {
            'server': '',
            'slave_id': 0,
            'start_address': 0,
            'num_coils': 0
        }
    },
    'Write_Single_Registe': {
        'parametros': {
            'server': '',
            'slave_id': 0,
            'address': 0,
            'value': 0
        }
    },
    'Read_Single_Register': {
        'parametros': {
            'server': '',
            'slave_id': 0,
            'start_address': 0,
            'num_registers': 0
        }
    },
}