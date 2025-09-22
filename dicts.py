import drivers.widgets_driver as wd

#################### Dicionários relacionados aos widgets ####################
# Dicionário com os widgets padrão e suas propriedades
widgets_padrao = {
    'Texto': {
        'classe': wd.Texto,
        'comando':[],
        'visual': {
            'text': 'Texto',
            'font': ('Roboto', 13),
            'text_color': "#000000",
            'fg_color': 'transparent',
            'corner_radius': 0,
            'width': 0,
            'height': 0,
            'image': '',
            'compound': 'left',
        }
    },
    'Botao': {
        'classe': wd.Botao,
        'comando':[
            'Write_Single_Coil',
            'Write_Multiple_Coils',
            'Write_Single_Register',
            'Write_Multiple_Registers',
        ],
        'visual': {
            'text': 'Botao',
            'font': ('Roboto', 13),
            'width': 140,
            'height': 28,
            'corner_radius': 6,
            'border_width': 0,
            'border_spacing': 2,
            'fg_color': "#BEBEBE",
            'hover_color': '#325882',
            'border_color': '#909090',
            'text_color': "#000000",
            'text_color_disabled': '#909090',
            'image': '',
            'compound': 'left',
        }
    },
    'Indicador': {
        'classe': wd.Indicador,
        'comando':[
            'Read_Single_Coil',
            'Read_Single_Register',
        ],
        'visual': {
            'font': ('Arial', 14),
            'text_color': "#000000",
            'fg_color': 'transparent',
            'corner_radius': 0,
            'width': 0,
            'height': 0,
        }
    },
}
# Traduções dos parâmetros dos widgets
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
# Traduções reversas, dic de suporte
traducoes_reverse = {v: k for k, v in traducoes_parametros.items()}
# Propriedades que possuem valores pré-definidos
parametros_especiais = {
    'cores': [
        'text_color',
        'fg_color',
        'hover_color',
        'border_color',
        'text_color_disabled',
        'progress_color',
        'button_color',
        'button_hover_color'
    ],
    'pre-definidos': {
        'compound': ['left', 'right', 'top', 'bottom', 'center'],
        'anchor': ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'center'],
        'state': ['normal', 'disabled'],
        'orientation': ['horizontal', 'vertical']
    },
    'font': {
        'styles': ['normal', 'bold', 'italic', 'bold italic', 'underline', 'overstrike'],
        'sizes': ['8', '10', '12', '14', '16', '18', '20', '24', '30']
    },
    'numericos':[
        'width',
        'height',
        'corner_radius',
        'border_width',
        'border_spacing',
        'from_',
        'to',
        'number_of_steps',
        'padx',
        'pady'
    ]
}
#################### Dicionários relacionados ao modbus ####################
# Opções para os Combobox modbus
selecionaveis_modbus = {
    'Conexão': ['TCP', 'RTU'],
    'Baudrate': ['9600', '19200', '38400', '57600', '115200'],
    'Paridade': ['N', 'P', 'I'],
    'Bytesize': ['8', '7'],
    'Stopbits': ['1', '2']
}
# Estruturas padrão para cada tipo de servidor
estrutura_servidor = {
    'TCP': {'IP': '192.168.0.200', 'Porta': 1502, 'Timeout (s)': 1},
    'RTU': {'ID':1, 'Porta Serial': 'COM3', 'Baudrate': '9600', 'Paridade': 'N', 'Bytesize': 8, 'Stopbits': 1, 'Timeout (s)': 1}
}
# Funções modbus possíveis
funcoes_modbus = {
    'Write_Single_Coil': {
        'parametros': {
            'address': 0,
            'value': ['0','1']
        }
    },
    'Write_Multiple_Coils': {
        'parametros': {
            'address': 0,
            'count': 1,
            'value': ['0','1']
        }
    },
    'Read_Single_Coil': {
        'parametros': {
            'address': 0,
            'sample_delay': 1
        }
    },
    'Write_Single_Register': {
        'parametros': {
            'address': 0,
            'value': 0
        }
    },
    'Write_Multiple_Registers': {
        'parametros': {
            'address': 0,
            'count': 1,
            'value': 0
        }
    },
    'Read_Single_Register': {
        'parametros': {
            'address': 0,
            'sample_delay': 1
        }
    },
}