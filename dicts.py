#################### Dicionários relacionados aos widgets ####################
# Traduções dos parâmetros dos widgets
traducoes_parametros = {
    "text": "Texto",
    "font": "Fonte",
    "text_color": "Cor do Texto",
    "fg_color": "Cor de Fundo",
    "corner_radius": "Raio da Borda",
    "width": "Largura",
    "height": "Altura",
    "image": "Imagem",
    "compound": "Composição",
    "border_width": "Largura da Borda",
    "border_spacing": "Espaçamento da Borda",
    "hover_color": "Cor ao Passar Mouse",
    "border_color": "Cor da Borda",
    "from_": "De",
    "to": "Para",
    "number_of_steps": "Número de Passos",
    "orientation": "Orientação",
    "progress_color": "Cor do Progresso",
    "button_color": "Cor do Botão",
    "button_hover_color": "Cor do Botão ao Passar Mouse",
    "variable": "Variável",
    "onvalue": "Valor Ligado",
    "offvalue": "Valor Desligado"
}
# Traduções reversas, dic de suporte
traducoes_reverse = {v: k for k, v in traducoes_parametros.items()}
# Propriedades que possuem valores pré-definidos
parametros_especiais = {
    "cores": [
        "text_color",
        "fg_color",
        "hover_color",
        "border_color",
        "text_color_disabled",
        "progress_color",
        "button_color",
        "button_hover_color"
    ],
    "pre-definidos": {
        "compound": ["left", "right", "top", "bottom", "center"],
        "anchor": ["n", "ne", "e", "se", "s", "sw", "w", "nw", "center"],
        "state": ["normal", "disabled"],
        "orientation": ["horizontal", "vertical"]
    },
    "font": {
        "styles": ["normal", "bold", "italic", "bold italic", "underline", "overstrike"],
        "sizes": [str(tamanho) for tamanho in range(8, 51)]
    },
    "numericos":[
        "width",
        "height",
        "corner_radius",
        "border_width",
        "border_spacing",
        "from_",
        "to",
        "number_of_steps",
        "padx",
        "pady"
    ]
}
parametros_nao_visuais = [
    "textvariable",
]
#################### Dicionários relacionados ao modbus ####################
# Funções modbus possíveis
funcoes_modbus = {
    "Write_Single_Coil": {
        "parametros": {
            "address": 0,
            "value": 0
        }
    },
    # "Write_Multiple_Coils": {
    #     "parametros": {
    #         "address": 0,
    #         "count": 1,
    #         "value": 0
    #     }
    # },
    "Write_Single_Register": {
        "parametros": {
            "address": 0,
            "value": 0
        }
    },
    # "Write_Multiple_Registers": {
    #     "parametros": {
    #         "address": 0,
    #         "count": 1,
    #         "value": 0
    #     }
    # },
    "Read_Single_Coil": {
        "parametros": {
            "address": 0,
        }
    },
    "Read_Single_Register": {
        "parametros": {
            "address": 0,
        }
    },
    "Trocar Aba":{
        "parametros": {
            "aba": "",
        }
    }
}