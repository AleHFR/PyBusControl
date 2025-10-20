import customtkinter as ctk

# Classe mãe interna pra configurar as demais widgets
class Widget():
    def __init__(self, canvas, classe, posicao, propriedades):
        # Atributos do widget
        self.classe = classe
        self.posicao = posicao
        self.caminho_imagem = None
        # Atributos de refrerência
        self.classeCTk = getattr(ctk, classe)
        self.canvas = canvas
        self.item = self.classeCTk(self.canvas, **propriedades)
        self.imagem = None

    def get(self):
        return self.item

class Texto(Widget):
    def __init__(self, canvas, posicao):
        self.nome = "Texto"
        self.propriedades = {
            "text": "Texto",
            "font": ("Roboto", 13),
            "text_color": "#000000",
            "fg_color": "transparent",
            "corner_radius": 0,
            "width": 0,
            "height": 0,
            "image": "",
            "compound": "left",
        }
        self.comando = None
        super().__init__(canvas=canvas, classe="CTkLabel", posicao=posicao, propriedades=self.propriedades)

class Botao(Widget):
    def __init__(self, canvas, posicao):
        self.nome = "Botao"
        self.propriedades = {
            "text": "Botao",
            "font": ("Roboto", 13),
            "width": 140,
            "height": 28,
            "corner_radius": 6,
            "border_width": 0,
            "border_spacing": 2,
            "fg_color": "#BEBEBE",
            "hover_color": "#325882",
            "border_color": "#909090",
            "text_color": "#000000",
            "image": "",
            "compound": "left",
        }
        self.comando = {
            "comando": " ",
            "parametros":{}
        }
        super().__init__(canvas=canvas, classe="CTkButton", posicao=posicao, propriedades=self.propriedades)

class Indicador(Widget):
    def __init__(self, canvas, posicao):
        self.nome = "Indicador"
        self.prefixo = ""
        self.sulfixo = ""
        self.casa_decimal = 0
        self.valor_interno = ctk.StringVar(value="0")
        self.propriedades = {
            "font": ("Arial", 14),
            "text_color": "#000000",
            "fg_color": "transparent",
            "corner_radius": 0,
            "width": 0,
            "height": 0,
            "textvariable": self.valor_interno,
        }
        self.comando = {
            "comando": " ",
            "parametros":{}
        }
        super().__init__(canvas=canvas, classe="CTkLabel", posicao=posicao, propriedades=self.propriedades)

    def set_prefixo(self, texto: str):
        self.prefixo = texto
        self.atualizar()

    def set_sulfixo(self, texto: str):
        self.sulfixo = texto
        self.atualizar()
    
    def set_casa_decimal(self, casa: int):
        self.casa_decimal = int(casa)
        self.atualizar()
    
    def atualizar(self, valor="0"):
        try:
            valor = float(valor)
            texto_formatado = f"{self.prefixo}{round(valor, self.casa_decimal):.{self.casa_decimal}f}{self.sulfixo}"
            self.valor_interno.set(texto_formatado)
        except Exception as e:
            texto_formatado = f"{self.prefixo}Erro{self.sulfixo}"
            self.valor_interno.set(texto_formatado)
            print(f"[ERRO] -> {type(e).__name__}: {e}")