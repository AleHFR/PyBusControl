import customtkinter as ctk

# Classe mãe interna pra configurar as demais widgets
class Widget():
    def __init__(self, canvas, classe, posicao, **kwargs):
        self.canvas = canvas
        self.classe = classe
        self.posicao = posicao
        self.propriedades = kwargs
        self.classeCTk = getattr(ctk, classe)
        self.item = self.classeCTk(self.canvas, **self.propriedades)
        self.imagem = None

    def get(self):
        return self.item

class Texto(Widget):
    def __init__(self, canvas, posicao, **kwargs):
        super().__init__(canvas=canvas, classe="CTkLabel", posicao=posicao, **kwargs)

class Botao(Widget):
    def __init__(self, canvas, posicao, **kwargs):
        super().__init__(canvas=canvas, classe="CTkButton", posicao=posicao, **kwargs)

class Indicador(Widget):
    def __init__(self, canvas, posicao, **kwargs):
        self.prefixo = ''
        self.sulfixo = ''
        self.casa_decimal = 0
        self.valor_interno = ctk.StringVar(value='0')
        
        super().__init__(canvas=canvas, classe="CTkLabel", posicao=posicao, textvariable=self.valor_interno, **kwargs)

    def set_prefixo(self, texto: str):
        self.prefixo = texto
        self._update_display()

    def set_sufixo(self, texto: str):
        self.sulfixo = texto
        self._update_display()
    
    def set_casa_decimal(self, casas: int):
        self.casa_decimal = casas
        self._update_display()
    
    def atualizar(self, valor):
        try:
            valor = float(valor)
            texto_formatado = f"{self.prefixo}{round(valor, self.casa_decimal):.{self.casa_decimal}f}{self.sulfixo}"
            self.valor_interno.set(texto_formatado)
        except (ValueError, TypeError):
            self.valor_interno.set("Erro")
            
    def _update_display(self):
        try:
            valor_atual = float(self.valor_interno.get())
            self.atualizar(valor_atual)
        except ValueError:
            pass